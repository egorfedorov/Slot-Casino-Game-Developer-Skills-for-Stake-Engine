#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const TEXT_EXTENSIONS = new Set([
  ".md",
  ".txt",
  ".json",
  ".js",
  ".mjs",
  ".cjs",
  ".ts",
  ".tsx",
  ".jsx",
  ".html",
  ".css"
]);

const SKIP_DIRS = new Set([
  ".git",
  "node_modules",
  "dist",
  "build",
  ".next",
  ".cache",
  "coverage"
]);

function printUsage() {
  console.error(
    "Usage: node scripts/audit-checklist.mjs --rules <path> --target <path> [--social true|false] [--format json|text]"
  );
}

function parseArgs(argv) {
  const args = {
    rules: "",
    target: "",
    social: true,
    format: "json"
  };

  for (let i = 0; i < argv.length; i += 1) {
    const key = argv[i];
    const value = argv[i + 1];

    if (key === "--rules" && value) {
      args.rules = value;
      i += 1;
    } else if (key === "--target" && value) {
      args.target = value;
      i += 1;
    } else if (key === "--social" && value) {
      args.social = value.toLowerCase() !== "false";
      i += 1;
    } else if (key === "--format" && value) {
      if (value !== "json" && value !== "text") {
        throw new Error("--format must be 'json' or 'text'");
      }
      args.format = value;
      i += 1;
    } else if (key.startsWith("--")) {
      throw new Error(`Unknown option: ${key}`);
    }
  }

  if (!args.rules || !args.target) {
    throw new Error("Missing required options --rules and/or --target");
  }
  return args;
}

function walkFiles(targetPath, out = []) {
  const stat = fs.statSync(targetPath);
  if (stat.isFile()) {
    const ext = path.extname(targetPath).toLowerCase();
    if (TEXT_EXTENSIONS.has(ext)) {
      out.push(path.resolve(targetPath));
    }
    return out;
  }

  const entries = fs.readdirSync(targetPath, { withFileTypes: true });
  for (const entry of entries) {
    if (entry.isDirectory() && SKIP_DIRS.has(entry.name)) {
      continue;
    }
    const fullPath = path.join(targetPath, entry.name);
    if (entry.isDirectory()) {
      walkFiles(fullPath, out);
      continue;
    }
    const ext = path.extname(entry.name).toLowerCase();
    if (TEXT_EXTENSIONS.has(ext)) {
      out.push(path.resolve(fullPath));
    }
  }
  return out;
}

function runAudit(rulesPath, targetPath, isSocial, format) {
  const rules = JSON.parse(fs.readFileSync(rulesPath, "utf-8"));
  const files = walkFiles(targetPath);
  const issues = [];

  for (const file of files) {
    const content = fs.readFileSync(file, "utf-8");
    const lowerContent = content.toLowerCase();

    // Check Restricted Terms
    if (rules.restrictedTerms) {
      for (const term of rules.restrictedTerms) {
        if (term.socialOnly && !isSocial) continue;
        
        const phrase = term.phrase.toLowerCase();
        if (lowerContent.includes(phrase)) {
          // Simple check: find line number
          const lines = content.split("\n");
          lines.forEach((line, idx) => {
            if (line.toLowerCase().includes(phrase)) {
              issues.push({
                file: path.relative(process.cwd(), file),
                line: idx + 1,
                type: "RESTRICTED_TERM",
                message: `Found prohibited term "${term.phrase}". Replacement: "${term.replacement}"`,
                context: line.trim().substring(0, 100)
              });
            }
          });
        }
      }
    }

    // Check Required Phrases (only if not social-specific or logic allows)
    if (rules.requiredPhrases) {
      for (const req of rules.requiredPhrases) {
        if (!lowerContent.includes(req.phrase.toLowerCase())) {
          // Check if this file type is relevant for the required phrase
          // E.g. disclaimer usually in specific files, but for now we warn if MISSING from project?
          // Actually, required phrases are usually "must exist SOMEWHERE". 
          // Checking every file for existence is wrong. 
          // We should check if it exists in AT LEAST ONE file in the target.
        }
      }
    }
  }

  // Global Required Phrase Check
  if (rules.requiredPhrases) {
    for (const req of rules.requiredPhrases) {
      let found = false;
      for (const file of files) {
        const content = fs.readFileSync(file, "utf-8").toLowerCase();
        if (content.includes(req.phrase.toLowerCase())) {
          found = true;
          break;
        }
      }
      if (!found) {
        issues.push({
          file: "PROJECT_WIDE",
          line: 0,
          type: "MISSING_REQUIRED",
          message: `Missing required phrase: "${req.phrase}"`,
          context: req.description
        });
      }
    }
  }

  if (format === "json") {
    console.log(JSON.stringify(issues, null, 2));
  } else {
    if (issues.length === 0) {
      console.log("✅ No compliance issues found.");
    } else {
      console.log(`❌ Found ${issues.length} issues:`);
      issues.forEach(issue => {
        console.log(`\n[${issue.type}] ${issue.file}:${issue.line}`);
        console.log(`   ${issue.message}`);
        if (issue.context) console.log(`   Context: "${issue.context}"`);
      });
      process.exit(1);
    }
  }
}

