# Optimization Playbook

## Compute-Bound

- Reduce instruction count.
- Replace expensive operations with cheaper equivalents when safe.
- Hoist loop-invariant computations.

## Memory-Bound

- Improve data locality (SoA/AoS tradeoffs).
- Reduce allocations and copies.
- Prefetch or batch accesses when pattern is predictable.

## Branch/Control Flow

- Reduce unpredictable branches in hot loops.
- Use table-driven or branchless patterns only when measured beneficial.

## Allocation Hotspots

- Reuse buffers.
- Use pooling/arena allocators for short-lived objects.
- Avoid per-iteration heap operations in hot loops.

## Concurrency/Locking

- Reduce lock scope and lock frequency.
- Partition shared state to reduce contention.
- Consider lock-free structures only when complexity is justified.
