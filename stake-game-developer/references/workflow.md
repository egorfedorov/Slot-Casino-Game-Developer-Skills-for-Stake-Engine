# Stake Game Workflow

## Goal

Ship a Stake game update that is math-sound, RGS-contract-safe, frontend-correct, and compliance-ready.

## Sequence

1. **Define Game Structure**
   - Create `config.yml` with core math rules (RTP, Symbols, Paylines).
   - Define States and Transitions (Idle, Spinning, Resolving).
   - Reference: `https://stake-engine.com/docs/math/high-level-structure/game-structure`

2. **Generate Math Source Files**
   - Create `events.jsonl` (or per-mode books) following the event schema.
   - Validate against `config.yml` constraints.
   - Reference: `https://stake-engine.com/docs/math/source-files/events`

3. **Validate Book/Index Integrity**
   - Run `scripts/validate-books-index.mjs`.
   - Ensure `index.json` links correctly to generated artifacts.

4. **Validate Event Stream**
   - Run `scripts/validate-rgs-events.mjs`.
   - Verify deterministic playback and state machine alignment.

5. **Frontend Integration**

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
