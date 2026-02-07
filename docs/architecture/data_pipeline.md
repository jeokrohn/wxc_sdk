# Requisitos de data pipeline (data_pipeline.py)

## Entradas/salidas
- Entrada: CSV único.
- Salidas:
  - `ready_to_load.csv` (normalizado)
  - `rejected_rows.csv` (solo fallos pre-API)

## Responsabilidades
- Validar columnas y tipos semánticos.
- Derivar `entity_key` si no viene explícito.
- Normalizar formato (trim, case en keys, booleans, teléfonos/extensiones).
- Aplicar dedupe mínimo y detectar colisiones de clave.
- Rechazar campos fuera de alcance para entidades de usuario post-LDAP.

## Rechazo (rejected_rows.csv)
Campos mínimos:
`timestamp,row_id,entity_type,entity_key,reason_code,reason_message,raw_row_minified`

## Invariantes
- no enviar a runtime filas inválidas,
- mantener trazabilidad 1:1 entre fila original y resultado de validación.
