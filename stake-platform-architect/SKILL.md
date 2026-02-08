---
name: stake-platform-architect
description: Architect Stake platform integration layers across services, contracts, and release workflows. Use when defining platform boundaries, service contracts, compliance-aware architecture decisions, or validating integration readiness for Stake-aligned systems.
---

# Stake Platform Architect

Use this skill to design Stake platform architecture with explicit contract and governance boundaries.

## Workflow

1. Define scope and constraints.
- Define domain boundaries, contracts, and platform capability map.
- Capture objective metrics, bounds, and release blockers.

2. Design implementation plan.
- Design integration topology, failure domains, and policy controls.
- Keep ownership and dependency boundaries explicit.

3. Execute and iterate.
- Implement in small, traceable increments.
- Record run/build context for reproducibility.

4. Validate contract integrity.
- Validate contract alignment, dependency safety, and rollout feasibility.
- Treat contract breaches as blockers.

5. Prepare handoff.
- Deliver architecture decision set, migration plan, and gate checklist.
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
- Treat unresolved contract ownership and compliance gaps as blockers.
