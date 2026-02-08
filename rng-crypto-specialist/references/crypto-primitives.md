# Crypto Primitives

## Recommended Defaults

- Commitment hash: `SHA-256`
- Outcome derivation: `HMAC-SHA256`
- Seed generation: OS CSPRNG (`/dev/urandom` or platform equivalent)
- Encoding: UTF-8 for strings, explicit byte order for integers

## Canonical Inputs

- `serverSeed`: secret until reveal
- `clientSeed`: user-provided or user-overridable
- `nonce`: monotonic counter
- `counter`: additional index for rejection sampling retries

## Bias-Free Range Mapping

For desired range `N`:

1. Derive `u64` value from cryptographic block.
2. Compute `limit = floor(2^64 / N) * N`.
3. Reject values `>= limit`.
4. Return `value mod N`.

This prevents modulo bias when `N` does not divide `2^64`.

## Common Failure Modes

- Using plain modulo without rejection sampling.
- Inconsistent serialization between services/languages.
- Nonce resets that allow replay.
- Revealing server seed too early.
- Reusing revealed seed in new rounds.

## Evidence Expectations

- At least one published test vector set.
- Transcript re-verification logs with pass/fail counts.
- Seed rotation policy and implementation proof.
