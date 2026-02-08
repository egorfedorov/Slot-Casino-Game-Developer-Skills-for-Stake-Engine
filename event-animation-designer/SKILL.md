---
name: event-animation-designer
description: Design, sequence, and validate event-driven animation systems for games and interactive UI. Use when defining animation triggers, timeline ordering, transition guards, interruption/cancel rules, easing/duration consistency, event-to-animation mapping, or release readiness checks for animation flow contracts.
---

# Event Animation Designer

Use this skill to turn animation ideas into deterministic, testable event-timeline contracts.

## Workflow

1. Define event-animation contract.
- Capture event sources, animation targets, states, and allowable transitions.
- Specify interruptibility and cancellation rules per animation group.

2. Build timeline map.
- Define ordered steps per event with explicit `startMs`, `durationMs`, and easing.
- Ensure step windows do not overlap when overlap is disallowed.

3. Define transition and guard logic.
- Enumerate valid `fromState -> toState` transitions.
- Define guards for trigger suppression, chaining, and fallback animations.

4. Validate flow consistency.
- Check required fields, durations, and easing values.
- Check transition references and step ordering.
- Treat missing transitions or negative durations as blockers.

5. Prepare implementation handoff.
- Deliver timeline contract, state map, and verification output.
- Include patch plan for runtime animation engine and UI bridge files.

## Commands

```bash
python3 scripts/validate_animation_timeline.py \
  --input <path/to/animation_timeline.json>
```

Treat non-zero exits as blocker findings.

## Output Contract

Return:

1. `Timeline Map`: events, states, transitions, and ordered steps.
2. `Validation Findings`: pass/fail checks with concrete failure reasons.
3. `Patch Plan`: files and animation handlers to adjust.
4. `Verification`: command outputs and success gates.
5. `Residual Risks`: unresolved edge cases (interrupts/chaining/fallback).

## References

- `references/workflow.md`: event-to-animation design flow.
- `references/contracts.md`: required timeline and transition contract.
- `references/signoff-template.md`: release handoff template.

## Execution Rules

- Keep animation sequencing deterministic and state-driven.
- Keep durations/easing explicit for every step.
- Block ambiguous transitions and orphaned events.
- Ensure cancellation paths are explicit where interruption is allowed.
