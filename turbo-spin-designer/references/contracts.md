# Turbo Spin Spec Contract

## File Shape

Required top-level fields:

- `name`
- `modes` (array)
- `timing` (object)
- `controls` (object)
- `accessibility` (object)

## Mode Shape

Each mode requires:

- `id`
- `label`
- `spinDurationMs`
- `settleDurationMs`
- `allowStop`
- `speedMultiplier`

## Timing Shape

Required:

- `minSpinMs`
- `minSettleMs`
- `maxTotalRoundMs`

## Controls Shape

Required:

- `spinButtonStates` (array)
- `speedToggleLockedStates` (array)

## Accessibility Shape

Required:

- `reducedMotion` (boolean)

## Failure Conditions

- Missing required fields.
- Empty modes list.
- Non-positive durations.
- Total round time exceeds `maxTotalRoundMs`.
