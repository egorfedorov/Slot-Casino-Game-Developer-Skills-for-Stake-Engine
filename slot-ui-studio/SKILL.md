---
name: slot-ui-studio
description: Build scalable slot UI production systems with shared components, state patterns, and release quality controls. Use when structuring slot UI architecture, component libraries, interaction contracts, or validating production UI readiness across titles.
---

# Slot UI Studio

Use this skill to organize slot UI production systems with reusable, governed patterns.

## Workflow

1. Define scope and constraints.
- Define UI surface inventory, component ownership, and style constraints.
- Capture objective metrics, bounds, and release blockers.

2. Design implementation plan.
- Design shared primitives, state contracts, and integration boundaries.
- Keep ownership and dependency boundaries explicit.

3. Execute and iterate.
- Implement in small, traceable increments.
- Record run/build context for reproducibility.

4. Validate contract integrity.
- Validate responsiveness, interaction consistency, and accessibility gates.
- Treat contract breaches as blockers.

5. Prepare handoff.
- Deliver component rollout plan, migration steps, and validation matrix.
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
- Flag inconsistent control semantics and accessibility regressions as blockers.
