# Stake Engine RGS Quick Reference

Source baseline: https://stake-engine.com/docs and local snapshots in `output/console/details`.

## Required launch URL fields

- `sessionID`: player session token.
- `lang`: UI language code (ISO 639-1).
- `device`: `mobile` or `desktop`.
- `rgs_url`: runtime RGS base URL (must be dynamic).
- Example: `index.html?sessionID=...&lang=en&device=desktop&rgs_url=...`

## Core wallet flow

1. `POST /wallet/authenticate`
- **Mandatory first call** on game load.
- Validates `sessionID`.
- Read `balance`, `config`, and possibly `round` from response.
- Use `config.minBet`, `config.maxBet`, `config.stepBet`, `config.betLevels`.
- **Note:** If not called, subsequent calls fail with `ERR_IS`.

2. `POST /wallet/play`
- Executes a game round.
- Returns event stream.

3. `GET /bet/replay/{game}/{version}/{mode}/{event}`
- **Replay API**: Fetches outcome for replay mode.
- **No Auth Required**: Must work without `sessionID`.
- Returns: `{ "payoutMultiplier": float, "costMultiplier": float, "state": object }`

3. `POST /wallet/end-round`
- **Mandatory** if round win > 0 or game logic requires explicit close.
- Finalizes the bet and updates balance.

4. `POST /wallet/balance`
- Refresh balance when needed.

5. `POST /bet/event`
- Save in-round progress to support resume after reconnect.

## Amount model

- Money is integer micro-units with 6 decimals of precision.
- Example: `1000000` means `1.0`.
- Validate amount range and step divisibility before sending play.

## Error codes to handle

Client side (400):
- `ERR_VAL`: invalid request.
- `ERR_IPB`: insufficient player balance.
- `ERR_IS`: invalid/expired session.
- `ERR_ATE`: auth token expired.
- `ERR_GLE`: gambling limits exceeded.
- `ERR_LOC`: invalid player location.

Server side (500):
- `ERR_GEN`: generic server error.
- `ERR_MAINTENANCE`: scheduled maintenance.

## Implementation guardrails

- Never call play/balance/end-round before authenticate.
- Never hardcode RGS host.
- Keep gameplay logic independent of displayed currency format.
