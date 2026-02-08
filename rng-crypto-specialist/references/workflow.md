# Workflow

## 1. Scope And Threat Model

- Enumerate RNG-dependent outcomes.
- Define attacker goals: predict outcomes, bias outcomes, alter transcripts, replay nonces.
- Define trust boundaries: backend, client, storage, transport, observability.

## 2. Commit-Reveal Design

- Generate high-entropy `serverSeed` from CSPRNG.
- Publish `serverSeedHash = SHA256(serverSeed)` before rounds begin.
- Use player-controlled `clientSeed` and monotonic `nonce`.
- Reveal `serverSeed` on rotation and allow retrospective verification.

## 3. Deterministic Outcome Derivation

- Build message with stable serialization, for example: `clientSeed:nonce:counter`.
- Compute block material with `HMAC_SHA256(serverSeed, message)`.
- Map to outcome range with rejection sampling, not naive modulo.
- Document exact math and types (byte order, integer size, encoding).

## 4. Controls

- Require nonce monotonicity per seed scope.
- Rotate server seeds on schedule or threshold.
- Prevent using revealed seeds for new wagers.
- Log verification fields without exposing unrevealed server seeds.

## 5. Verification

- Verify commitment hash against revealed server seed.
- Recompute outcomes from transcript and compare against stored outcomes.
- Validate no nonce duplicates or regressions in each scope.
- Validate mapping method has no detectable bias.

## 6. Release Gate

- Publish algorithm note and test vectors.
- Run transcript verification tooling on representative production-like data.
- Block release if any commitment/outcome/nonce mismatch occurs.
