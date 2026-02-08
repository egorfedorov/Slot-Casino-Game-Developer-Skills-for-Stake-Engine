---
name: slot-mechanics-designer
description: Design, review, and harden slot feature mechanics from product idea to implementation-ready behavior spec. Use when defining feature triggers, state transitions, retrigger rules, multipliers, respins, bonus entry/exit flow, mechanic sequencing, anti-loop constraints, or pre-implementation mechanic validation.
---

# Slot Mechanics Designer

Use this skill to convert mechanic ideas into deterministic state/trigger/action specs that engineering and math teams can implement safely.

## Workflow

1. Define mechanic scope and constraints.
- Capture core loop, feature list, target experience, and hard constraints (max win, duration caps, retrigger limits).
- Separate product goals from implementation assumptions.

2. Model states and transitions first.
- Define explicit states (`base`, `feature`, `bonus`, `terminal` as needed).
- Define transition events and guard conditions.
- Require deterministic entry and exit paths for each feature.

3. Define trigger and action contracts.
- For each mechanic, specify `triggerEvent`, `entryState`, `targetState`, and actions.
- Keep action payloads explicit (for example spins/multiplier/value).
- Enforce retrigger and cooldown behavior explicitly.

4. Validate graph integrity before implementation.
- Ensure all transitions reference known states.
- Ensure non-terminal states are reachable and have exits.
- Ensure mechanics map to valid transitions.

5. Package handoff spec.
- Deliver state graph, mechanic table, event contract, and known risks.
- Include exact patch plan for implementation files.

## Commands

```bash
python3 scripts/check_mechanics_spec.py \
  --input <path/to/mechanics_spec.json>
```

Treat non-zero exits as blocker findings.

## Output Contract

Return:

1. `Mechanic Map`: states, transitions, mechanics, and action payloads.
2. `Validation Findings`: graph consistency and trigger/action coverage with pass/fail.
3. `Patch Plan`: file-level implementation steps.
4. `Verification`: commands and expected success criteria.
5. `Residual Risks`: unresolved design or implementation blockers.

## References

- `references/workflow.md`: step-by-step mechanics design process.
- `references/mechanics-patterns.md`: proven feature patterns and guardrails.
- `references/signoff-template.md`: final handoff template.

## Execution Rules

- Make state transitions explicit; avoid implicit side effects.
- Cap feature loops and retriggers to prevent runaway rounds.
- Keep mechanics deterministic and replay-friendly.
- Flag any unreachable or non-terminating state as a blocker.
