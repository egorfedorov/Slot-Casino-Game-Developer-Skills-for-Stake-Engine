---
name: ai-game-developer
description: Build, integrate, and validate AI-driven gameplay systems for production game runtimes. Use when implementing AI behavior modules, wiring inference providers into game loops, enforcing latency/fallback budgets, validating safety and telemetry contracts, or auditing AI game features before release.
---

# AI Game Developer

Use this skill to ship AI gameplay features with deterministic runtime behavior and explicit failure handling.

## Workflow

1. Define runtime contract first.
- Specify AI feature goals, update cadence, latency budget, and deterministic fallback behavior.
- Declare model/provider dependencies and allowed failure modes.

2. Implement AI systems behind adapters.
- Keep inference providers behind replaceable adapter interfaces.
- Separate game loop logic from model/provider wiring.
- Ensure each AI system has clear input/output contracts.

3. Enforce runtime safeguards.
- Add timeout and fallback strategy for inference failures.
- Bound update rates and queue growth.
- Protect core gameplay from AI dependency outages.

4. Validate integration spec consistency.
- Validate systems/models/runtime/safety/telemetry fields.
- Validate fallback model references and guard coverage.
- Treat missing fallback and missing telemetry as blockers.

5. Prepare production handoff.
- Deliver module map, runtime budgets, fallback behavior, and test expectations.
- Include patch plan with concrete file targets.

## Commands

```bash
python3 scripts/validate_ai_game_runtime.py \
  --input <path/to/ai_game_runtime_spec.json>
```

Treat non-zero exits as blocker findings.

## Output Contract

Return:

1. `Runtime Map`: systems, models, providers, and budgets.
2. `Validation Findings`: pass/fail with concrete integration gaps.
3. `Patch Plan`: runtime/modules/config files requiring changes.
4. `Verification`: command outputs and acceptance criteria.
5. `Residual Risks`: unresolved latency, fallback, or safety concerns.

## References

- `references/workflow.md`: implementation-to-release process.
- `references/runtime-rules.md`: runtime guardrails and constraints.
- `references/signoff-template.md`: release handoff template.

## Execution Rules

- Keep AI features optional from core gameplay continuity perspective.
- Keep fallback behavior deterministic and tested.
- Keep latency budgets explicit and enforced.
- Flag unsafe failure modes and missing telemetry as blockers.
