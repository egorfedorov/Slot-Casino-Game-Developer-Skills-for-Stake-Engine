# Workflow

## 1. Baseline And Model

- Record baseline single-thread and multi-thread runs.
- Capture scheduler/runtime settings and core topology.

## 2. Work Decomposition

- Choose decomposition strategy (task/data/pipeline).
- Set chunk sizes and scheduling policy.
- Minimize shared mutable state.

## 3. Bottleneck Analysis

- Measure contention, synchronization overhead, and imbalance.
- Inspect memory behavior (bandwidth/cache effects).

## 4. Scaling Validation

- Compare baseline and current by thread count.
- Evaluate speedup and efficiency curves.
- Gate regressions with fixed thresholds.

## 5. Sign-Off

- Summarize improvements/regressions.
- Include exact rerun commands and patch plan.
