---
name: game-math-director
description: Direct game-math strategy, target setting, and validation governance across game modes. Use when aligning RTP/volatility goals, defining math sign-off criteria, reviewing simulation evidence, or coordinating math decisions across teams.
---

# Game Math Director

Use this skill to direct game-math decisions with clear targets and validation governance.

## Workflow

1. Define scope and constraints.
- Define math targets per mode and global risk constraints.
- Capture objective metrics, bounds, and release blockers.

2. Design implementation plan.
- Design review cadence for model, simulation, and artifact evidence.
- Keep ownership and dependency boundaries explicit.

3. Execute and iterate.
- Implement in small, traceable increments.
- Record run/build context for reproducibility.

4. Validate contract integrity.
- Validate target adherence, drift explanations, and sign-off readiness.
- Treat contract breaches as blockers.

5. Prepare handoff.
- Deliver decision log, action plan, and unresolved risk items.
- Include exact commands and acceptance criteria.

## Output Contract

Return:

1. `Context`: goals, assumptions, constraints.
2. `Validation`: pass/fail checks and key deltas.
3. `Changes`: concrete file-level updates.
4. `Commands`: commands and expected outputs.
5. `Risks`: unresolved issues and limits.

## References

- `references/workflow.md`: detailed execution flow.
- `references/checklist.md`: sign-off checklist.

## Execution Rules

- Keep decisions measurable and reversible.
- Keep validation criteria explicit before iteration.
- Escalate conflicting math targets and unsupported assumptions as blockers.
