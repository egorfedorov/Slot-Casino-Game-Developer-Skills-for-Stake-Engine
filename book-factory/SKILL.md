---
name: book-factory
description: Generate and validate high-volume game book artifacts with repeatable packaging and integrity checks. Use when producing books/index assets at scale, managing generation throughput, or validating artifact consistency before deployment.
---

# Book Factory

Use this skill to produce large-scale book artifacts with deterministic integrity controls.

## Workflow

1. Define scope and constraints.
- Define output formats, indexing rules, and generation quotas.
- Capture objective metrics, bounds, and release blockers.

2. Design implementation plan.
- Design generation pipeline steps and storage/layout conventions.
- Keep ownership and dependency boundaries explicit.

3. Execute and iterate.
- Implement in small, traceable increments.
- Record run/build context for reproducibility.

4. Validate contract integrity.
- Validate artifact completeness, ID integrity, and index consistency.
- Treat contract breaches as blockers.

5. Prepare handoff.
- Deliver package manifest, failure report, and remediation plan.
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
- Treat missing artifacts and reference mismatches as blockers.
