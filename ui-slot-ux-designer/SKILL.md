---
name: ui-slot-ux-designer
description: Design, review, and validate slot game UI/UX flows for desktop and mobile play. Use when defining control hierarchy, spin-state UX, bet/balance presentation, modal interactions, responsive layouts, accessibility constraints, animation-feedback timing, or release readiness checks for slot user experience contracts.
---

# UI Slot UX Designer

Use this skill to turn slot UX ideas into explicit, testable interaction contracts.

## Workflow

1. Define UX scope and player flow.
- Capture session entry, betting, spin cycle, result feedback, and exit states.
- Define desktop/mobile differences explicitly.

2. Establish control hierarchy.
- Define primary controls (spin/bet) and secondary controls (autoplay/turbo/settings).
- Set visibility and priority rules by viewport and game state.

3. Model states and interactions.
- Define UX states and allowed transitions.
- Map interaction triggers to target states and feedback timing.
- Explicitly define disabled/blocked behavior during spin/resolve phases.

4. Enforce accessibility and responsiveness.
- Validate touch targets, reduced-motion support, and contrast-aware behavior.
- Verify control layout works at defined breakpoints.

5. Validate and hand off.
- Run contract validation and classify blockers.
- Deliver patch plan for UI components/state handlers.

## Commands

```bash
python3 scripts/validate_slot_ux_spec.py \
  --input <path/to/slot_ux_spec.json>
```

Treat non-zero exits as blocker findings.

## Output Contract

Return:

1. `UX Map`: views, controls, states, and interactions.
2. `Validation Findings`: pass/fail checks with exact failures.
3. `Patch Plan`: component/state files to adjust.
4. `Verification`: command outputs and success criteria.
5. `Residual Risks`: unresolved usability/accessibility risks.

## References

- `references/workflow.md`: end-to-end slot UX design process.
- `references/ux-rules.md`: control, feedback, and accessibility rules.
- `references/signoff-template.md`: release handoff template.

## Execution Rules

- Keep spin-cycle controls deterministic by state.
- Keep mobile-first touch safety and clarity as hard constraints.
- Keep feedback timing explicit and bounded.
- Flag inaccessible or ambiguous control behavior as blockers.
