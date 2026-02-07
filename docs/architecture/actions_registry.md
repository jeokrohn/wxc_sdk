# Requisitos de actions registry (actions_registry.py)

## Reglas globales
- prohibido `user_create` y `user_update_identity`.
- cada step declara:
  - códigos HTTP de éxito,
  - campos mínimos de respuesta,
  - reason_code de fallo.
- si método SDK no existe y no hay REST validado: `pending(sdk_method_missing)`.
- si precheck no automatizable por API: `pending(out_of_scope)`.
- idempotencia por lookup + upsert con clave estable.

## Fase 1
### location
`location_lookup -> location_create|location_update`

### trunk
`trunk_lookup -> trunk_create|trunk_update`

### route_group
`route_group_lookup -> route_group_create|route_group_update`
precheck de trunks referenciados.

### internal_dialing
`internal_dialing_precheck -> internal_dialing_update`
si dependencia falta => `resource_dependency_missing`.

### dial_plan
`dial_plan_precheck -> dial_plan_lookup -> dial_plan_create|dial_plan_update`
colisión de patrón => `invalid_dial_plan_collision`.

### location_call_profiles
`location_call_profiles_update`

### location_number_state
`number_inventory_precheck -> manage_number_state`
si falta número => `number_inventory_missing`.

### schedules
`schedule_lookup -> schedule_create|schedule_update`

### announcements_repo
`announcement_lookup|upload` (idempotente por clave).

## Fase 2
### user_calling_settings
`user_lookup -> user_enable_calling -> user_apply_calling_settings`
si no existe usuario => `user_not_found`.

### user_numbers
`user_lookup -> number_inventory_precheck -> person_numbers_update`

### user_forwarding
`user_lookup -> user_forwarding_configure`

### user_recording
`user_lookup -> recording_precheck -> user_recording_update`

### user_monitoring
`user_lookup -> monitoring_precheck -> user_monitoring_update`

### user_exec_assistant
`user_lookup -> exec_assistant_update`

### workspace
`workspace_lookup -> workspace_create|workspace_update`
si falta al actualizar => `workspace_not_found`.

### workspace_numbers
`workspace_lookup -> number_inventory_precheck -> workspace_numbers_update`

### workspace_forwarding
`workspace_lookup -> workspace_forwarding_configure`

### workspace_recording
`workspace_lookup -> recording_precheck -> workspace_recording_update`

### workspace_monitoring
`workspace_lookup -> workspace_monitoring_update`

## Fase 3
### groups
`group_lookup -> group_create|group_update`

### group_membership
`group_lookup -> membership_add_remove` (idempotente)

### feature_access
`user_lookup -> feature_access_update`

### call_pickup_group
`pickup_lookup -> pickup_create|pickup_update`

### call_queue
`queue_lookup -> queue_create|queue_update -> queue_agents_update`

### hunt_group
`hunt_lookup -> hunt_create|hunt_update`

### auto_attendant
`aa_predeps(schedule/announcement) -> aa_lookup -> aa_create|aa_update`

### devices
`device_lookup(serial/mac) -> device_create|device_assign`

### number_removal
`number_assignment_precheck -> location_numbers_remove`

## Criterios de éxito
- create: 200/201 + `id` (o equivalente)
- update: 200/204
- delete/remove: 200/204/404 idempotente (cuando aplique)
