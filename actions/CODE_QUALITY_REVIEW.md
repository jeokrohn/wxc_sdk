# Code Quality Review: `actions/`

Fecha: 2026-02-07

## Alcance
Se revisaron todos los scripts `actions/action_*.py` y el módulo compartido `actions/_shared.py`.

## Guías validadas (según configuración)

- **Funciones pequeñas y simples**: los scripts de acción delegan la lógica común a `_shared.py`; cada script solo define `SPEC` y el entrypoint.
- **Separar creación y uso de dependencias**: `SimpleApiClient` se construye en `run_action_spec()` y se inyecta en funciones auxiliares.
- **Abstracción para reducir dependencia entre módulos**: `ActionSpec`/`ApiCall` estandarizan configuración y ejecución.
- **Documentación de edge cases**: errores de red/HTTP y falta de snapshot se registran y devuelven código de salida no-cero.

## Hallazgos

1. **Bug funcional corregido**: `--mode revert` no estaba permitido por `argparse` aunque el flujo existía y la documentación lo anunciaba.
2. **Bug funcional corregido**: faltaban `SnapshotMeta`, `Path` y `tempfile` en `_shared.py`, lo que provocaba fallo en runtime al usar snapshot/revert.
3. **Robustez mejorada**: se valida que `--vars` sea JSON válido y un objeto (`dict`) antes de usarlo.
4. **Mejora pendiente (no bloqueante)**: hay múltiples líneas >120 columnas en scripts de acciones (legibilidad/estilo).
5. **Mejora pendiente (tooling)**: no se pudo ejecutar `flake8` porque no está instalado en el entorno actual.

## Resultado

- Scripts revisados: **19** (`action_*.py`).
- Estado general: **funcionales para probe/apply/revert** tras las correcciones en `_shared.py`.