try {
  const args = parseArgs(process.argv.slice(2));
  runAudit(args.rules, args.target, args.social, args.format);
} catch (err) {
  console.error(`Error: ${err.message}`);
  printUsage();
  process.exit(1);
}

function toLineNumber(text, index) {
  if (index <= 0) {
    return 1;
  }
  return text.slice(0, index).split("\n").length;
}

function findOccurrences(text, phrase) {
  const matches = [];
  const needle = phrase.toLowerCase();
  const haystack = text.toLowerCase();
  let cursor = 0;
  while (cursor < haystack.length) {
    const found = haystack.indexOf(needle, cursor);
    if (found === -1) {
      break;
    }
    matches.push(found);
    cursor = found + needle.length;
  }
  return matches;
}

function renderText(result) {
  const lines = [];
  lines.push(`status: ${result.status}`);
  lines.push(`filesScanned: ${result.summary.filesScanned}`);
  lines.push(`violations: ${result.summary.violationCount}`);
  if (result.violations.length > 0) {
    lines.push("");
    for (const violation of result.violations) {
      const loc = violation.file
        ? `${violation.file}${violation.line ? `:${violation.line}` : ""}`
        : "(global)";
      lines.push(
        `- [${violation.severity}] ${violation.type} @ ${loc}: ${violation.message}`
      );
      if (violation.suggestion) {
        lines.push(`  suggestion: ${violation.suggestion}`);
      }
    }
  }
  return lines.join("\n");
}

function main() {
  let args;
  try {
    args = parseArgs(process.argv.slice(2));
  } catch (error) {
    printUsage();
    console.error(error.message);
    process.exit(2);
  }

  const rulesPath = path.resolve(args.rules);
  const targetPath = path.resolve(args.target);
  if (!fs.existsSync(rulesPath)) {
    console.error(`Rules file not found: ${rulesPath}`);
    process.exit(2);
  }
  if (!fs.existsSync(targetPath)) {
    console.error(`Target path not found: ${targetPath}`);
    process.exit(2);
  }

  const rules = JSON.parse(fs.readFileSync(rulesPath, "utf8"));
  const restrictedTerms = Array.isArray(rules.restrictedTerms)
    ? rules.restrictedTerms
    : [];
  const requiredPhrases = Array.isArray(rules.requiredPhrases)
    ? rules.requiredPhrases
    : [];

  const files = walkFiles(targetPath);
  const violations = [];
  const aggregateText = [];

  for (const file of files) {
    let text = "";
    try {
      text = fs.readFileSync(file, "utf8");
      aggregateText.push(text);
    } catch {
      violations.push({
        type: "read_error",
        severity: "high",
        file,
        message: "Failed to read file as UTF-8 text."
      });
      continue;
    }

    for (const term of restrictedTerms) {
      if (!term || typeof term.phrase !== "string" || term.phrase.length === 0) {
        continue;
      }
      if (term.socialOnly === true && !args.social) {
        continue;
      }
      const foundAt = findOccurrences(text, term.phrase);
      for (const index of foundAt) {
        violations.push({
          type: "restricted_term",
          severity: "high",
          file,
          line: toLineNumber(text, index),
          message: `Found restricted phrase '${term.phrase}'.`,
          suggestion: term.replacement
            ? `Replace with '${term.replacement}'.`
            : undefined
        });
      }
    }
  }

  const allText = aggregateText.join("\n").toLowerCase();
  for (const item of requiredPhrases) {
    if (!item || typeof item.phrase !== "string" || item.phrase.length === 0) {
      continue;
    }
    if (!allText.includes(item.phrase.toLowerCase())) {
      violations.push({
        type: "missing_required_phrase",
        severity: "high",
        message:
          item.description || `Required phrase '${item.phrase}' was not found.`,
        suggestion: `Add phrase '${item.phrase}'.`
      });
    }
  }

  const result = {
    status: violations.length > 0 ? "fail" : "pass",
    violations,
    summary: {
      filesScanned: files.length,
      violationCount: violations.length
    }
  };

  if (args.format === "text") {
    console.log(renderText(result));
  } else {
    console.log(JSON.stringify(result, null, 2));
  }
  process.exit(result.status === "pass" ? 0 : 1);
}

main();
