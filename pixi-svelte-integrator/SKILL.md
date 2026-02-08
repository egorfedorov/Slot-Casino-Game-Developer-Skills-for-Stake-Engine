---
name: pixi-svelte-integrator
description: Integrate and validate PixiJS rendering pipelines inside Svelte applications. Use when wiring Pixi application lifecycle to Svelte component lifecycle, handling mount/unmount cleanup, coordinating reactive state with render loop events, validating resize/high-DPI behavior, or debugging event/input/render synchronization issues.
---

# Pixi Svelte Integrator

Use this skill to build stable Pixi+Svelte integrations with explicit lifecycle and teardown guarantees.

## Workflow

1. Define integration boundaries first.
- Decide ownership of app state, render loop control, and event dispatch.
- Keep Pixi scene mutation behind a clear adapter layer.

2. Wire lifecycle safely.
- Create Pixi `Application` in Svelte mount lifecycle.
- Bind canvas to a dedicated host element.
- Destroy application and detach listeners on unmount.

3. Handle resize and DPI policy.
- Track container size updates and renderer resize calls.
- Set and document resolution policy for high-DPI screens.

4. Validate event and render flow.
- Ensure input/event bridge is deterministic and unsubscribed on teardown.
- Keep animation tick subscriptions bounded and removable.

5. Run contract checks before handoff.
- Validate lifecycle contract (create/mount/resize/unmount) and required artifacts.
- Treat missing destroy/unsubscribe paths as blockers.

## Commands

```bash
python3 scripts/validate_pixi_svelte_contract.py \
  --contract <path/to/pixi_svelte_contract.json>
```

Treat non-zero exits as blocker findings.

## Output Contract

Return:

1. `Integration Map`: host component, Pixi app adapter, and event bridge.
2. `Validation Findings`: pass/fail checks for lifecycle, resize, and teardown.
3. `Patch Plan`: exact files and integration points to change.
4. `Verification`: commands and expected pass criteria.
5. `Residual Risks`: unresolved runtime synchronization concerns.

## References

- `references/workflow.md`: end-to-end integration process.
- `references/contracts.md`: lifecycle and event bridge contract rules.
- `references/signoff-template.md`: handoff template for release readiness.

## Execution Rules

- Keep Pixi init/destroy aligned with Svelte mount/unmount.
- Keep all event subscriptions disposable and verified at teardown.
- Avoid direct scene mutation from arbitrary Svelte components.
- Flag any leaked ticker/listener path as a blocker.
