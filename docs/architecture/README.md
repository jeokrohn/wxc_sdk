# Universal Webex Bulk Provision Bot (Post-LDAP) — Arquitectura v3 (detallada)

## Propósito del paquete de arquitectura
Este directorio define el **contrato integral de implementación** (sin código) para un bot de provisión masiva de Webex Calling orientado a despliegues enterprise.

Objetivos no negociables:
- Un único CSV de entrada como fuente de verdad.
- Idempotencia determinista por lookup remoto + upsert.
- Reanudación segura por checkpoint atómico.
- Sin intervención manual: lo no automatizable queda en `pending(out_of_scope)`.
- Estado terminal por fila exactamente uno de: `rejected`, `pending`, `success`.

## Enfoque de diseño v3
- Marco 1→7 (producto, UX, técnico, pruebas/seguridad, plan, ripple effects, contexto).
- Prioridad MVP: flujo feliz robusto + errores críticos operativos.
- “Zoom out / zoom in”: primero arquitectura global, después detalle por módulo.
- “Distilling the model”: simplificar por eliminación de complejidad innecesaria.

## Documentos de producto y operación (1→7)
1. `01_definicion_producto.md`
2. `02_diseno_experiencia_usuario.md`
3. `03_necesidades_tecnicas.md`
4. `04_testing_seguridad.md`
5. `05_plan_trabajo.md`
6. `06_ripple_effects.md`
7. `07_contexto_ampliado.md`

## Documentos modulares (contrato ejecutable por ingeniería)
- `input_schema.md`: contrato CSV, validación y claves estables.
- `config.md`: variables, defaults y límites estáticos.
- `data_pipeline.md`: normalización, dedupe y rechazo pre-API.
- `batch_iterator.md`: fases, entity_types, lotes y topes.
- `connection_client.md`: request único con timeouts/retry/validación.
- `actions_registry.md`: steps por entity_type, prechecks y reglas de éxito.
- `action_helpers.md`: builders puros y normalización semántica.
- `executor.md`: orquestación, estados terminales, circuit breaker y resume.
- `error_handling.md`: taxonomía y mapeo de reason codes.
- `writers.md`: outputs append-safe y serialización de filas.
- `state_store.md`: checkpoint atómico y lectura robusta.
- `startup_checks.md`: preflight de entorno, auth y permisos.
- `logging.md`: observabilidad estructurada sin secretos.
- `testing.md`: plan de pruebas unitarias, mock HTTP y aceptación.

## Relación con módulos Python del bot
- `config.py` ↔ `config.md`
- `data_pipeline.py` ↔ `input_schema.md` + `data_pipeline.md`
- `batch_iterator.py` ↔ `batch_iterator.md`
- `connection_client.py` ↔ `connection_client.md`
- `actions_registry.py` / `action_helpers.py` ↔ `actions_registry.md` / `action_helpers.md`
- `executor.py` ↔ `executor.md`
- `error_handling.py` ↔ `error_handling.md`
- `writers.py` ↔ `writers.md`
- `state_store.py` ↔ `state_store.md`
- `startup_checks.py` ↔ `startup_checks.md`
