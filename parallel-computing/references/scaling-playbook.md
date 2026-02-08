# Scaling Playbook

## Contention

- Reduce lock granularity and lock frequency.
- Use sharding/partitioning to reduce cross-thread coordination.

## Load Imbalance

- Use dynamic scheduling when tasks are irregular.
- Adjust chunk size to balance overhead vs fairness.

## Memory/Cache Limits

- Reduce false sharing by separating hot writable data.
- Improve data locality and preallocation.
- Batch operations to improve memory access patterns.

## Synchronization Overhead

- Remove unnecessary barriers.
- Move synchronization out of hot loops.
- Prefer message passing for coarse-grained coordination when applicable.
