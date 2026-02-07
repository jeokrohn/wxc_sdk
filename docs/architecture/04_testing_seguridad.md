# 4) Implementar pruebas y medidas de seguridad

## Objetivos de cobertura
- Alta cobertura en lógica de control (validación, batching, checkpoint, mapeo de errores).
- Cobertura media en capa de integración (con mocks estables).
- Cobertura funcional mínima por cada fase y entity_type crítico.

## Tipos de pruebas
### Unitarias (sin red)
- validación de esquema CSV,
- dedupe y normalización,
- iterador de fases/lotes,
- serialización append-safe,
- checkpoint atómico y lectura robusta,
- mapeo reason_code por tipo de fallo.

### Behaviorales (HTTP mock)
- create/update success,
- 429 -> retry -> success,
- 5xx -> retry_exhausted,
- 4xx -> non_retryable_external / auth_invalid / permission_denied,
- user_not_found,
- precondition_missing,
- sdk_method_missing,
- half_applied,
- resume sin duplicación.

### E2E (entorno lab)
- ejecución completa por fases,
- validación de outputs y consistencia final,
- prueba de recuperación tras interrupción controlada.

## Side-effects esperados
- cambios en entity_types pueden romper plantillas CSV existentes;
- cambios de timeouts/retries impactan SLAs de ventana de ejecución.

## Seguridad para poder ship
- secretos solo vía variables de entorno;
- no loggear tokens/headers sensibles;
- startup checks de auth y permisos;
- sanitizar campos de fila al persistir raw JSON;
- abortar en corrupción de outputs/checkpoint.

## Auditoría
- trazabilidad por row_id y step,
- razón de fallo siempre explícita,
- evidencia de preflight y circuit breaker en logs.
