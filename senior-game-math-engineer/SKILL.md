---
name: senior-game-math-engineer
description: Design, audit, and tune casino game math for Stake-style game pipelines. Use when defining mode math, paytables, reel strips, feature frequencies, RTP/volatility/hit-rate targets, book weights, max-win controls, simulation plans, or release sign-off evidence.
---

# Senior Game Math Engineer

Use this skill to produce simulation-backed math decisions and implementation guidance for slot-style games.

## Workflow

1. Capture target spec before tuning.
- Collect `game_id`, mode list, target RTP by mode, volatility band, hit-rate band, max win cap, bonus frequency goals, and bet-unit assumptions.
- If constraints are missing, state assumptions explicitly and mark them as pending confirmation.

2. Build math model before runtime code.
- Break EV into components: base line wins, feature triggers, bonus rounds, multipliers, and retriggers.
- Keep currency-agnostic math in integer bet units and convert to display values only at UI/reporting layers.
- Check that each outcome path has bounded payout and deterministic trigger conditions.

3. Define mode architecture and RTP split.
- Allocate RTP contribution per mode and feature (base vs bonus).
- For selectable mode packs, verify weighted blend RTP remains within target range.
- Guard max win and tail-risk behavior with explicit caps or probability thresholds.

4. Run simulation and convergence checks.
- Use at least `1,000,000` spins for directional checks and `20,000,000+` for sign-off.
- Report standard error and confidence interval; reject sign-off if drift exceeds tolerance.
- Keep seeds reproducible and preserve run configuration for replay.

5. Validate generated artifacts.
- Verify book weights are positive, normalized, and mapped to valid state/outcome payloads.
- Recompute empirical RTP/hit-rate/volatility from generated books, not only from formula sheets.
- Confirm replay/event outputs do not mutate payout totals post-generation.

6. Prepare sign-off handoff.
- Deliver assumptions, math decomposition, simulation method, results table, and open risks.
- Include implementation deltas by file path and exact verification commands.

## Project Commands

Use existing project verifiers first:

```bash
python3 Engine/scripts/verify_rtp.py <game_id> --spins 1000000
bash games/Darumas/verify_math.sh
bash games/Darumas/test_rtp_check.sh
```

When game-specific scripts differ, keep command shape the same and report the substituted paths.

## Output Contract

When designing or auditing math, return:

1. `Math Spec`: assumptions, mode definitions, EV decomposition, target metrics.
2. `Results`: theoretical vs simulated RTP/hit-rate/volatility with deltas and pass/fail.
3. `Patch Plan`: exact files/functions to edit and why.
4. `Verification`: runnable commands and expected pass criteria.
5. `Risks`: unresolved constraints that block sign-off.

## References

- `references/workflow.md`: detailed step-by-step execution order.
- `references/metrics-and-thresholds.md`: formulas, tolerances, and acceptance gates.
- `references/signoff-template.md`: final report template for handoff.

## Execution Rules

- Distinguish theoretical RTP from simulated RTP in every report.
- Treat sub-million-spin conclusions as preliminary only.
- Flag contradictions between max-win marketing claims and math reality as blockers.
- Prefer deterministic, replayable evidence over narrative claims.
