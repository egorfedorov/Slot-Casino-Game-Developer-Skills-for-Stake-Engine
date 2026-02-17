---
name: css-motion-designer
description: Design CSS animation systems and motion recipes for casino game UI. Use when building round transitions, idle loops, inter-round motion, background patterns, or CSS-only animation specs.
---

# CSS Motion Designer

Use this skill to design production-ready CSS animation systems for casino games, especially round transitions, inter-round motion loops, and lightweight background effects.

## Context Analysis (yui540 motions)

- The motions are authored as pure CSS animations and then screen-recorded.
- Visual rhythm is achieved with discrete stepping and grid-based pattern changes.
- Example motion uses a long sequence string like `0111222333...` to encode frame states.
- Authoring stack includes React with emotion/styled, but the motion logic itself is CSS-first.
- Motion relies on tight timing control and repeated short loops to build perceived complexity.
- Discrete stepping avoids interpolation blur and preserves pixel/segment clarity.
- Motion reads as “procedural” because pattern state is encoded and cycled, not hand-drawn.

## Core Methods Extracted

1. Step-based pattern animation.
- Use `steps(n)` to create discrete jumps for grid patterns.
- Pair `steps(n)` with `repeating-linear-gradient` to build scan, stripe, and barcode effects.

2. Sequence-driven state modulation.
- Encode states as a numeric string (0–3 or 0–4) and map to palette offsets.
- Use CSS variables for state index and drive `background-position` or `filter` shifts.

3. Micro-loop composition.
- Build short 400–1400ms loops and layer them for a richer visual cadence.
- Prefer two short loops instead of one long loop to reduce drift and ease control.

4. Palette orchestration.
- Use 2–4 tones for contrast and keep the darkest tone aligned with the game background.
- Cycle palette assignments per step for pseudo-random “sparkle” without heavy textures.

5. Rhythm gating.
- Insert “quiet” steps (repeated state indices) to avoid constant visual noise.
- Gate loop activation to low-attention states (idle, between rounds, loading).

## Workflow

1. Define motion intent and placement.
- Identify where the motion lives (between rounds, idle state, loading, win transition).
- Declare the player state that can trigger or cancel the motion.

2. Translate visual rhythm into a pattern grammar.
- Choose a grid size and a palette (2–4 tones).
- Encode states as a sequence string (e.g., 0–3) to define frame variations.
- Decide between continuous motion (linear) vs discrete motion (`steps()`).

3. Build CSS motion layers.
- Use CSS variables for palette and speed.
- Prefer transforms and opacity for compositing.
- Use `steps(n)` for pixel/segment patterns to avoid blurry interpolation.

4. Validate performance and safety.
- Cap animation complexity and layer count.
- Provide `prefers-reduced-motion` fallback.
- Ensure animation does not obscure critical UI or break readability.

5. Prepare integration handoff.
- Provide keyframes, timings, and trigger conditions.
- Include reset rules for round transitions.

## Motion Recipes

### Inter-Round Barcode Sweep (Inspired by yui540/5)

Use a repeatable sequence to create a scanning bar effect between rounds.

```css
.interRoundSweep {
  --tile-size: 12px;
  --steps: 30;
  --speed: 1200ms;
  --c0: #0b0f1a;
  --c1: #162235;
  --c2: #223a55;
  --c3: #2f4c6a;
  background: repeating-linear-gradient(
    90deg,
    var(--c0) 0,
    var(--c0) var(--tile-size),
    var(--c1) var(--tile-size),
    var(--c1) calc(var(--tile-size) * 2),
    var(--c2) calc(var(--tile-size) * 2),
    var(--c2) calc(var(--tile-size) * 3),
    var(--c3) calc(var(--tile-size) * 3),
    var(--c3) calc(var(--tile-size) * 4)
  );
  animation: barcodeShift var(--speed) steps(var(--steps)) infinite;
}

@keyframes barcodeShift {
  0% { background-position: 0 0; }
  100% { background-position: calc(var(--tile-size) * 12) 0; }
}
```

### Round Transition Pulse

```css
.roundPulse {
  animation: roundPulse 600ms ease-in-out 1;
}

@keyframes roundPulse {
  0% { opacity: 0; transform: scale(0.98); }
  50% { opacity: 1; transform: scale(1); }
  100% { opacity: 0; transform: scale(1.02); }
}
```

