# Workflow

## 1. Scope And Constraints

- Define gameplay goals and AI role boundaries.
- Define runtime constraints (latency budget, fallback window, update rate).

## 2. Runtime Architecture

- Define AI systems and provider adapters.
- Define model routing and fallback chain.
- Define data contracts between game loop and AI modules.

## 3. Safety And Reliability

- Define failure modes and safe degradation behavior.
- Define timeout/retry policy with bounded queues.

## 4. Validation

- Validate spec consistency and dependency references.
- Validate telemetry coverage for runtime decisions.

## 5. Release Handoff

- Deliver module map, budgets, and fallback logic summary.
- Include file-level patch plan and acceptance checks.
