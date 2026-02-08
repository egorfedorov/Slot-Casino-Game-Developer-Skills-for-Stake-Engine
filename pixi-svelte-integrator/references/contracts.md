# Contracts

## Contract File Shape

Required top-level fields:

- `name`: integration name
- `hostComponent`: Svelte host component path/name
- `pixiAdapter`: adapter module path/name
- `lifecycle`: object
- `events`: object
- `resize`: object

## Lifecycle Requirements

Required `lifecycle` flags:

- `createOnMount` = `true`
- `destroyOnUnmount` = `true`
- `detachCanvasOnUnmount` = `true`
- `disposeListenersOnUnmount` = `true`

## Event Requirements

Required `events` fields:

- `bridgeEnabled` = `true`
- `unsubscribeOnUnmount` = `true`
- `sources`: non-empty array

## Resize Requirements

Required `resize` fields:

- `observeContainer` = `true`
- `rendererResize` = `true`
- `respectDevicePixelRatio` = `true`

## Failure Conditions

- Missing required top-level keys.
- Any required lifecycle flag not `true`.
- Missing/unbounded event cleanup.
- Missing container resize handling.
