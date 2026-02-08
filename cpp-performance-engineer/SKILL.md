---
name: cpp-performance-engineer
description: Profile, diagnose, and optimize C++ performance bottlenecks with measurable evidence. Use when analyzing CPU/memory hotspots, benchmarking before/after changes, triaging regressions from benchmark outputs, improving cache behavior, reducing lock contention, tuning compiler flags, or preparing performance sign-off reports.
---

# C++ Performance Engineer

Use this skill to move C++ performance work from intuition to benchmark-backed decisions.

## Workflow

1. Establish reproducible baseline.
- Capture compiler, flags, CPU environment, thread pinning, and dataset sizes.
- Run baseline benchmarks before changing code.

2. Identify hotspot class.
- Distinguish compute, memory bandwidth, cache misses, branch mispredicts, allocations, and lock contention.
- Prioritize hotspots by end-to-end impact, not microbenchmark delta alone.

3. Apply targeted optimizations.
- Use data-layout and allocation changes for memory-bound paths.
- Use algorithmic/branch simplification for compute-bound paths.
- Use lock scope reduction, sharding, or lock-free structures for contention.
- Keep each optimization isolated and benchmarked.

4. Validate with benchmark comparison.
- Compare current run against baseline with explicit regression thresholds.
- Flag statistically suspicious or high-variance benchmark rows.

5. Package performance handoff.
- Provide measured deltas, affected files, tradeoffs, and risks.
- Include reproducible benchmark commands.

## Commands

```bash
python3 scripts/compare_benchmark_json.py \
  --baseline <baseline.json> \
  --current <current.json> \
  --metric cpu_time \
  --regression-threshold 5.0
```

Treat non-zero exits as blocker regressions.

## Output Contract

Return:

1. `Baseline Context`: compiler/env assumptions and benchmark scope.
2. `Findings`: top regressions/improvements with measured deltas.
3. `Optimization Plan`: exact code-level changes and expected impact.
4. `Verification`: rerun commands and regression gates.
5. `Residual Risks`: variance, measurement noise, or unresolved bottlenecks.

## References

- `references/workflow.md`: detailed profiling and optimization sequence.
- `references/optimization-playbook.md`: hotspot-to-technique mapping.
- `references/signoff-template.md`: concise performance report template.

## Execution Rules

- Never claim performance gains without before/after measurements.
- Keep benchmark environments comparable across runs.
- Separate microbenchmark wins from end-to-end impact.
- Escalate regressions above threshold as blockers.
