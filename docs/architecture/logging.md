# Requisitos de logging

## Formato
- estructurado (JSON o key=value),
- nivel INFO por defecto.

## Eventos obligatorios
- inicio/fin run,
- inicio/fin fase,
- inicio/fin lote con contadores,
- fila en error (`entity_key`, `step`, `reason_code`),
- reintentos cuando ocurren,
- trigger de circuit breaker,
- startup checks pass/fail.

## Prohibiciones
- no loggear tokens ni headers sensibles,
- evitar ruido: resumen por lote + detalle de errores.
