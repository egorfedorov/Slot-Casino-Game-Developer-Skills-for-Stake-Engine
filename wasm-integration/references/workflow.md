# Workflow

## 1. Contract Definition

- Define module names and ownership.
- Define required exports/import usage and init entrypoints.
- Define runtime constraints (threads/SIMD/fallback policy).

## 2. Artifact Build

- Build `.wasm` and loader artifacts from reproducible configs.
- Keep artifact paths stable for deployment manifests.

## 3. Bundle Validation

- Verify wasm binary sanity (magic + version).
- Verify loader presence and instantiation path.
- Verify required symbols and init references.

## 4. Runtime Validation

- Verify load errors are surfaced with actionable messages.
- Verify fallback path when feature assumptions fail.

## 5. Sign-Off

- Deliver pass/fail bundle report.
- Include exact patch plan and verification commands.
