# Requisitos de state store (state_store.py)

## Checkpoint obligatorio
- `pipeline_version`
- `input_hash`
- `phase`
- `last_row_id`
- `started_at`
- `updated_at`

## Escritura
- atómica: tmp + rename.

## Lectura
- validar JSON y esquema mínimo,
- JSON corrupto => abortar controlado con log crítico.

## Invariante
- checkpoint nunca debe adelantar outputs ya persistidos.
