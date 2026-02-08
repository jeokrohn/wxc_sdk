
# actions/

Scripts MVP (1 script = 1 acción) para validar viabilidad de endpoints remotos de Webex.


## Runbook MVP end-to-end
Para un flujo completo (generar users dummy -> subida al tenant -> validación del primer script -> ejecución de lote), usa:

- `actions/LAB_MVP_RUNBOOK.md`

## Hallazgo dry-run/testing server-side
No se identifica en la especificación de `functionsList.md` ni en `docs/architecture` una opción de `dry-run` remoto para estas operaciones de configuración.
Por eso cada script soporta:

- `--mode probe` (default): llamadas controladas de lectura o llamadas con dummy input para observar respuestas 4xx/404 comunes sin flujo completo.
- `--mode apply`: intenta ejecutar la acción real contra endpoint con valores aportados vía `--vars`.
- `--mode revert`: restaura el último snapshot preflight capturado durante `--mode apply` para la misma acción.

## Snapshot preflight para revert
- Antes de ejecutar `--mode apply`, el script ejecuta un preflight con llamadas `GET` (a partir de `probe_calls`) para capturar el estado actual remoto.
- Ese snapshot se guarda en temporal con:
  - `lastdatetime_snapshot_action_<action_key>.json` (puntero al último estado)
  - `<YYYYMMDD_HHMMSS>_lastdatetime_snapshot_action_<action_key>.json` (histórico por ejecución)
- Por defecto se usa el directorio temporal del sistema; se puede personalizar con `--snapshot-dir`.

## Uso común
```bash
export WEBEX_ACCESS_TOKEN="..."
python actions/action_call_queue.py --mode probe --vars '{"location_id":"Y2lzY29..."}'
python actions/action_call_queue.py --mode apply --vars '{"location_id":"Y2lzY29...","queue_name":"MVP-Q","extension":"5501","queue_id":"...","member_id":"..."}'
python actions/action_call_queue.py --mode revert --vars '{}' --snapshot-dir /tmp/webex-actions
```

Cada script escribe logs de inicio/fin por paso API e incluye notas de pre y post pasos para identificar si la acción es directa o requiere middle-steps.

## Ayuda de variables por script
Cada script ahora muestra en `--help` qué variables de `--vars` son:

- **Required (apply mode)**: obligatorias para ejecutar `--mode apply`.
- **Optional (probe-only)**: solo útiles para `--mode probe`.

Además, se incluye un mapeo consolidado en `actions/vars_mapping.md` con el detalle por script, endpoint y estado de paridad (script vs SDK 1.27 vs especificación oficial).

## Runner consolidado con validación de respuestas
`actions/run_apply_actions.py` ahora permite:

- Cargar token por `WEBEX_ACCESS_TOKEN`, `WEBEX_TOKEN`, `--token` o `--token-file`.
- Cargar `--context-file` (default `actions/lab_context.json`) para reemplazar automáticamente valores `MISSING_*`.
- Guardar reporte JSON (`--report-file`) con resultado por script y por API call (conteo 2xx vs non-2xx).
- Generar un log por acción (`--log-file` interno por script) además del log consolidado.

Ejemplo:

```bash
python actions/run_apply_actions.py   --continue-on-error   --context-file actions/lab_context.json   --log-file actions/logs/apply_runner_latest.log   --report-file actions/logs/apply_runner_latest.json
```
