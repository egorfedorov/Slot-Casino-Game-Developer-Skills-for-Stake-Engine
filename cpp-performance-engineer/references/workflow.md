# Workflow

## 1. Repro Baseline

- Capture build flags, CPU model, governor/turbo status, and benchmark command.
- Run baseline multiple times to estimate variance.

## 2. Profile First

- Use profiler output to identify hottest functions and call paths.
- Classify bottleneck type: compute, cache, memory, branch, lock, or allocation.

## 3. Optimize Iteratively

- Apply one optimization at a time where feasible.
- Re-run benchmark after each change.
- Keep notes on tradeoffs (complexity, memory usage, portability).

## 4. Compare Benchmark Runs

- Compare baseline vs current by benchmark name.
- Enforce regression threshold for blocker detection.
- Highlight top regressions and top improvements.

## 5. Sign-Off

- Produce concise report with measured deltas and patch plan.
- Include rerun commands and environment notes.
