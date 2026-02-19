# Autoplay Spec Contract

## File Shape

Required top-level fields:

- `name`
- `limits` (object)
- `stopConditions` (array)
- `ui` (object)
- `confirmation` (object)
- `accessibility` (object)

## Limits Shape

Required:

- `maxSpins`
- `minSpins`

## UI Shape

Required:

- `spinButtonStates` (array)
- `showRemainingSpins` (boolean)

## Confirmation Shape

Required:

- `required` (boolean)
- `showsCost` (boolean)

## Accessibility Shape

Required:

- `reducedMotion` (boolean)

## Failure Conditions

- Missing required fields.
- Invalid spins range.
- Missing confirmation in autoplay flow.
