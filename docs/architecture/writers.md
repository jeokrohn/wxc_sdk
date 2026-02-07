# Requisitos de writers (writers.py)

## Principios
- append-safe en modo append,
- flush por registro,
- aborto controlado ante corrupción detectada.

## Archivos y esquemas
### rejected_rows.csv
`timestamp,row_id,entity_type,entity_key,reason_code,reason_message,raw_row_minified`

### results.csv
`timestamp,batch_id,row_id,phase,entity_type,entity_key,step,status,http_status,message,remote_id`

### pending_rows.csv
`timestamp,batch_id,row_id,phase,entity_type,entity_key,step,reason_code,reason_message,http_status,raw_row_minified`

## raw_row_minified
- JSON compacto,
- incluir solo columnas relevantes,
- evitar exposición de datos sensibles.
