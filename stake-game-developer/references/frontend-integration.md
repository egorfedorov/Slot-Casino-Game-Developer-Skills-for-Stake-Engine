# Frontend Integration

## Core Principle

Implement frontend as a deterministic event player.

Do not calculate wins, cascades, or multipliers if those values are already delivered by events.

## Integration Rules

1. Spin flow
- Disable spin input once request starts.
- Re-enable only after terminal `roundResult` handling and animation completion.

2. Grid updates
- Render from `reveal` payloads in order.
- Keep event order and animation order aligned.

3. Win rendering
- Read payout and positions from `winInfo`.
- Avoid deriving alternative payouts client-side.

4. Multiplier state
- Update display on `multiplierUpdate`.
- Keep displayed multiplier consistent with event payload.

5. Bonus transitions
- Enter bonus state on `bonusTrigger`.
- Keep remaining spins and mode UI synchronized with subsequent events.

## Error Behavior

- Contract errors: stop playback and surface precise diagnostics.
- Network errors during spin: prevent duplicate spins and provide user recovery path.

## QA Checks

- No console errors in production mode.
- Replay behavior matches original event stream output.
- UI labels/wording remain compliant with jurisdiction mode when `social=true`.
