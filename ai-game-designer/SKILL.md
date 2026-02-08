---
name: ai-game-designer
description: Design and validate AI-assisted game design specifications from concept to implementation handoff. Use when defining core loops, progression systems, economy sinks/sources, feature specs, risk constraints, content generation hooks, or quality gates for translating design docs into engineering-ready contracts.
---

# AI Game Designer

Use this skill to produce coherent, constraint-aware game design specs with explicit implementation contracts.

## Workflow

1. Define game vision and constraints.
- Capture target audience, session length, progression horizon, and platform constraints.
- Document hard constraints (economy limits, fairness goals, compliance limitations).

2. Model loops and systems.
- Define core loop, meta loop, and retention loop with explicit input/output resources.
- Define feature dependencies and unlock conditions.

3. Define economy and progression contract.
- Define sources/sinks and progression pacing targets.
- Prevent degenerate loops by constraining exploit paths.
- Declare telemetry signals needed to validate assumptions.

4. Validate design spec integrity.
- Check required sections and referenced features.
- Check consistency between loops, progression, and economy definitions.
- Treat missing constraints or contradictory rules as blockers.

5. Prepare engineering handoff.
- Provide design-to-implementation mapping and patch plan targets.
- Include measurable acceptance criteria.

## Commands

```bash
python3 scripts/validate_game_design_spec.py \
  --input <path/to/game_design_spec.json>
```

Treat non-zero exits as blocker findings.

## Output Contract

Return:

1. `Design Map`: loops, systems, features, and constraints.
2. `Validation Findings`: pass/fail with concrete inconsistencies.
3. `Patch Plan`: docs/files that must change before implementation.
4. `Verification`: command outputs and acceptance criteria.
5. `Residual Risks`: unresolved economy or progression risks.

## References

- `references/workflow.md`: design-to-handoff process.
- `references/design-rules.md`: loop/economy/progression guardrails.
- `references/signoff-template.md`: release handoff template.

## Execution Rules

- Keep design constraints explicit and measurable.
- Keep loop/economy dependencies internally consistent.
- Flag exploitable or contradictory progression paths as blockers.
- Require telemetry hooks for key balance assumptions.
