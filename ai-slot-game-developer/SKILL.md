---
name: ai-slot-game-developer
description: Build, integrate, and validate AI-driven slot gameplay systems in production runtimes. Use when implementing AI features for slot modes, wiring model providers, enforcing spin-cycle latency budgets, defining deterministic fallbacks, validating mode/runtime/safety/telemetry contracts, or auditing AI slot readiness before release.
---

# AI Slot Game Developer

Use this skill to ship AI slot features that stay deterministic, performant, and safe under production constraints.

## Workflow

1. Define slot runtime contract.
- Specify AI feature scope per mode (`base`, `bonus`, `buy`, etc.), update points, and max runtime latency.
- Declare deterministic fallback behavior for each mode.

2. Implement AI adapters and mode bindings.
- Keep AI provider/model calls behind adapter interfaces.
- Bind each AI system to explicit slot mode and spin-cycle stage.
- Keep payout-critical logic deterministic and provider-independent.

3. Enforce runtime and safety budgets.
- Apply timeout, queue-depth, and retry limits.
- Ensure inference failure cannot block spin resolution.
- Add safe default outputs per mode.

4. Validate integration spec.
- Validate modes/systems/models/runtime/safety/telemetry consistency.
- Validate fallback model references and mode references.
- Treat missing fallback or missing telemetry as blockers.

5. Prepare release handoff.
- Deliver runtime map, mode budgets, fallback plan, and patch targets.
- Include exact verification commands and acceptance criteria.

## Commands

```bash
python3 scripts/validate_ai_slot_runtime_spec.py \
  --input <path/to/ai_slot_runtime_spec.json>
```

Treat non-zero exits as blocker findings.

## Output Contract

Return:

1. `Slot Runtime Map`: modes, AI systems, models, and budgets.
2. `Validation Findings`: pass/fail with exact mismatches.
3. `Patch Plan`: modules/config files to update.
4. `Verification`: command outputs and pass criteria.
5. `Residual Risks`: unresolved runtime or safety concerns.

## References

- `references/workflow.md`: implementation-to-release process.
- `references/slot-runtime-rules.md`: slot-specific runtime and safety guardrails.
- `references/signoff-template.md`: release sign-off template.

## Execution Rules

- Keep payout-critical path deterministic regardless of model outputs.
- Keep mode fallback behavior explicit and tested.
- Keep runtime budgets bounded and measurable.
- Flag unsafe fallback or missing telemetry as blockers.
