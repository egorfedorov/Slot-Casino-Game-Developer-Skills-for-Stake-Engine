# Workflow

## 1. Intent And Constraints

- Capture desired player experience and feature hierarchy.
- Capture hard constraints: max win, max feature length, retrigger caps.

## 2. State Graph

- Define `initialState`.
- Define state list with terminal flags.
- Define transitions with `from`, `event`, `to`.

## 3. Mechanics Definitions

- Define each mechanic with:
  - `id`
  - `triggerEvent`
  - `entryState`
  - `targetState`
  - `actions[]`
- Attach guard conditions and cooldown/retrigger policies explicitly.

## 4. Integrity Checks

- Verify all state references are valid.
- Verify non-terminal states are reachable and have outgoing transitions.
- Verify mechanic trigger and state mapping have transition support.

## 5. Implementation Handoff

- Deliver behavior spec and event contract.
- Include engine/frontend integration notes and patch plan.
- Include explicit unresolved assumptions.
