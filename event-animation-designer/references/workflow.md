# Workflow

## 1. Event Inventory

- List all triggering events and origin systems.
- Map each event to animation intent and target state changes.

## 2. Timeline Authoring

- Define step sequence with explicit `startMs`, `durationMs`, and easing.
- Decide overlap policy per animation group.

## 3. State And Transition Model

- Define state nodes and valid transitions.
- Add guard rules for interruption, chaining, and cancellation.

## 4. Validation

- Validate required fields and value ranges.
- Validate step ordering and transition references.
- Validate event coverage and orphan detection.

## 5. Handoff

- Produce timeline contract and validation summary.
- Include patch plan for runtime integration files.
