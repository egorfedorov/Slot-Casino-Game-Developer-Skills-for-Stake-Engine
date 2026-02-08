---
name: multi-agent-orchestrator
description: Coordinate multi-agent execution plans with explicit dependencies, ownership boundaries, and completion gates. Use when orchestrating multiple autonomous workstreams, sequencing inter-agent tasks, resolving dependency conflicts, or validating end-to-end pipeline readiness.
---

# Multi-Agent Orchestrator

Use this skill to coordinate multi-agent execution with clear sequencing and dependency control.

## Workflow

1. Define scope and constraints.
- Define participating agents, roles, task graph, and shared contracts.
- Capture objective metrics, bounds, and release blockers.

2. Design implementation plan.
- Map agent handoffs, synchronization points, and retry/escalation policy.
- Keep ownership and dependency boundaries explicit.

3. Execute and iterate.
- Implement in small, traceable increments.
- Record run/build context for reproducibility.

4. Validate contract integrity.
- Validate dependency closure, handoff completeness, and terminal states.
- Treat contract breaches as blockers.

5. Prepare handoff.
- Deliver final orchestration map, unresolved dependencies, and runbook actions.
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
- Flag deadlocks, orphan tasks, or circular dependencies as blockers.
