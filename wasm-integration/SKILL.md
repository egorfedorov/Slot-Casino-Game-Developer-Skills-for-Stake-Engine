---
name: wasm-integration
description: Integrate, validate, and harden WebAssembly modules in frontend/backend application pipelines. Use when wiring WASM build artifacts with JS/TS loaders, validating module/loader contracts, checking init symbols and runtime assumptions, triaging WASM loading failures, or preparing release sign-off for wasm bundle integrity.
---

# WASM Integration

Use this skill to move WebAssembly integration from ad hoc wiring to validated artifact contracts.

## Workflow

1. Define integration contract.
- Document module roles, expected exports/imports, init symbol, and runtime constraints.
- Declare artifact locations and loader ownership.

2. Build and package deterministically.
- Produce `.wasm` and loader artifacts with reproducible build flags.
- Keep artifact naming stable for deployment and caching.

3. Validate bundle integrity.
- Verify wasm binary header/version and non-empty content.
- Verify loader files exist and include WASM instantiation path.
- Verify required symbols are referenced by loader contract.

4. Validate runtime assumptions.
- Check thread/SIMD feature assumptions and fallbacks where required.
- Confirm error handling around failed fetch/instantiate paths.

5. Produce handoff and release gate.
- Deliver pass/fail validation summary, patch plan, and unresolved risks.
- Include exact commands for reproducible verification.

## Commands

```bash
python3 scripts/validate_wasm_bundle.py \
  --manifest <path/to/wasm_bundle.json>
```

Treat non-zero exits as blocker findings.

## Output Contract

Return:

1. `Bundle Map`: module names and artifact paths.
2. `Validation Findings`: pass/fail by module with exact mismatch reasons.
3. `Patch Plan`: files and integration points to fix.
4. `Verification`: command outputs and success criteria.
5. `Residual Risks`: runtime assumptions not yet proven.

## References

- `references/workflow.md`: end-to-end integration flow.
- `references/runtime-contracts.md`: expected loader/module contracts.
- `references/signoff-template.md`: release handoff template.

## Execution Rules

- Keep module-loader contracts explicit and versioned.
- Validate artifact presence and binary sanity before runtime debugging.
- Require deterministic error handling for load/init failures.
- Treat missing critical symbols as blocker issues.
