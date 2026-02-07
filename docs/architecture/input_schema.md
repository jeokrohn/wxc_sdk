# Contrato único de entrada (input_schema.md)

## Objetivo
Formalizar el CSV único de entrada con validaciones pre-API y reglas de derivación.

## Columnas base (todas las filas)
- `entity_type` (obligatorio)
- `entity_key` (obligatorio o derivable)
- `location_key` (obligatorio cuando aplique)
- `row_ref` (opcional; si falta se usa índice de lectura)

## Columnas por tipo (mínimos)
### location
- `location_name` (si no hay `location_external_id`)
- `location_external_id` (recomendado)
- `time_zone` (obligatorio)
- `address_*` (mínimos obligatorios)

### user_* (post-LDAP)
- `email` obligatorio
- `location_key` obligatorio
- `calling_enabled` opcional (default true)
- `calling_settings_*` opcional
- campos de identidad (`display_name`, `first_name`, `last_name`, etc.) => fuera de alcance

### workspace*
- `workspace_display_name` o `workspace_external_id`
- `location_key`

### assignment / numbers
- `email` o `user_key`
- `extension` y/o `phone_number` (según política)
- `location_key`

## entity_types soportados por fase
### Fase 1
`location, trunk, route_group, internal_dialing, dial_plan, location_call_profiles, location_number_state, schedules, announcements_repo`

### Fase 2
`user_calling_settings, user_numbers, user_forwarding, user_recording, user_monitoring, user_exec_assistant, workspace, workspace_numbers, workspace_forwarding, workspace_recording, workspace_monitoring`

### Fase 3
`groups, group_membership, feature_access, call_pickup_group, call_queue, hunt_group, auto_attendant, devices, number_removal`

## Derivación de entity_key
- location: `location_external_id` o `location_name`
- trunk: `trunk_name`
- route_group: `route_group_name`
- dial_plan/routing_rule: `rule_name` o compuesto
- user_*: `email`
- workspace: `workspace_external_id` o `workspace_display_name`
- assignment/numbers: `(location_id+extension)` o `(location_id+phone_number)`
- queue/hunt/aa/pickup: `(location_id+name)` o `(location_id+extension)`

## Validaciones pre-API
- email válido
- entity_type en enumeración cerrada
- location_key no vacío cuando requerido
- extension numérica (2–8 dígitos)
- phone_number en formato esperado (E.164 si aplica)
- unicidad mínima:
  - location_key único en location
  - email único en user rows
  - extension única por location_key (si aplica)

## Resultado de validación
- inválido pre-API => `rejected_rows.csv`
- válido => `ready_to_load.csv`
