---
name: low-latency-systems
description: Design, diagnose, and optimize low-latency request paths in backend and realtime systems. Use when profiling p50/p95/p99 latency regressions, reducing queueing and lock contention, tuning network/serialization overhead, validating tail-latency improvements, or preparing latency sign-off evidence with strict percentile gates.
---

# Low Latency Systems

Use this skill to turn latency incidents and regressions into measurable, reproducible fixes.

## Workflow

1. Lock measurement context first.
- Capture workload, concurrency, payload sizes, warmup policy, and hardware/runtime settings.
- Keep baseline and current runs environment-compatible.

2. Decompose latency path.
- Split end-to-end latency into ingress, queue, compute, storage/network, and egress components.
- Prioritize tail-latency contributors over average-only improvements.

3. Apply targeted latency fixes.
- Reduce blocking, contention, and unbounded queues.
- Reduce allocations/serialization overhead in hot paths.
- Use batching, caching, and async boundaries only when measured beneficial.

4. Validate percentile regressions.
- Compare baseline vs current percentiles (`p50`, `p95`, `p99`, optional `p999`).
- Gate release on configured regression thresholds.

5. Produce sign-off output.
- Provide measured deltas, affected components/files, and residual risks.
- Include exact rerun commands for verification.

## Commands

```bash
python3 scripts/compare_latency_runs.py \
  --baseline <baseline.json> \
  --current <current.json> \
  --threshold-pct 5
```

Treat non-zero exits as blocker regressions.

## Output Contract

Return:

1. `Latency Baseline`: environment/workload assumptions.
2. `Findings`: percentile deltas and hotspot classes.
3. `Optimization Plan`: exact changes with expected impact.
4. `Verification`: rerun commands and regression gates.
5. `Residual Risks`: variance or unresolved tail spikes.

## References

- `references/workflow.md`: detailed low-latency process.
- `references/latency-playbook.md`: bottleneck-to-fix mapping.
- `references/signoff-template.md`: concise sign-off format.

## Execution Rules

- Prioritize tail latency (`p95/p99`) when evaluating user impact.
- Keep measurement setup stable across comparisons.
- Require before/after evidence for each claimed improvement.
- Escalate threshold breaches as blockers.
