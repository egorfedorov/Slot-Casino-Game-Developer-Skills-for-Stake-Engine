# CSS Motion Spec Contract

## File Shape

Required top-level fields:

- `name`
- `placements` (array of strings)
- `recipes` (array)
- `timings` (object)
- `accessibility` (object)

## Recipe Shape

Each recipe requires:

- `id`
- `intent`
- `cssClass`
- `keyframes`
- `durationMs`
- `loop` (boolean)

## Timings Shape

Required:

- `maxDurationMs`
- `maxConcurrentLayers`

## Accessibility Shape

Required:

- `reducedMotion` (boolean)
- `noObstructionZones` (array)

## Failure Conditions

- Missing required fields.
- Empty recipe list.
- Non-positive duration.
- Max duration exceeded by any recipe.
