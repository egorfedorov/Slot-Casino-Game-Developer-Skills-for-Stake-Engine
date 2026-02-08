# Compliance Checklist

## Required Gate

Run compliance checks as a release blocker:

```bash
node scripts/audit-checklist.mjs \
  --rules references/compliance-rules.json \
  --target <path> \
  --social true \
  --format text
```

## Frontend Requirements

- Main game frame is not scrollable.
- Production build does not emit console errors.
- Sound can be disabled in UI.
- Assets are loaded from expected CDN pathing.
- Mobile view remains usable.
- Double-tap zoom is disabled on mobile.

## Rules and Presentation

- Payout info and win-combo rules are clear.
- Game modes and mode costs are clear.
- Bonus/free-spin trigger conditions are clear.
- Bet-mode confirmations are present for high-cost mode changes.
- Disclaimer text required by platform is present.

## RGS and Replay

- Use `rgs_url` query parameter for API target.
- Respect RGS-provided min/max/default bet levels.
- Use RGS-provided balance values.
- Replay URL and optional replay params are supported.

## Social/Jurisdiction

- When `social=true`, restricted phrases must be replaced.
- Do not use prohibited “bet/buy/gamble” style wording in social context.
- Ensure SC/GC display rules are respected where required.

## Fail Policy

Any compliance violation is a hard fail for release recommendation.
