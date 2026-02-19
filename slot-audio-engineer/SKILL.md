---
name: slot-audio-engineer
description: Design, mix, and integrate slot game audio including ambient loops, spin sounds, win celebrations, and feature music. Use when defining audio assets, tuning volume levels, synchronizing sound with animations, or validating audio loop seamlessness.
---

# Slot Audio Engineer

Use this skill to design and implement immersive audio experiences that drive player engagement and retention.

## Workflow

1. Define Audio Direction.
- Establish theme, mood, and key audio motifs.
- Create asset list: ambient loops, spin start/stop, reel stop, win tiers, feature triggers.

2. Design and Produce Assets.
- Create seamless loops for background and features.
- Design sound effects (SFX) for interactions.
- Ensure audio levels are balanced and normalized (-14 LUFS target).

3. Integrate and Synchronize.
- Map audio events to game state changes.
- Tune timing to match animation curves.
- Implement dynamic mixing (ducking background for wins).

4. Validate and Optimize.
- Verify loop seamlessness and zero-crossing clicks.
- Check memory usage and compression settings.
- Test across devices for clarity and latency.

## Output Contract

Return:

1. `Audio Map`: list of assets and their triggers.
2. `Integration Plan`: code snippets or config for audio engine.
3. `Validation Report`: loudness check, loop check, memory budget check.

## References

- `references/workflow.md`: Detailed audio production workflow.
- `references/checklist.md`: Quality assurance checklist for audio.
