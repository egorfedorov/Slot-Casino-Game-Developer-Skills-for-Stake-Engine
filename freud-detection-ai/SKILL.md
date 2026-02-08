---
name: freud-detection-ai
description: Design and validate AI-driven anomaly/fraud-style detection workflows for game operations. Use when defining signal features, model scoring thresholds, investigation routing, or validating detection pipeline reliability and false-positive controls.
---

# Freud Detection AI

Use this skill to implement anomaly-detection workflows with explainable gating and review paths.

## Workflow

1. Define scope and constraints.
- Define detection scope, signals, threshold policy, and review SLA.
- Capture objective metrics, bounds, and release blockers.

2. Design implementation plan.
- Design model-scoring flow, fallback heuristics, and escalation rules.
- Keep ownership and dependency boundaries explicit.

3. Execute and iterate.
- Implement in small, traceable increments.
- Record run/build context for reproducibility.

4. Validate contract integrity.
- Validate threshold outcomes, alert quality, and investigation traceability.
- Treat contract breaches as blockers.

5. Prepare handoff.
- Deliver detector configuration diff, alert routing updates, and runbook.
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
- Escalate unbounded false-positive risk and opaque scoring logic as blockers.
