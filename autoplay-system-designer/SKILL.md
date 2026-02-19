---
name: autoplay-system-designer
description: Define auto-play UX, stop conditions, and safeguards for slot games. Invoke when implementing autoplay controls, confirmations, or stop-on-event rules.
---

# Autoplay System Designer

Use this skill to design casino-grade auto-play behavior with clear stop rules, safe UI states, and compliance-ready confirmations.

## Core Principles

- Auto-play must be explicit, reversible, and visible at all times.
- Auto-play never bypasses required confirmations for high-cost modes.
- Stop conditions are deterministic and checked before each spin.

## Workflow

1. Define auto-play scope.
- Max spins, stop on win/loss, stop on feature trigger.
- Decide what happens on connection loss or errors.

2. Define UI states.
- Spin button becomes Stop during auto-play.
- Show remaining spins and active stop conditions.

3. Define confirmation flow.
- Require confirmation before start.
- Show cost multipliers or special mode costs.

4. Define stop rules.
- Manual stop always overrides.
- Stop on balance below min bet.
- Stop on session invalidation or compliance errors.

5. Prepare QA matrix.
- Single spin, multiple spins, feature trigger, error recovery.

## Output Contract

Return:

1. `Auto-Play Policy`: limits, counters, stop conditions.
2. `UI Mapping`: button state, counters, labels.
3. `Confirmation Flow`: modal content and gating rules.
4. `Error Handling`: resume/stop policy and user messaging.
5. `Verification`: test matrix and pass criteria.
6. `Risks`: edge cases or ambiguity.

## Commands

```bash
python3 scripts/validate_autoplay_spec.py \
  --input <path/to/autoplay_spec.json>
```

Treat non-zero exits as blocker findings.

## References

- `references/workflow.md`: autoplay design flow.
- `references/contracts.md`: autoplay spec contract.
- `references/checklist.md`: UX and compliance checks.
- `references/signoff-template.md`: sign-off template.

## Execution Rules

- Auto-play must always expose a Stop control.
- Never allow one-click auto-play start without confirmation.
- Avoid restricted wording in social jurisdictions.
