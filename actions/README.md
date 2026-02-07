
# actions/

Scripts MVP (1 script = 1 acción) para validar viabilidad de endpoints remotos de Webex.

## Hallazgo dry-run/testing server-side
No se identifica en la especificación de `functionsList.md` ni en `docs/architecture` una opción de `dry-run` remoto para estas operaciones de configuración.
Por eso cada script soporta:

- `--mode probe` (default): llamadas controladas de lectura o llamadas con dummy input para observar respuestas 4xx/404 comunes sin flujo completo.
- `--mode apply`: intenta ejecutar la acción real contra endpoint con valores aportados vía `--vars`.

## Uso común
```bash
export WEBEX_ACCESS_TOKEN="..."
python actions/action_call_queue.py --mode probe --vars '{"location_id":"Y2lzY29..."}'
python actions/action_call_queue.py --mode apply --vars '{"location_id":"Y2lzY29...","queue_name":"MVP-Q","extension":"5501","queue_id":"...","member_id":"..."}'
```

Cada script escribe logs de inicio/fin por paso API e incluye notas de pre y post pasos para identificar si la acción es directa o requiere middle-steps.
