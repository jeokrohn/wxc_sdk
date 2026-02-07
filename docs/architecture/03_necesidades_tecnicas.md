# 3) Necesidades técnicas

## Detalles técnicos imprescindibles
- Contrato de entrada cerrado por CSV.
- Validación pre-API estricta.
- Proceso por fases y topes estáticos.
- Idempotencia por estado remoto.
- Persistencia de salida por fila en tiempo real.

## Modelo de datos local
No se exige DB en MVP; persistencia en archivos:
- `ready_to_load.csv`
- `rejected_rows.csv`
- `results.csv`
- `pending_rows.csv`
- `checkpoint.json`

Opcional evolución (si se necesita DB):
- `runs(run_id, input_hash, phase, status, timestamps)`
- `row_results(run_id, row_id, entity_key, status, reason_code, step, remote_id)`
- `row_events(run_id, row_id, step, request_meta, response_meta)`

## Diseño y patrones
- Preferir funciones puras para validación/builders.
- Usar clases para configuración tipada y objetos de integración.
- Inyectar dependencias (cliente API, writers, state_store, registry).
- Usar Enums para estados/reason_codes/error_class.
- Protocols/ABCs para desacoplar adaptadores de infraestructura.

## Librerías/dependencias
- `wxc_sdk` como capa principal.
- REST directo únicamente con contrato verificado cuando falte método SDK.
- Retry/backoff con jitter (tenacity o equivalente).

## Reglas de mantenibilidad
- Módulos y funciones cortas con responsabilidades claras.
- Separar creación de dependencias de uso (factory vs execution).
- Evitar diffs de estado complejos; preferir upsert determinista.

## Edge cases obligatorios
- timeouts de conexión y lectura,
- respuestas 2xx sin campos mínimos,
- corrupción de archivo de salida,
- checkpoint inválido,
- dependencia previa ausente (p.ej., route_group no existente),
- colisión de dial plan con extensiones internas,
- rate limit persistente.
