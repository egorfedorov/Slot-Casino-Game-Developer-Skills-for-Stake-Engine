# Stake Game Workflow

## Goal

Ship a Stake game update that is math-sound, RGS-contract-safe, frontend-correct, and compliance-ready.

## Sequence

1. Capture brief and constraints
- Game identity, core mechanics, and mode list.
- RTP targets, max win, and volatility intent.
- Any jurisdiction-specific launch requirements.

2. Validate books and index metadata
- Run `scripts/validate-books-index.mjs` against generated `index.json`.
- Block on missing referenced files, malformed mode metadata, or invalid RTP ranges.

3. Validate RGS event contract
- Run `scripts/validate-rgs-events.mjs` on sample JSON/JSONL streams.
- Block on ordering errors (missing `spinStart`, missing `roundResult`, invalid post-result events).

4. Validate frontend contract assumptions
- Confirm event-driven playback only.
- Confirm win display and multipliers are read from events.
- Confirm button/animation synchronization with `roundResult` completion.

5. Run compliance gate
- Run `scripts/audit-checklist.mjs` using `references/compliance-rules.json`.
- Treat violations as release blockers.

6. Produce release summary
- Include pass/fail per gate.
- Include precise findings with file and line when available.

## Release Gate Policy

All gates must pass before release recommendation:
- Books/index validation
- Event stream contract validation
- Compliance audit

If any gate fails, stop and return actionable findings rather than partial approval.