### Idle Spark Grid

Use a 2D grid with step-based offsets to create a subtle “sparkle” during idle.

```css
.idleSparkGrid {
  --cell: 10px;
  --speed: 900ms;
  --steps: 18;
  --bg: #0b0f1a;
  --a: #162235;
  --b: #1f3046;
  --c: #2a3f5a;
  background:
    repeating-linear-gradient(0deg, var(--bg) 0, var(--bg) var(--cell), transparent var(--cell), transparent calc(var(--cell) * 2)),
    repeating-linear-gradient(90deg, var(--bg) 0, var(--bg) var(--cell), transparent var(--cell), transparent calc(var(--cell) * 2)),
    linear-gradient(120deg, var(--a), var(--b), var(--c));
  background-size: auto, auto, 200% 200%;
  animation: idleSpark var(--speed) steps(var(--steps)) infinite;
}

@keyframes idleSpark {
  0% { background-position: 0 0, 0 0, 0% 50%; }
  100% { background-position: 0 0, 0 0, 100% 50%; }
}
```

### Win Accent Scan

Use a fast scan band for a win highlight overlay.

```css
.winAccentScan {
  --speed: 700ms;
  --accent: rgba(255, 214, 102, 0.35);
  background: linear-gradient(90deg, transparent, var(--accent), transparent);
  background-size: 200% 100%;
  animation: winScan var(--speed) ease-out 1;
}

@keyframes winScan {
  0% { background-position: 0% 0; }
  100% { background-position: 200% 0; }
}
```

### Reel Mask Flutter

Use clip-path to create a fluttering shutter feel without heavy assets.

```css
.reelMaskFlutter {
  --speed: 800ms;
  animation: flutter var(--speed) steps(12) infinite;
  clip-path: polygon(0 0, 100% 0, 100% 85%, 0 100%);
}

@keyframes flutter {
  0% { clip-path: polygon(0 0, 100% 0, 100% 86%, 0 100%); }
  100% { clip-path: polygon(0 0, 100% 0, 100% 92%, 0 100%); }
}
```

### Loading Orbit (CSS-Only)

Use a simple rotating gradient for loading or bet-lock states.

```css
.loadingOrbit {
  --speed: 1100ms;
  background: conic-gradient(from 0deg, #0b0f1a, #1b2a40, #0b0f1a);
  animation: orbit var(--speed) linear infinite;
}

@keyframes orbit {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
```

## Casino Integration Patterns

- **Idle State**: low-contrast grid spark, minimal motion noise.
- **Between Rounds**: barcode sweep or soft pulse to indicate state change.
- **Win Reveal**: short scan or pulse overlay that never obscures payout text.
- **Loading/Bet Lock**: orbit or step-based stripes to signal controlled waiting.
- **Bonus Entry**: layered pulse + scan, capped to under 1s total.

## Accessibility and Risk Controls

- Always provide `prefers-reduced-motion: reduce` to disable non-critical loops.
- Keep motion density low during gameplay; reserve “busy” effects for transitions.
- Prevent text flicker by avoiding opacity shifts under critical HUD.

## Output Contract

Return:

1. `Motion Brief`: placement, trigger conditions, duration targets.
2. `Pattern Grammar`: grid size, palette, sequence encoding, steps count.
3. `Keyframes`: final CSS keyframes and class names.
4. `Integration Plan`: which game states show/hide the motion.
5. `Validation`: performance and accessibility checks.
6. `Residual Risks`: readability, distraction, or device constraints.

## Commands

```bash
python3 scripts/validate_css_motion_spec.py \
  --input <path/to/css_motion_spec.json>
```

Treat non-zero exits as blocker findings.

## References

- `references/workflow.md`: motion design workflow.
- `references/contracts.md`: CSS motion spec contract.
- `references/patterns.md`: pattern library and casino state mapping.
- `references/signoff-template.md`: delivery checklist template.

## Execution Rules

- Keep animations deterministic and short in gameplay-critical paths.
- Prefer transforms/opacity over layout-affecting properties.
- Use `steps()` for discrete pattern motion and pixel-art stability.
- Always include a reduced-motion variant.
- Never mask or block critical game info during motion playback.
