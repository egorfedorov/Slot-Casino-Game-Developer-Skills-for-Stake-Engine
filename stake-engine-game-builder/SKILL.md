---
name: stake-engine-game-builder
description: Build, adapt, and review casino game implementations for Stake Engine based on https://stake-engine.com/docs requirements. Use when implementing RGS communication, replay mode, frontend compliance, publication readiness checks, or converting an existing game to Stake Engine-compatible behavior.
---

# Stake Engine Game Builder

Use this skill to ship a game that passes Stake Engine technical review.

## Execute Workflow

1. Identify task type.
- New game integration: implement full flow from URL parsing to RGS calls and replay mode.
- Existing game audit: run compliance checklist and patch gaps.
- Submission readiness: run test matrix and deliver fail/pass report with fixes.

2. Parse runtime query parameters first.
- Read `sessionID`, `lang`, `device`, and `rgs_url` from game URL.
- Never hardcode RGS host.
- Treat `lang` as ISO 639-1 code and keep UI stable even if only `en` is translated.

3. Implement mandatory RGS lifecycle.
- Call `POST /wallet/authenticate` on load before any other wallet endpoint.
- Use `config.minBet`, `config.maxBet`, `config.stepBet`, and `config.betLevels` from authenticate response.
- Place bets via play endpoint and finalize round with `POST /wallet/end-round` when round must be closed.
- Handle invalid session and balance errors explicitly.

4. Apply amount and display rules.
- Keep money in integer micro-units (1.000000 precision).
- Validate bet amount bounds and step divisibility before sending request.
- Format balance by currency metadata in UI only; game math must stay currency-agnostic.

5. Implement mandatory replay mode.
- Detect replay via `replay=true` query param.
- Fetch replay state from `GET {rgs_url}/bet/replay/{game}/{version}/{mode}/{event}`.
- Disable live betting/session flow in replay mode.
- Keep replay controls only (play / play again) and show final result.

6. Enforce frontend compliance.
- Ship static frontend files only.
- Load assets (fonts/images/audio) from Stake Engine CDN paths only.
- Keep mobile and mini-player layouts readable and usable.
- Provide rules/paytable, RTP, max win, and mode-cost details in UI.
- Include mandatory disclaimer in rules popup.

7. Validate before handoff.
- Test each mode across win/loss/max-win scenarios.
- Test replay for each mode with provided event IDs.
- Test currencies/languages matrix.
- Check browser console/network for errors and external-resource leaks.

## Output Contract

When delivering implementation or audit, return:

1. `Implemented` or `Missing` checklist by area: URL/RGS, betting constraints, replay, UI compliance.
2. Exact file-level patch plan.
3. Test matrix with pass/fail and reproduction steps for failures.

## References

Load only what is needed:

- RGS and wallet flow: `references/stake-engine-rgs.md`
- Replay requirements: `references/stake-engine-replay.md`
- Frontend/compliance checklist: `references/stake-engine-frontend-checklist.md`

Use local docs snapshots for details and examples:
- `/Users/egorfedorov/Downloads/darkbytes/Engine/output/console/details/rgs.md`
- `/Users/egorfedorov/Downloads/darkbytes/Engine/output/console/details/wallet.md`
- `/Users/egorfedorov/Downloads/darkbytes/Engine/output/console/details/replay.md`
- `/Users/egorfedorov/Downloads/darkbytes/Engine/output/console/details/front.md`
- `/Users/egorfedorov/Downloads/darkbytes/Engine/output/console/details/disclaimer.md`
