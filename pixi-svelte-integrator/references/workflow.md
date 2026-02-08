# Workflow

## 1. Ownership Model

- Define Svelte-owned state vs Pixi-owned render state.
- Define one integration adapter as the mutation boundary.

## 2. Lifecycle Wiring

- Create Pixi app on Svelte mount.
- Attach view/canvas to explicit host element.
- Destroy app and listeners on unmount.

## 3. Resize And Resolution

- Listen to container resize events.
- Resize renderer and camera/stage bounds consistently.
- Define high-DPI resolution policy.

## 4. Event Bridge

- Convert pointer/keyboard events into explicit action events.
- Keep subscriptions centralized and disposable.

## 5. Validation Gate

- Validate contract completeness and teardown paths.
- Block release on missing lifecycle or cleanup wiring.
