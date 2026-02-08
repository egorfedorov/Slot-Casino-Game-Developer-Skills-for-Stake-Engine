# Runtime Rules

## Required Runtime Guarantees

- AI inference must not block core game loop beyond declared budget.
- Fallback path must be deterministic and state-safe.
- All AI-driven decisions must be observable via telemetry.

## Model/Provider Rules

- Every primary model can define a fallback model.
- Fallback references must resolve to existing model IDs.
- Provider outages must map to explicit failure modes.

## Safety Rules

- Define rate limiting for AI invocation paths.
- Define bounded queue/backpressure behavior.
- Define safe behavior when inference confidence is unavailable.
