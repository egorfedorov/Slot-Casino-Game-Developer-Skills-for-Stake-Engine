#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const ALLOWED_EVENT_TYPES = new Set([
  "spinstart",
  "reveal",
  "wininfo",
  "setwin",
  "settotalwin",
  "finalwin",
  "multiplierupdate",
  "updateglobalmult",
  "bonustrigger",
  "freespintrigger",
  "freespinretrigger",
  "enterbonus",
  "updatefreespin",
  "freespinend",
  "stickyzones",
  "newstickysymbols",
  "bonuspick",
  "roundresult"
]);

const ROUND_INDEX_TYPES = new Set([
  "reveal",
  "wininfo",
  "multiplierupdate",
  "updateglobalmult"
]);

function printUsage() {
  console.error(
    "Usage: node scripts/validate-rgs-events.mjs --input <json|jsonl> [--format json|text]"
  );
}

function parseArgs(argv) {
  const args = {
    input: "",
    format: "json"
  };
  for (let i = 0; i < argv.length; i += 1) {
    const key = argv[i];
    const value = argv[i + 1];
    if (key === "--input" && value) {
      args.input = value;
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
  if (!args.input) {
    throw new Error("Missing required option --input");
  }
  return args;
}

function normalizeType(type) {
  return String(type ?? "")
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]/g, "");
}

function toInteger(value) {
  if (typeof value === "number" && Number.isFinite(value) && Number.isInteger(value)) {
    return value;
  }
  if (typeof value === "string" && value.trim() !== "") {
    const parsed = Number(value);
    if (Number.isFinite(parsed) && Number.isInteger(parsed)) {
      return parsed;
    }
  }
  return null;
}

function toNumber(value) {
  if (typeof value === "number" && Number.isFinite(value)) {
    return value;
  }
  if (typeof value === "string" && value.trim() !== "") {
    const parsed = Number(value);
    if (Number.isFinite(parsed)) {
      return parsed;
    }
  }
  return null;
}

function readWinInfoTotal(event) {
  const totalWin = toInteger(event?.totalWin ?? event?.total_win);
  const payout = toInteger(event?.payout);
  let winsSum = null;

  if (Array.isArray(event?.wins)) {
    winsSum = event.wins.reduce((sum, win) => {
      const value = toInteger(win?.win ?? win?.payout);
      return sum + (value ?? 0);
    }, 0);
  }

  const total = totalWin ?? payout ?? winsSum ?? null;
  return { total, totalWin, payout, winsSum };
}

function readTerminalTotal(event) {
  const type = normalizeType(event?.type);
  if (type === "finalwin") {
    return toInteger(event?.amount);
  }
  if (type === "roundresult") {
    return toInteger(event?.totalPayout ?? event?.total_win ?? event?.total);
  }
  return null;
}

function normalizeRoundObject(item, fallbackId) {
  if (Array.isArray(item)) {
    return { id: fallbackId, events: item };
  }
  if (!item || typeof item !== "object") {
    return null;
  }
  if (Array.isArray(item.events)) {
    return { id: item.id ?? fallbackId, events: item.events };
  }
  if (item.round && Array.isArray(item.round.events)) {
    return { id: item.round.id ?? item.id ?? fallbackId, events: item.round.events };
  }
  if (typeof item.type === "string") {
    return { id: fallbackId, events: [item] };
  }
  return null;
}

function parseJsonInput(text) {
  const raw = JSON.parse(text);

  if (Array.isArray(raw)) {
    if (raw.length === 0) {
      return [];
    }
    if (raw.every((item) => item && typeof item.type === "string")) {
      return [{ id: 0, events: raw }];
    }
    const rounds = [];
    raw.forEach((item, idx) => {
      const normalized = normalizeRoundObject(item, idx);
      if (normalized) {
        rounds.push(normalized);
      }
    });
    return rounds;
  }

  if (raw && typeof raw === "object") {
    if (Array.isArray(raw.events)) {
      return [{ id: raw.id ?? 0, events: raw.events }];
    }
    if (Array.isArray(raw.rounds)) {
      return raw.rounds
        .map((round, idx) => normalizeRoundObject(round, idx))
        .filter(Boolean);
    }
    if (Array.isArray(raw.data)) {
      return raw.data
        .map((round, idx) => normalizeRoundObject(round, idx))
        .filter(Boolean);
    }
  }

  return [];
}

