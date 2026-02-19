---
name: slot-vfx-artist
description: Design and implement visual effects for slot games using shaders, particle systems, and sprite animations. Use when defining big win sequences, feature transitions, symbol animations, or optimizing VFX performance for mobile devices.
---

# Slot VFX Artist

Use this skill to create high-impact visual effects that enhance game excitement and feedback.

## Workflow

1. Conceptualize Effects.
- Sketch or storyboard key moments (Big Win, Free Spins Entry).
- Define style: magical, sci-fi, realistic, cartoon.

2. Implement Core Systems.
- Create particle emitters for coins, sparkles, fire, etc.
- Write shaders for glow, distortion, and color grading.

3. Animate and Sequence.
- keyframe animation properties (scale, opacity, position).
- Sequence effects with game events and audio.

4. Optimize Performance.
- Manage particle counts and overdraw.
- Use texture atlases and compression.
- Profile on low-end devices.

## Output Contract

Return:

1. `VFX Specifications`: description of effects and parameters.
2. `Assets`: shaders, textures, and particle configs.
3. `Performance Report`: frame rate impact and memory usage.

## References

- `references/workflow.md`: VFX pipeline and best practices.
