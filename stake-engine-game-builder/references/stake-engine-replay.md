# Stake Engine Replay Requirements

Source baseline: https://stake-engine.com/docs and local `output/console/details/replay.md`.

## Mandatory status

- Replay support is required for approval of new games.

## Replay mode parameters

Required:
- `replay=true`
- `game`
- `version`
- `mode`
- `event`
- `rgs_url`

Optional:
- `currency`, `amount`, `lang`, `device`, `social`

## Replay endpoint

- `GET {rgs_url}/bet/replay/{game}/{version}/{mode}/{event}`

Expected payload fields:
- `payoutMultiplier`
- `costMultiplier`
- `state` (game-specific replay state)

## UX and behavior rules

- Auto-fetch replay data at load.
- Show loading indicator, then explicit play trigger.
- Disable or hide live betting controls.
- Do not make authenticated session calls in replay mode.
- Play full animation/sound sequence and display final result.
- Provide `Play Again` to rerun replay only.
- Prevent transition from replay session into real betting.

## QA scenarios per mode

- Loss
- Normal win
- Big win
- Max win cap
- Bonus trigger (if mode supports it)