function parseJsonlInput(text) {
  const lines = text
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean);

  if (lines.length === 0) {
    return [];
  }

  const parsed = lines.map((line, idx) => {
    try {
      return JSON.parse(line);
    } catch (error) {
      throw new Error(`Invalid JSONL line ${idx + 1}: ${error.message}`);
    }
  });

  if (parsed.every((item) => item && typeof item.type === "string")) {
    return [{ id: 0, events: parsed }];
  }

  return parsed
    .map((item, idx) => normalizeRoundObject(item, idx))
    .filter(Boolean);
}

function parseRounds(filePath, text) {
  const ext = path.extname(filePath).toLowerCase();

  if (ext === ".jsonl") {
    return parseJsonlInput(text);
  }

  try {
    return parseJsonInput(text);
  } catch {
    return parseJsonlInput(text);
  }
}

function pushError(errors, roundId, eventIndex, code, message) {
  errors.push({ roundId, eventIndex, code, message });
}

function pushWarning(warnings, roundId, eventIndex, code, message) {
  warnings.push({ roundId, eventIndex, code, message });
}

function validateRound(round, errors, warnings) {
  const roundId = round.id ?? null;
  const events = Array.isArray(round.events) ? round.events : null;
  if (!events || events.length === 0) {
    pushError(errors, roundId, null, "empty_round", "Round has no events.");
    return;
  }

  const normalizedTypes = events.map((event) => normalizeType(event?.type));

  const hasAnyIndex = events.some((event) => Object.prototype.hasOwnProperty.call(event ?? {}, "index"));
  if (hasAnyIndex) {
    events.forEach((event, index) => {
      const eventIndex = toInteger(event?.index);
      if (eventIndex === null || eventIndex !== index) {
        pushError(
          errors,
          roundId,
          index,
          "non_contiguous_index",
          "event.index must be contiguous and start from 0."
        );
      }
    });
  }

  let revealCount = 0;
  let lastRoundIndex = -Infinity;
  let winInfoSum = 0;

  normalizedTypes.forEach((type, index) => {
    const event = events[index];
    if (!type) {
      pushError(errors, roundId, index, "invalid_event", "Event type is missing.");
      return;
    }

    if (!ALLOWED_EVENT_TYPES.has(type)) {
      pushWarning(
        warnings,
        roundId,
        index,
        "unknown_event_type",
        `Unknown event type '${event?.type}'.`
      );
    }

    if (type === "reveal") {
      revealCount += 1;
    }

    if (ROUND_INDEX_TYPES.has(type)) {
      const roundIndex = toInteger(event?.roundIndex ?? event?.round_index);
      if (roundIndex !== null) {
        if (roundIndex < lastRoundIndex) {
          pushError(
            errors,
            roundId,
            index,
            "non_monotonic_round_index",
            "roundIndex must be non-decreasing."
          );
        }
        lastRoundIndex = Math.max(lastRoundIndex, roundIndex);
      }
    }

    if (type === "wininfo") {
      const totals = readWinInfoTotal(event);
      if (totals.total === null) {
        pushError(
          errors,
          roundId,
          index,
          "missing_win_fields",
          "winInfo must contain totalWin/payout/wins[]."
        );
      } else if (totals.total < 0) {
        pushError(
          errors,
          roundId,
          index,
          "negative_win_total",
          "winInfo total must be >= 0."
        );
      } else {
        winInfoSum += totals.total;
      }

      if (totals.totalWin !== null && totals.winsSum !== null && totals.totalWin !== totals.winsSum) {
        pushWarning(
          warnings,
          roundId,
          index,
          "wininfo_total_mismatch",
          "winInfo.totalWin does not match sum(wins[].win)."
        );
      }

      const payout = toNumber(event?.payout);
      const basePayout = toNumber(event?.basePayout ?? event?.base_payout);
      const appliedMultiplier = toNumber(event?.appliedMultiplier ?? event?.applied_multiplier);
      if (payout !== null && basePayout !== null && appliedMultiplier !== null) {
        const expected = (basePayout * appliedMultiplier) / 100;
        if (Math.abs(expected - payout) > 1e-6) {
          pushError(
            errors,
            roundId,
            index,
            "inconsistent_payout",
            `winInfo payout mismatch. expected=${expected}, got=${payout}`
          );
        }
      }
    }
  });

  if (revealCount === 0) {
    pushError(
      errors,
      roundId,
      null,
      "missing_reveal",
      "Round must include at least one 'reveal' event."
    );
  }

  const spinStartIndex = normalizedTypes.indexOf("spinstart");
  if (spinStartIndex > 0) {
    pushError(
      errors,
      roundId,
      spinStartIndex,
      "spin_start_not_first",
      "If present, 'spinStart' must be the first event."
    );
  }

  const finalWinIndices = [];
  const roundResultIndices = [];
  const setTotalWinIndices = [];
  const setWinIndices = [];
  const fsTriggerIndices = [];
  let hasEnterBonus = false;
  let hasFreeSpinEnd = false;
  let hasUpdateFreeSpin = false;

  normalizedTypes.forEach((type, index) => {
    if (type === "finalwin") finalWinIndices.push(index);
    if (type === "roundresult") roundResultIndices.push(index);
    if (type === "settotalwin") setTotalWinIndices.push(index);
    if (type === "setwin") setWinIndices.push(index);
    if (type === "freespintrigger" || type === "freespinretrigger") fsTriggerIndices.push(index);
    if (type === "enterbonus") hasEnterBonus = true;
    if (type === "freespinend") hasFreeSpinEnd = true;
    if (type === "updatefreespin") hasUpdateFreeSpin = true;
  });

  if (finalWinIndices.length > 1) {
    pushError(
      errors,
      roundId,
      null,
      "multiple_final_win",
      "Round contains multiple 'finalWin' events."
    );
  }

  if (roundResultIndices.length > 1) {
    pushError(
      errors,
      roundId,
      null,
      "multiple_round_result",
      "Round contains multiple 'roundResult' events."
    );
  }

  const terminalCandidates = [...finalWinIndices, ...roundResultIndices].sort((a, b) => a - b);
  if (terminalCandidates.length === 0) {
    pushError(
      errors,
      roundId,
      null,
      "missing_terminal_event",
      "Round must contain terminal 'finalWin' (canonical) or 'roundResult' (legacy)."
    );
    return;
  }

  const terminalIndex = terminalCandidates[terminalCandidates.length - 1];
  if (terminalIndex !== events.length - 1) {
    pushError(
      errors,
      roundId,
      terminalIndex,
      "event_after_terminal",
      "No events may appear after the terminal event."
    );
  }

  if (finalWinIndices.length > 0 && roundResultIndices.length > 0) {
    pushWarning(
      warnings,
      roundId,
      null,
      "mixed_terminal_types",
      "Both finalWin and roundResult are present; prefer finalWin-only canonical stream."
    );
  }

  const terminalEvent = events[terminalIndex];
  const terminalType = normalizedTypes[terminalIndex];
  const terminalTotal = readTerminalTotal(terminalEvent);
  if (terminalTotal === null || terminalTotal < 0) {
    pushError(
      errors,
      roundId,
      terminalIndex,
      "missing_terminal_total",
      `${terminalEvent?.type} has no valid total amount.`
    );
  }

  if (setTotalWinIndices.length === 0) {
    pushError(
      errors,
      roundId,
      null,
      "missing_set_total_win",
      "Round must include at least one 'setTotalWin' event."
    );
  } else {
    const lastSetTotalWinIndex = setTotalWinIndices[setTotalWinIndices.length - 1];
    if (lastSetTotalWinIndex > terminalIndex) {
      pushError(
        errors,
        roundId,
        lastSetTotalWinIndex,
        "set_total_after_terminal",
        "setTotalWin must occur before terminal event."
      );
    }

    const lastSetTotalAmount = toInteger(events[lastSetTotalWinIndex]?.amount);
    if (lastSetTotalAmount === null || lastSetTotalAmount < 0) {
      pushError(
        errors,
        roundId,
        lastSetTotalWinIndex,
        "invalid_set_total_amount",
        "setTotalWin.amount must be integer >= 0."
      );
    } else if (terminalTotal !== null && lastSetTotalAmount !== terminalTotal) {
      pushError(
        errors,
        roundId,
        lastSetTotalWinIndex,
        "set_total_terminal_mismatch",
        "Final setTotalWin.amount must equal terminal total amount."
      );
    }
  }

  if (terminalType === "finalwin") {
    setWinIndices.forEach((index) => {
      if (index > terminalIndex) {
        pushError(
          errors,
          roundId,
          index,
          "set_win_after_final",
          "setWin must occur before finalWin."
        );
      }
    });

    if (terminalTotal !== null && terminalTotal > 0 && setWinIndices.length === 0) {
      pushWarning(
        warnings,
        roundId,
        null,
        "missing_set_win_positive_payout",
        "Positive terminal payout without any setWin events."
      );
    }
  }

  const topLevelPayoutMultiplier = toInteger(round?.payoutMultiplier);
  if (topLevelPayoutMultiplier !== null && terminalTotal !== null && topLevelPayoutMultiplier !== terminalTotal) {
    pushError(
      errors,
      roundId,
      null,
      "payout_multiplier_mismatch",
      "Top-level payoutMultiplier does not match terminal total amount."
    );
  }

  const bonusPickEvent = events.find((event) => normalizeType(event?.type) === "bonuspick");
  if (bonusPickEvent) {
    const bonusPickPayout = toInteger(bonusPickEvent?.payout);
    if (bonusPickPayout === null || bonusPickPayout < 0) {
      pushError(
        errors,
        roundId,
        null,
        "invalid_bonuspick_payout",
        "bonusPick.payout must be integer >= 0."
      );
    } else if (terminalTotal !== null && bonusPickPayout !== terminalTotal) {
      pushError(
        errors,
        roundId,
        null,
        "bonuspick_terminal_mismatch",
        "bonusPick.payout must equal terminal total amount."
      );
    }
  } else if (terminalTotal !== null && winInfoSum !== terminalTotal) {
    pushError(
      errors,
      roundId,
      null,
      "sum_wininfo_terminal_mismatch",
      "sum(winInfo totals) must equal terminal total amount."
    );
  }

  const hasFreeSpinReveal = events.some((event) => {
    if (normalizeType(event?.type) !== "reveal") {
      return false;
    }
    const revealType = normalizeType(event?.revealType ?? event?.reveal_type);
    const gameType = normalizeType(event?.gameType ?? event?.game_type);
    return revealType === "freespin" || gameType === "freegame";
  });

  const hasFreeSpinContext = hasUpdateFreeSpin || hasFreeSpinEnd || hasFreeSpinReveal;

  if (fsTriggerIndices.length > 0 && !hasEnterBonus) {
    pushWarning(
      warnings,
      roundId,
      null,
      "missing_enter_bonus",
      "freeSpinTrigger present without enterBonus event."
    );
  }

  if (fsTriggerIndices.length > 0 && hasFreeSpinContext && !hasFreeSpinReveal) {
    pushWarning(
      warnings,
      roundId,
      null,
      "missing_freespin_reveal",
      "freeSpinTrigger present without free-spin reveal events."
    );
  }

  if (hasUpdateFreeSpin && fsTriggerIndices.length === 0) {
    pushWarning(
      warnings,
      roundId,
      null,
      "update_freespin_without_trigger",
      "updateFreeSpin present without freeSpinTrigger/freeSpinRetrigger."
    );
  }

  if (fsTriggerIndices.length > 0 && hasFreeSpinContext && !hasFreeSpinEnd) {
    pushWarning(
      warnings,
      roundId,
      null,
      "missing_freespin_end",
      "freeSpinTrigger present without freeSpinEnd."
    );
  }
}

