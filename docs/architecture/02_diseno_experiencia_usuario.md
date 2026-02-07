# 2) Diseño de experiencia de usuario (UX operativa)

## User stories (flujo feliz)
1. Como operador, cargo un CSV válido y ejecuto provisión completa sin pasos manuales.
2. Como operador, recibo outputs claros (`results`, `pending`, `rejected`) para auditoría.
3. Como operador, reinicio tras caída y continuo sin duplicidades.

## User stories (flujos alternativos)
1. Como operador, si una fila falla validación, aparece en `rejected_rows.csv` con detalle.
2. Si la API responde 429/5xx, el bot reintenta con límites y sigue.
3. Si un usuario no existe aún en Webex, la fila queda `pending(user_not_found)`.
4. Si faltan permisos/scopes, se aborta temprano (startup checks) o se marca pendiente según contexto.
5. Si se supera umbral de fallos no recuperables por lote, circuit breaker detiene ejecución.

## UX sin interfaz gráfica
- Este producto es de operación por CLI/pipeline CI/CD.
- No hay menús de UI; la experiencia es mediante artefactos y logs estructurados.
- La “navegación” del usuario ocurre en:
  - `checkpoint.json` para estado del run,
  - `results.csv` para éxito/pendiente,
  - `pending_rows.csv` para remediación,
  - `rejected_rows.csv` para corrección de input.

## Wireframe textual del flujo
- Entrada: `input.csv`
- Prevalidación: `ready_to_load.csv` + `rejected_rows.csv`
- Ejecución:
  - Fase 1: location/routing
  - Fase 2: user/workspace settings
  - Fase 3: servicios compartidos
- Salida:
  - `results.csv`
  - `pending_rows.csv`
  - `checkpoint.json`

## Consideraciones UX de soporte
- Manual operativo con ejemplos por entity_type.
- Diccionario de reason codes con acción sugerida.
- Playbook de “retry/re-run/resume”.
