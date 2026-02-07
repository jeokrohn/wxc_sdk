# Requisitos de executor (executor.py)

## Orquestación
- ejecutar fases en orden fijo,
- iterar lotes y filas,
- resolver steps desde registry.

## Política por fila
- error en cualquier step => `pending` y continuar con siguiente fila,
- si hubo steps previos exitosos y luego fallo => `pending(half_applied)`,
- success solo si todos los steps obligatorios finalizan bien.

## Persistencia y orden de escritura
1. escribir `results.csv`/`pending_rows.csv` según corresponda,
2. flush,
3. actualizar checkpoint.

Nunca actualizar checkpoint antes de persistir salida de la fila actual.

## Resume
- validar `input_hash`;
- si cambia: abortar run controladamente;
- retomar en `phase` y `last_row_id + 1`.

## Circuit breaker
- evaluar al final de cada lote,
- si fallos no recuperables >= `CIRCUIT_BREAKER_THRESHOLD`, abortar controladamente y persistir checkpoint.
