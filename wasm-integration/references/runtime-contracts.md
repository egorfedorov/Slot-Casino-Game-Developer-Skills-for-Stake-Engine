# Runtime Contracts

## Manifest Shape

Expected root fields:

- `root` (optional): base directory for relative paths
- `modules`: array of module descriptors

Module descriptor fields:

- `name` (required)
- `wasm` (required)
- `loader` (required)
- `initSymbol` (optional)
- `requiredExports` (optional array)
- `requiredImports` (optional array)
- `requiresThreads` (optional boolean)
- `requiresSimd` (optional boolean)

## Loader Expectations

- Must reference WebAssembly instantiation path:
  - `WebAssembly.instantiate`
  - or `WebAssembly.instantiateStreaming`
- If `initSymbol` is provided, loader should reference it.
- If `requiresThreads` is true, loader should reference `SharedArrayBuffer`.

## Failure Conditions

- Missing or unreadable artifacts.
- Invalid wasm header/version.
- Missing required loader references.
- Manifest shape errors.
