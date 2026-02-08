# Contracts

## Timeline File Shape

Required top-level fields:

- `name`
- `states` (array of state names or objects with `name`)
- `events` (array)
- `transitions` (array)
- `timelines` (array)

## Transition Shape

Each transition requires:

- `from`
- `event`
- `to`

## Timeline Shape

Each timeline requires:

- `event`
- `fromState`
- `toState`
- `steps` (non-empty array)

Each step requires:

- `id`
- `target`
- `startMs` (`>= 0`)
- `durationMs` (`> 0`)
- `easing`

## Failure Conditions

- Missing required fields.
- Unknown state/event references.
- Non-positive duration.
- Out-of-order step starts.
- Timeline without matching transition.
