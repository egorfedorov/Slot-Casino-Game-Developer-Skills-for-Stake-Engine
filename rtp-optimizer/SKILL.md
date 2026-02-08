---
name: rtp-optimizer
description: Optimize and validate slot/casino RTP against explicit targets using simulation evidence. Use when defining RTP targets per mode, tuning paytables and feature frequencies, validating convergence from simulation runs, comparing theoretical vs empirical RTP, or preparing release sign-off with pass/fail thresholds.
---

# RTP Optimizer

Use this skill to move a game from rough math to quantifiably validated RTP.

## Workflow

1. Define targets and guardrails first.
- Capture RTP target by mode, tolerance band, max win cap, volatility expectations, and feature frequency limits.
- Mark any missing constraint as an explicit assumption.

2. Identify controllable tuning levers.
- Prioritize levers with predictable RTP effect: symbol payouts, reel strips, feature trigger weights, bonus multipliers, and retrigger caps.
- Avoid changing multiple high-impact levers at once unless required.

3. Run iterative simulation with convergence checks.
- Use short runs for direction (`>=1M` spins), then long runs for sign-off (`>=20M` spins).
- Track seeds, config hash/version, and lever deltas per run.
- Reject sign-off if mean RTP is outside tolerance or confidence interval crosses tolerance boundaries.

4. Cross-check theoretical and artifact-weighted RTP.
- Compare model RTP, simulator RTP, and weighted book RTP.
- Treat unresolved drift between these sources as a blocker.

5. Prepare optimization sign-off.
- Deliver run summary, lever changes, pass/fail verdict, and residual risks.
- Include exact patch plan and verification commands.

## Commands

```bash
python3 scripts/evaluate_rtp_runs.py \
  --input <runs.jsonl> \
  --target-rtp 0.9600 \
  --tolerance 0.0020
```

Use this command to produce deterministic convergence and pass/fail output for a run set.

## Output Contract

Return:

1. `Targets`: mode targets, tolerance bands, assumptions.
2. `Lever Plan`: changed levers and expected RTP direction.
3. `Run Results`: mean RTP, CI, drift, pass/fail verdict.
4. `Patch Plan`: exact files/functions requiring edits.
5. `Residual Risks`: blockers or statistical uncertainty.

## References

- `references/workflow.md`: tuning lifecycle and sequencing.
- `references/tuning-levers.md`: common lever impact and failure patterns.
- `references/signoff-template.md`: concise handoff template.

## Execution Rules

- Keep theoretical and simulated RTP separated in reporting.
- Require reproducible run metadata (seed, spins, config version).
- Treat tolerance breach or unstable convergence as release blockers.
