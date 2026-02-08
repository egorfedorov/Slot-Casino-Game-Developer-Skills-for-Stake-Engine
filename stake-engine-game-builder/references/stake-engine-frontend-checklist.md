# Stake Engine Frontend Compliance Checklist

Source baseline: https://stake-engine.com/docs and local snapshots `front.md` + `disclaimer.md`.

## Build and Deployment

- Use Vite for build pipeline (`npm create vite@latest`).
- Set `base: "./"` in `vite.config.ts` (plugins section).
- Upload `dist/` contents to Stake Engine.
- Ensure no absolute paths in build artifacts.

## Asset and runtime policy

- Ship static files only.
- Load fonts/images/audio from Stake Engine CDN paths.
- Avoid external runtime dependencies that trigger network leaks.
- Keep console/network tabs clean (no recurring errors).

## Layout and UX

- Support mobile form factors.
- Support mini-player/popout without distorted core game board.
- Keep win amounts legible, including fast-play paths.

## Game info requirements

- Expose rules/paytable in UI.
- Show RTP and max win per mode.
- Explain mode-specific cost and purchased actions.
- List payout combinations and special symbol values.
- Describe feature triggers (for example scatters/free spins).

## Control requirements

- Allow player to change bet size.
- Offer all bet levels returned by authenticate config.
- Display current balance.
- Show non-zero final win clearly.
- Increment payout display coherently for multi-step win reveals.
- Provide sound toggle.
- Map spacebar to bet action.
- Require explicit confirmation for autoplay.

## Mandatory disclaimer

Include equivalent meaning to:
- Malfunction voids wins and plays.
- Stable internet is required; reload to complete interrupted rounds.
- RTP is a long-run expectation.
- Browser visuals do not determine settlement.
- Payout is determined by RGS response.
