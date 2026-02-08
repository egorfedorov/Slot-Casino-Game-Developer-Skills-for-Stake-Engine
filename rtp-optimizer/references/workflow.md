# Workflow

## 1. Intake

- Capture target RTP by mode.
- Capture tolerance and release gate definition.
- Capture constraints: max win, volatility band, hit-rate band, feature limits.

## 2. Baseline

- Run baseline simulation with locked seed and config version.
- Record current RTP drift and uncertainty.
- Confirm baseline reproducibility before tuning.

## 3. Tuning Loop

- Select one or two high-impact levers.
- Apply changes and rerun simulation.
- Record delta from baseline and previous run.
- Keep a lever-change log per iteration.

## 4. Convergence

- Evaluate multiple runs, not single-run outcomes.
- Compute mean RTP and confidence interval.
- Continue iterations until target and interval both satisfy tolerance.

## 5. Cross-Validation

- Compare theoretical RTP, simulator RTP, and artifact-weighted RTP.
- Investigate and resolve any material mismatch before sign-off.

## 6. Sign-Off

- Produce target table, run summary, pass/fail verdict, and residual risks.
- Include exact verification commands and required file-level changes.