function renderText(result) {
  const lines = [];
  lines.push(`status: ${result.status}`);
  lines.push(`roundsChecked: ${result.roundsChecked}`);
  lines.push(`errors: ${result.errors.length}`);
  lines.push(`warnings: ${result.warnings.length}`);
  if (result.errors.length > 0) {
    lines.push("");
    lines.push("Error details:");
    for (const err of result.errors) {
      lines.push(
        `- [${err.code}] round=${err.roundId ?? "?"} event=${err.eventIndex ?? "-"}: ${err.message}`
      );
    }
  }
  if (result.warnings.length > 0) {
    lines.push("");
    lines.push("Warning details:");
    for (const warn of result.warnings) {
      lines.push(
        `- [${warn.code}] round=${warn.roundId ?? "?"} event=${warn.eventIndex ?? "-"}: ${warn.message}`
      );
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

  const inputPath = path.resolve(args.input);
  if (!fs.existsSync(inputPath)) {
    console.error(`Input file not found: ${inputPath}`);
    process.exit(2);
  }

  const text = fs.readFileSync(inputPath, "utf8");
  let rounds;
  try {
    rounds = parseRounds(inputPath, text);
  } catch (error) {
    console.error(error.message);
    process.exit(2);
  }

  const errors = [];
  const warnings = [];
  if (!Array.isArray(rounds) || rounds.length === 0) {
    errors.push({
      roundId: null,
      eventIndex: null,
      code: "no_rounds",
      message: "No rounds could be parsed from input."
    });
  } else {
    rounds.forEach((round) => validateRound(round, errors, warnings));
  }

  const result = {
    status: errors.length > 0 ? "fail" : "pass",
    roundsChecked: Array.isArray(rounds) ? rounds.length : 0,
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
