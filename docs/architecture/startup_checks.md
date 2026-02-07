# Requisitos de startup checks (startup_checks.py)

## Antes de procesar primera fila
1. validar env vars requeridas,
2. validar autenticación (endpoint ligero tipo people_me),
3. validar acceso de telefonía (endpoint ligero de locations).

## Resultado
- pass: iniciar ejecución,
- fail: abortar controlado sin procesar filas.

## Registro
- `startup_checks=pass|fail`,
- causa resumida sin secretos.
