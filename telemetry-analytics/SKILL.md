---
name: telemetry-analytics
description: Design telemetry and analytics systems for reliable KPI tracking and decision support. Use when defining event schemas, metric derivations, analytics pipelines, anomaly checks, or validating telemetry coverage for product releases.
---

# Telemetry Analytics

Use this skill to define telemetry pipelines and analytics outputs with KPI trustworthiness.

## Workflow

1. Define scope and constraints.
- Define KPI questions, event taxonomy, and data quality constraints.
- Capture objective metrics, bounds, and release blockers.

2. Design implementation plan.
- Design ingestion, transformation, and aggregation flow with lineage.
- Keep ownership and dependency boundaries explicit.

3. Execute and iterate.
- Implement in small, traceable increments.
- Record run/build context for reproducibility.

4. Validate contract integrity.
- Validate event completeness, metric accuracy, and anomaly detection gates.
- Treat contract breaches as blockers.

5. Prepare handoff.
- Deliver schema updates, dashboard mapping, and quality checks.
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
- Flag missing instrumentation and unverifiable KPI derivations as blockers.
