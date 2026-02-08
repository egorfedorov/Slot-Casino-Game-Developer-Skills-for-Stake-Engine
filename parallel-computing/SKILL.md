---
name: parallel-computing
description: Design, optimize, and validate parallel execution across CPU threads/workers with measurable scaling evidence. Use when selecting parallelization strategy, diagnosing contention and load imbalance, evaluating speedup/efficiency curves, tuning task granularity, or triaging baseline-vs-current parallel performance regressions.
---

# Parallel Computing

Use this skill to convert parallel performance work into reproducible scaling decisions.

## Workflow

1. Define scaling objective and constraints.
- Capture workload shape, data size, and latency/throughput targets.
- Define hardware assumptions (core count, SMT policy, NUMA context).

2. Choose parallel model and partitioning.
- Select task/data/pipeline parallelism intentionally.
- Set chunk size and scheduling strategy to minimize overhead and imbalance.
- Define shared-state boundaries before coding.

3. Diagnose bottlenecks.
- Check lock contention, false sharing, synchronization frequency, and memory bandwidth pressure.
- Separate algorithmic limits from runtime/scheduler overhead.

4. Validate scaling behavior.
- Compare baseline vs current throughput by thread count.
- Evaluate parallel efficiency and regressions at each thread level.
- Treat regressions above threshold as blockers.

5. Deliver implementation handoff.
- Include tuning deltas, tradeoffs, and reproducible benchmark commands.
- Provide clear patch plan for runtime/algorithm changes.

## Commands

```bash
python3 scripts/compare_parallel_scaling.py \
  --baseline <baseline.json> \
  --current <current.json> \
  --regression-threshold-pct 5 \
  --efficiency-drop-threshold-pct 10
```

Treat non-zero exits as blocker regressions.

## Output Contract

Return:

1. `Scaling Context`: workload and hardware assumptions.
2. `Findings`: thread-level throughput/speedup/efficiency deltas.
3. `Optimization Plan`: concrete runtime/algorithm changes.
4. `Verification`: benchmark commands and thresholds.
5. `Residual Risks`: unresolved contention or scaling ceilings.

## References

- `references/workflow.md`: detailed parallel optimization sequence.
- `references/scaling-playbook.md`: common bottlenecks and remedies.
- `references/signoff-template.md`: concise scaling sign-off format.

## Execution Rules

- Compare like-for-like workloads and environments only.
- Report both speedup and efficiency, not throughput alone.
- Flag thread-level regressions above thresholds as blockers.
- Avoid overfitting to one thread count; evaluate full scaling curve.
