# Requisitos de batch iterator (batch_iterator.py)

## Orden fijo de ejecución
### Fase 1
`location, trunk, route_group, internal_dialing, dial_plan, location_call_profiles, location_number_state, schedules, announcements_repo`

### Fase 2
`user_calling_settings, user_numbers, user_forwarding, user_recording, user_monitoring, user_exec_assistant, workspace, workspace_numbers, workspace_forwarding, workspace_recording, workspace_monitoring`

### Fase 3
`groups, group_membership, feature_access, call_pickup_group, call_queue, hunt_group, auto_attendant, devices, number_removal`

## Reglas de batching
- `batch_id` determinista = `phase + sequential_batch_number`.
- máximo `BATCH_SIZE` filas por lote.
- máximo `MAX_ROWS` filas por run.
- máximo `MAX_BATCHES` lotes por run.
- al alcanzar tope: salida controlada + checkpoint.

## Invariantes
- no procesar fase N+1 si fase N no terminó,
- no alterar orden de entity_types dentro de fase.
