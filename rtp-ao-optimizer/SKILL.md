---
name: rtp-ao-optimizer
description: Optimize RTP and AO targets under controlled constraints and statistical validation gates. Use when tuning payout structures, feature rates, or mode mixes; evaluating convergence; and preparing sign-off evidence for target compliance.
---

# RTP AO Optimizer

Use this skill to tune RTP/AO targets with bounded changes and statistical validation.

## Workflow

1. Define scope and constraints.
- Define target vector, tolerance bands, and hard safety constraints.
- Capture objective metrics, bounds, and release blockers.

2. Design implementation plan.
- Design lever-adjustment strategy and run-budget policy.
- Keep ownership and dependency boundaries explicit.

3. Execute and iterate.
- Implement in small, traceable increments.
- Record run/build context for reproducibility.

4. Validate contract integrity.
- Validate final metrics, confidence stability, and guardrail compliance.
- Treat contract breaches as blockers.

5. Prepare handoff.
- Deliver final parameter diff, metric table, and sign-off decision.
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
- Flag non-convergence and hard-constraint breaches as blockers.
