#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const PATH_KEYS = [
  "book",
  "bookFile",
  "bookPath",
  "book_file",
  "jsonl",
  "jsonlPath",
  "lut",
  "lutFile",
  "lutPath",
  "lut_file"
];

const RTP_KEYS = ["rtp", "rtpPct", "rtp_percent", "targetRtp"];
const COUNT_KEYS = ["count", "rounds", "totalRounds", "total_rounds", "totalWeight"];

function printUsage() {
  console.error(
    "Usage: node scripts/validate-books-index.mjs --index <index.json> [--base-dir <dir>] [--format json|text]"
  );
}

function parseArgs(argv) {
  const args = {
    index: "",
    baseDir: "",
    format: "json"
  };

  for (let i = 0; i < argv.length; i += 1) {
    const key = argv[i];
    const value = argv[i + 1];
    if (key === "--index" && value) {
      args.index = value;
      i += 1;
    } else if (key === "--base-dir" && value) {
      args.baseDir = value;
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

  if (!args.index) {
    throw new Error("Missing required option --index");
  }
  return args;
}

function asNumber(value) {
  return typeof value === "number" && Number.isFinite(value) ? value : null;
}

function extractModes(index) {
  if (Array.isArray(index)) {
    return index.map((entry, idx) => ({
      name: entry?.name ?? entry?.mode ?? `mode_${idx}`,
      entry
    }));
  }
  if (!index || typeof index !== "object") {
    return [];
  }
  if (Array.isArray(index.modes)) {
    return index.modes.map((entry, idx) => ({
      name: entry?.name ?? entry?.mode ?? `mode_${idx}`,
      entry
    }));
  }
  if (index.books && typeof index.books === "object") {
    if (Array.isArray(index.books)) {
      return index.books.map((entry, idx) => ({
        name: entry?.name ?? entry?.mode ?? `mode_${idx}`,
        entry
      }));
    }
    return Object.entries(index.books).map(([name, entry]) => ({ name, entry }));
  }
  return [];
}

function pushError(errors, mode, code, message) {
  errors.push({ mode, code, message });
}

function pushWarning(warnings, mode, code, message) {
  warnings.push({ mode, code, message });
}

function validateMode(modeName, entry, baseDir, errors, warnings) {
  if (!entry || typeof entry !== "object") {
    pushError(errors, modeName, "invalid_mode", "Mode entry is missing or invalid.");
    return;
  }

  let fileRefCount = 0;
  for (const key of PATH_KEYS) {
    const value = entry[key];
    if (typeof value === "string" && value.trim().length > 0) {
      fileRefCount += 1;
      const absolutePath = path.isAbsolute(value)
        ? value
        : path.resolve(baseDir, value);
      if (!fs.existsSync(absolutePath)) {
        pushError(
          errors,
          modeName,
          "missing_file",
          `Referenced file for '${key}' does not exist: ${absolutePath}`
        );
      }
    }
  }
  if (fileRefCount === 0) {
    pushWarning(
      warnings,
      modeName,
      "no_file_refs",
      "No known file reference keys were found."
    );
  }

  for (const key of RTP_KEYS) {
    if (Object.prototype.hasOwnProperty.call(entry, key)) {
      const value = asNumber(entry[key]);
      if (value === null) {
        pushError(errors, modeName, "invalid_rtp", `'${key}' must be numeric.`);
      } else if (value < 0 || value > 200) {
        pushError(
          errors,
          modeName,
          "rtp_out_of_range",
          `'${key}' must be between 0 and 200. got=${value}`
        );
      }
    }
  }

  for (const key of COUNT_KEYS) {
    if (Object.prototype.hasOwnProperty.call(entry, key)) {
      const value = asNumber(entry[key]);
      if (value === null) {
        pushError(errors, modeName, "invalid_count", `'${key}' must be numeric.`);
      } else if (value < 0) {
        pushError(
          errors,
          modeName,
          "negative_count",
          `'${key}' cannot be negative. got=${value}`
        );
      }
    }
  }
}

function renderText(result) {
  const lines = [];
  lines.push(`status: ${result.status}`);
  lines.push(`modesChecked: ${result.modesChecked}`);
  lines.push(`errors: ${result.errors.length}`);
  lines.push(`warnings: ${result.warnings.length}`);
  if (result.errors.length > 0) {
    lines.push("");
    lines.push("Error details:");
    for (const err of result.errors) {
      lines.push(`- [${err.code}] mode=${err.mode}: ${err.message}`);
    }
  }
  if (result.warnings.length > 0) {
    lines.push("");
    lines.push("Warning details:");
    for (const warn of result.warnings) {
      lines.push(`- [${warn.code}] mode=${warn.mode}: ${warn.message}`);
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

  const indexPath = path.resolve(args.index);
  if (!fs.existsSync(indexPath)) {
    console.error(`Index file not found: ${indexPath}`);
    process.exit(2);
  }

  const baseDir = args.baseDir
    ? path.resolve(args.baseDir)
    : path.dirname(indexPath);

  let indexData;
  try {
    indexData = JSON.parse(fs.readFileSync(indexPath, "utf8"));
  } catch (error) {
    console.error(`Failed to parse index JSON: ${error.message}`);
    process.exit(2);
  }

  const modes = extractModes(indexData);
  const errors = [];
  const warnings = [];

  if (modes.length === 0) {
    errors.push({
      mode: null,
      code: "no_modes",
      message:
        "No modes found in index. Expected index.modes[] or index.books{} structure."
    });
  } else {
    for (const mode of modes) {
      validateMode(mode.name, mode.entry, baseDir, errors, warnings);
    }
  }

  const result = {
    status: errors.length > 0 ? "fail" : "pass",
    modesChecked: modes.length,
    errors,
    warnings
  };

  if (args.format === "text") {
    console.log(renderText(result));
  } else {
    console.log(JSON.stringify(result, null, 2));
  }
  process.exit(result.status === "pass" ? 0 : 1);
}

main();
