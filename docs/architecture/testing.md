# Requisitos de testing

## Unit tests
- `data_pipeline`: schema/normalización/dedupe/rejected.
- `batch_iterator`: orden por fase + límites.
- `writers` y `state_store`: append, flush, atomicidad, corrupción.
- `error_handling`: mapping reason_code.

## Behaviorales (mock HTTP)
- create success,
- update success,
- 429 retry success,
- 5xx retry_exhausted,
- 4xx non-retry,
- user_not_found,
- precondition_missing,
- sdk_method_missing,
- half_applied,
- crash/restart resume sin duplicar.

## Aceptación
- prueba de 21.000 filas con límites configurados,
- no bloqueos indefinidos (timeouts),
- estados finales correctos por fila,
- consistencia de outputs.
