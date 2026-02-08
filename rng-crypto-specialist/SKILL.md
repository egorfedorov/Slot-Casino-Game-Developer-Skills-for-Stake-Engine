---
name: rng-crypto-specialist
description: Design, implement, and audit provably fair RNG and cryptographic seed workflows for casino games. Use when defining commit-reveal architecture, server/client seed lifecycle, nonce progression, hash/HMAC outcome derivation, bias-free range mapping, fairness transcript verification, or cryptographic release sign-off evidence.
---

# RNG Crypto Specialist

Use this skill to make RNG behavior reproducible, tamper-evident, and independently verifiable.

## Workflow

1. Define fairness contract before implementation.
- Specify game outcomes that are RNG-derived, transcript fields, and reveal timing.
- Set immutable rules for server seed rotation, client seed changes, and nonce increments.
- Declare what players can verify pre- and post-reveal.

2. Choose cryptographic primitives and transcript schema.
- Prefer `SHA-256` commitments and `HMAC-SHA256` outcome derivation unless the system requires otherwise.
- Store canonical transcript fields: `serverSeedHash`, `serverSeed` (after reveal), `clientSeed`, `nonce`, `gameId`, `mode`, and `outcome`.
- Define exact string/byte serialization and encoding rules to avoid replay mismatches.

3. Enforce bias-free outcome mapping.
- Derive randomness from deterministic crypto material only.
- Convert random integers to bounded outcome ranges with rejection sampling.
- Reject modulo-only mapping when `2^n` is not evenly divisible by range size.

4. Implement seed and nonce lifecycle controls.
- Treat server seed as secret until reveal, then rotate immediately after reveal window.
- Keep per-session or per-player nonce monotonic and gap-free.
- Block replay or out-of-order nonce acceptance at API boundaries.

5. Verify transcripts with deterministic tooling.
- Recompute commitment hashes from revealed server seeds.
- Recompute expected outcomes from `serverSeed`, `clientSeed`, and `nonce`.
- Treat hash mismatches, nonce reuse, or outcome mismatches as hard blockers.

6. Produce cryptographic sign-off package.
- Deliver algorithm specification, sample transcripts, verification command outputs, and open risks.
- Include exact patch plan with file paths for any fixes.

## Commands

```bash
python3 scripts/verify_provably_fair.py \
  --server-seed "<secret>" \
  --client-seed "<client>" \
  --nonce 0 \
  --range-max 10000

python3 scripts/verify_provably_fair.py \
  --input <transcript.jsonl> \
  --default-range-max 10000
```

Treat non-zero exits as blocker findings.

## Output Contract

When handling RNG crypto tasks, return:

1. `Protocol Summary`: commit-reveal flow, primitives, serialization, and rotation policy.
2. `Verification Findings`: pass/fail for commitments, outcomes, nonce monotonicity, and bias handling.
3. `Patch Plan`: exact files/functions to change and why.
4. `Evidence`: commands run and key outputs.
5. `Residual Risks`: unresolved issues preventing sign-off.

## References

- `references/workflow.md`: end-to-end implementation and audit procedure.
- `references/crypto-primitives.md`: approved primitives, mappings, and pitfalls.
- `references/signoff-template.md`: concise report structure for handoff.

## Execution Rules

- Keep pre-reveal server seeds confidential; never log plaintext secrets in production traces.
- Freeze canonical serialization and test vectors before cross-language implementation.
- Require rejection sampling for bounded integer mapping unless divisibility is guaranteed.
- Mark any unverifiable outcome path as non-compliant.
