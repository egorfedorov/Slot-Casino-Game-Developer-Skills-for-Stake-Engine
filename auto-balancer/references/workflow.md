# Workflow

## 1. Target Setup

- Define metric targets and tolerance windows.
- Define hard constraints and stop conditions.
- Define tunable parameters and bounds.

## 2. Baseline

- Run baseline simulation/evaluation.
- Capture baseline metric vector and config version.

## 3. Iterative Balancing

- Apply constrained parameter updates.
- Run evaluation and collect metrics.
- Keep history of each iteration.

## 4. Gate Validation

- Validate target metric tolerances.
- Validate hard constraints.
- Validate minimum iteration/run requirements.

## 5. Sign-Off

- Produce final parameter diff and metric summary.
- Include reproducible commands and patch plan.
