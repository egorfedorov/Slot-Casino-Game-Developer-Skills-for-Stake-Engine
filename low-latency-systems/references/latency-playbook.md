# Latency Playbook

## Queueing/Contention

- Reduce lock scope and contention points.
- Bound queue depth and apply backpressure.
- Prefer sharding over global locks in hot paths.

## Serialization/Parsing

- Reduce payload size and avoid repeated encode/decode.
- Use zero-copy or pooled buffers when safe.

## Network/I/O

- Reuse connections and avoid avoidable round-trips.
- Batch small requests where latency budget allows.
- Cache high-frequency read paths with strict invalidation.

## Tail-Latency Control

- Set timeouts and cancellation boundaries.
- Isolate slow dependencies and fail fast when needed.
- Measure and cap retries to avoid amplification.
