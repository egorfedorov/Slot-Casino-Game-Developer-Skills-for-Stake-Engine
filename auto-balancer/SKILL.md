---
name: auto-balancer
description: Automatically tune game/system parameters toward target metrics under explicit constraints. Use when iterating configuration weights, payout tables, trigger rates, or other balancing levers; running balance loops against simulation outputs; validating tolerance gates; and preparing pass/fail balancing sign-off artifacts.
---

# Auto Balancer

Use this skill to run controlled parameter tuning loops with deterministic validation gates.

## Workflow

1. Define balancing contract.
- Declare target metrics, tolerances, hard constraints, and stop conditions.
- Declare which parameters are allowed to move and their bounds.

2. Establish baseline and iteration plan.
- Record baseline metrics before tuning.
- Apply small, traceable parameter changes per iteration.
- Track config hash/version for each run.

3. Run balance loop.
- Execute simulation/evaluation runs.
- Compare observed metrics to targets and compute deltas.
- Keep only changes that improve objective without violating hard constraints.

4. Validate gate conditions.
- Check each metric against tolerance range.
- Fail immediately on hard-constraint breaches.
- Require minimum run count before final pass.

5. Prepare sign-off handoff.
- Return final parameter set, metric table, and failed/passed gates.
- Include patch plan and exact verification commands.

## Commands

```bash
python3 scripts/validate_balance_runs.py \
  --input <path/to/balance_runs.json> \
  --spec <path/to/target_spec.json>
```

Treat non-zero exits as blocker results.

## Output Contract

Return:

1. `Target Contract`: metrics, tolerances, and constraints.
2. `Run Summary`: baseline, best run, and final run deltas.
3. `Gate Results`: pass/fail per metric and per hard constraint.
4. `Patch Plan`: exact files/params to update.
5. `Residual Risks`: unresolved drift or instability concerns.

## References

- `references/workflow.md`: balancing process and iteration order.
- `references/metric-rules.md`: tolerance and hard-constraint rules.
- `references/signoff-template.md`: balancing sign-off template.

## Execution Rules

- Keep balancing changes bounded and reversible.
- Keep hard constraints non-negotiable.
- Keep baseline comparison in every report.
- Flag non-convergent loops as blockers.
