# Workflow

## 1. Baseline Setup

- Fix workload profile and traffic mix.
- Record runtime/hardware configuration.
- Run baseline multiple times to estimate variance.

## 2. Path Breakdown

- Split latency into service stages.
- Identify queueing vs execution time.
- Confirm if bottleneck is CPU, memory, lock, I/O, or network.

## 3. Optimization Loop

- Apply one measurable change at a time.
- Re-run controlled load test.
- Record percentile movement and error budget impact.

## 4. Regression Gate

- Compare baseline/current percentile metrics.
- Fail gate if regression exceeds threshold.

## 5. Sign-Off

- Deliver percentile summary, component-level findings, and patch plan.
- Include exact commands for reproducibility.
