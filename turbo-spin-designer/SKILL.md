---
name: turbo-spin-designer
description: Define turbo/quick spin behavior, timings, and UI rules for slot games. Invoke when implementing fast spin modes, stop/skip behavior, or spin-speed UX standards.
---

# Turbo Spin Designer

Use this skill to design turbo and quick-spin modes with studio-grade UX, strict timing rules, and safe integration patterns.

## Core Principles

- Turbo must never change math or outcomes, only presentation timing.
- Quick Spin is a moderate speed-up; Turbo is the fastest allowed.
- Stop/Skip behavior must be deterministic and never skip required result events.

## Workflow

1. Define spin speed modes.
- Declare `normal`, `quick`, `turbo` modes with timing targets.
- Define max speed multipliers and minimum durations per state.

2. Define stop/skip behavior.
- Decide if “Stop” advances to final state or fast-forwards step-by-step.
- Ensure stop does not alter payout or event ordering.

3. Map UI state transitions.
- Spin button shows `Spin`, `Stop`, or `Auto Stop` based on state.
- Lock speed toggles during resolve to avoid desync.

4. Validate casino-grade constraints.
- Maintain readability of reels, wins, and feature triggers.
- Cap total round time to avoid illegal 0ms spins.

5. Deliver integration handoff.
- Provide state map, timing tables, and trigger rules.
- Provide spec for QA checks and edge-case handling.

## Output Contract

Return:

1. `Mode Table`: normal/quick/turbo timings and multipliers.
2. `Stop Logic`: allowed states, behavior, and guard rules.
3. `UI Mapping`: button states and toggle availability.
4. `State Safety`: minimum durations per phase.
5. `Verification`: QA checks and pass criteria.
6. `Risks`: ambiguity or desync points.

## Commands

```bash
python3 scripts/validate_turbo_spin_spec.py \
  --input <path/to/turbo_spin_spec.json>
```

Treat non-zero exits as blocker findings.

## References

- `references/workflow.md`: design flow and timing rules.
- `references/contracts.md`: turbo spin spec contract.
- `references/checklist.md`: UX and QA checklist.
- `references/signoff-template.md`: sign-off template.

## Execution Rules

- Never modify outcomes or RNG when turbo is enabled.
- Ensure minimum visual exposure of wins and features.
- Enforce stop button behavior as state-driven, not time-driven.
