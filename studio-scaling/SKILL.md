---
name: studio-scaling
description: Scale game studio delivery systems across teams, pipelines, and release cadences. Use when designing team topology changes, pipeline throughput improvements, cross-team dependency governance, or operational maturity gates for scaling production.
---

# Studio Scaling

Use this skill to scale studio workflows with predictable throughput and quality gates.

## Workflow

1. Define scope and constraints.
- Define scaling objective, current bottlenecks, and throughput targets.
- Capture objective metrics, bounds, and release blockers.

2. Design implementation plan.
- Design team/process topology changes and ownership interfaces.
- Keep ownership and dependency boundaries explicit.

3. Execute and iterate.
- Implement in small, traceable increments.
- Record run/build context for reproducibility.

4. Validate contract integrity.
- Validate throughput, handoff latency, and quality gate impact.
- Treat contract breaches as blockers.

5. Prepare handoff.
- Deliver rollout plan, risk controls, and measurable success criteria.
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
- Escalate ambiguous ownership and unmanaged cross-team dependencies as blockers.
