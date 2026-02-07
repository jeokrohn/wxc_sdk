# Requisitos de configuración (config.py)

## Variables requeridas
- `ENVIRONMENT` ∈ {`lab`, `prod`}
- `WEBEX_BASE_URL`
- `WEBEX_TOKEN`
- `OUTPUT_DIR`

## Variables opcionales (defaults)
- `BATCH_SIZE=500`
- `MAX_ROWS=21000`
- `MAX_BATCHES=1000`
- `MAX_RETRIES=5`
- `REQUEST_TIMEOUT_SECONDS=20`
- `CONNECT_TIMEOUT_SECONDS=5`
- `CIRCUIT_BREAKER_THRESHOLD=0.80`
- `ENABLE_SAFE_COMPENSATION=false`
- `PIPELINE_VERSION=1`

## Reglas
- parseo tipado estricto de configuración,
- mostrar config efectiva sin secretos al iniciar,
- cualquier loop debe respetar límites estáticos,
- no permitir ejecución si faltan variables requeridas.
