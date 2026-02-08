# Comandos de prueba por script (laboratorio)

> Todos los scripts `action_*.py` hacen llamadas reales al API Webex y **requieren** `WEBEX_ACCESS_TOKEN` válido y datos existentes en el tenant.

## Paso 0: generar usuarios dummy

```bash
python actions/generate_dummy_users.py --count 15 --domain lab.example.com --format json --output actions/dummy_users.json
python actions/generate_dummy_users.py --count 15 --domain lab.example.com --format csv --output actions/dummy_users.csv
```

## Paso 1: comandos por script

### action_auto_attendant.py
- Required `--vars`: `aa_name, extension, location_id, schedule_name`
- Optional `--vars`: `(none)`
- Dependencias/espera de servidor: Paso previo: crear/usar schedule y announcement si faltan. / Paso posterior: validar menús y horario en lectura final.
```bash
python actions/action_auto_attendant.py --mode apply --vars '{"aa_name": "<aa_name>", "extension": "<extension>", "location_id": "<location_id>", "schedule_name": "<schedule_name>"}'
```

### action_call_pickup_group.py
- Required `--vars`: `extension, location_id, member_id, pickup_name`
- Optional `--vars`: `(none)`
- Dependencias/espera de servidor: Paso previo: lookup por location+name/extension. / Paso posterior: releer grupo para validar miembros.
```bash
python actions/action_call_pickup_group.py --mode apply --vars '{"extension": "<extension>", "location_id": "<location_id>", "member_id": "<member_id>", "pickup_name": "<pickup_name>"}'
```

### action_call_profiles.py
- Required `--vars`: `location_id`
- Optional `--vars`: `(none)`
- Dependencias/espera de servidor: Paso previo: confirmar entidad destino y licencia. / Paso posterior: releer configuración para confirmar estado final.
```bash
python actions/action_call_profiles.py --mode apply --vars '{"location_id": "<location_id>"}'
```

### action_call_queue.py
- Required `--vars`: `extension, location_id, member_id, queue_id, queue_name`
- Optional `--vars`: `(none)`
- Dependencias/espera de servidor: Paso previo: validar location y announcement opcional. / Paso posterior: actualizar agentes de la cola.
```bash
python actions/action_call_queue.py --mode apply --vars '{"extension": "<extension>", "location_id": "<location_id>", "member_id": "<member_id>", "queue_id": "<queue_id>", "queue_name": "<queue_name>"}'
```

### action_day_t_numbers_caller_id.py
- Required `--vars`: `location_id, person_id, primary_number`
- Optional `--vars`: `(none)`
- Dependencias/espera de servidor: Paso previo: validar inventario y disponibilidad para external caller id. / Paso posterior: leer caller-id final para comprobar cambio.
```bash
python actions/action_day_t_numbers_caller_id.py --mode apply --vars '{"location_id": "<location_id>", "person_id": "<person_id>", "primary_number": "<primary_number>"}'
```

### action_delegated_admin.py
- Required `--vars`: `principal_id, role_id, scope`
- Optional `--vars`: `(none)`
- Dependencias/espera de servidor: Paso previo: confirmar endpoint oficial soportado en tenant/version. / Paso posterior: si no existe contrato estable => marcar out_of_scope.
```bash
python actions/action_delegated_admin.py --mode apply --vars '{"principal_id": "<principal_id>", "role_id": "<role_id>", "scope": "<scope>"}'
```

### action_devices.py
- Required `--vars`: `device_model, workspace_id`
- Optional `--vars`: `serial`
- Dependencias/espera de servidor: Paso previo: lookup por serial/MAC. / Paso posterior: confirmar asignación a persona/workspace.
```bash
python actions/action_devices.py --mode apply --vars '{"device_model": "<device_model>", "workspace_id": "<workspace_id>"}'
```

### action_group_assignment.py
- Required `--vars`: `group_id, group_name, member_id`
- Optional `--vars`: `(none)`
- Dependencias/espera de servidor: Paso previo: resolver group_id por nombre. / Paso posterior: sincronizar miembros (add/remove) de forma idempotente.
```bash
python actions/action_group_assignment.py --mode apply --vars '{"group_id": "<group_id>", "group_name": "<group_name>", "member_id": "<member_id>"}'
```

### action_hunt_group.py
- Required `--vars`: `extension, hunt_name, location_id, member_id`
- Optional `--vars`: `(none)`
- Dependencias/espera de servidor: Paso previo: lookup del hunt group. / Paso posterior: comprobar política y miembros.
```bash
python actions/action_hunt_group.py --mode apply --vars '{"extension": "<extension>", "hunt_name": "<hunt_name>", "location_id": "<location_id>", "member_id": "<member_id>"}'
```

### action_internal_extensions_sbc.py
- Required `--vars`: `location_id, route_group_id, route_group_name, trunk_id, trunk_name`
- Optional `--vars`: `(none)`
- Dependencias/espera de servidor: Paso previo: confirmar trunk/route_group existentes o crearlos. / Paso posterior: verificar internal_dialing de la sede y PSTN asociado.
```bash
python actions/action_internal_extensions_sbc.py --mode apply --vars '{"location_id": "<location_id>", "route_group_id": "<route_group_id>", "route_group_name": "<route_group_name>", "trunk_id": "<trunk_id>", "trunk_name": "<trunk_name>"}'
```

### action_interplatform_dial_plan.py
- Required `--vars`: `dial_pattern, dial_plan_name, route_group_id`
- Optional `--vars`: `(none)`
- Dependencias/espera de servidor: Paso previo: validar trunk/route_group destino. / Paso posterior: comprobar regla creada/actualizada con GET por id.
```bash
python actions/action_interplatform_dial_plan.py --mode apply --vars '{"dial_pattern": "<dial_pattern>", "dial_plan_name": "<dial_plan_name>", "route_group_id": "<route_group_id>"}'
```

### action_legacy_forwarding.py
- Required `--vars`: `forward_destination, person_id`
- Optional `--vars`: `(none)`
- Dependencias/espera de servidor: Paso previo: comprobar que el prefijo legacy enruta en dial plan. / Paso posterior: validar forwarding final en lectura de settings.
```bash
python actions/action_legacy_forwarding.py --mode apply --vars '{"forward_destination": "<forward_destination>", "person_id": "<person_id>"}'
```

### action_location_number_removal.py
- Required `--vars`: `location_id, primary_number`
- Optional `--vars`: `(none)`
- Dependencias/espera de servidor: Paso previo: verificar que número no está asignado. / Paso posterior: aceptar 404 como idempotente cuando aplique.
```bash
python actions/action_location_number_removal.py --mode apply --vars '{"location_id": "<location_id>", "primary_number": "<primary_number>"}'
```

### action_manager_assistant.py
- Required `--vars`: `assistant_person_id, person_id`
- Optional `--vars`: `(none)`
- Dependencias/espera de servidor: Paso previo: resolver executive/assistants por email. / Paso posterior: releer configuración para verificar roles/políticas.
```bash
python actions/action_manager_assistant.py --mode apply --vars '{"assistant_person_id": "<assistant_person_id>", "person_id": "<person_id>"}'
```

### action_monitoring.py
- Required `--vars`: `person_id, target_person_id`
- Optional `--vars`: `(none)`
- Dependencias/espera de servidor: Paso previo: precheck de licencia compatible. / Paso posterior: validar lista completa de monitored elements.
```bash
python actions/action_monitoring.py --mode apply --vars '{"person_id": "<person_id>", "target_person_id": "<target_person_id>"}'
```

### action_nominal_users.py
- Required `--vars`: `extension, person_id, primary_number`
- Optional `--vars`: `email`
- Dependencias/espera de servidor: Paso previo: lookup de person por email. / Paso posterior: aplicar números/caller-id solo si user existe.
```bash
python actions/action_nominal_users.py --mode apply --vars '{"extension": "<extension>", "person_id": "<person_id>", "primary_number": "<primary_number>"}'
```

### action_secondary_numbers.py
- Required `--vars`: `extension, person_id, secondary_number`
- Optional `--vars`: `(none)`
- Dependencias/espera de servidor: Paso previo: precheck de inventario de número. / Paso posterior: verificación de asignación con GET numbers.
```bash
python actions/action_secondary_numbers.py --mode apply --vars '{"extension": "<extension>", "person_id": "<person_id>", "secondary_number": "<secondary_number>"}'
```

### action_user_recording.py
- Required `--vars`: `person_id`
- Optional `--vars`: `(none)`
- Dependencias/espera de servidor: Paso previo: comprobar licencia/feature recording. / Paso posterior: confirmar modo aplicado con GET.
```bash
python actions/action_user_recording.py --mode apply --vars '{"person_id": "<person_id>"}'
```

### action_workspaces.py
- Required `--vars`: `extension, primary_number, workspace_id`
- Optional `--vars`: `workspace_name`
- Dependencias/espera de servidor: Paso previo: lookup por displayName o externalId. / Paso posterior: verificar settings de números del workspace.
```bash
python actions/action_workspaces.py --mode apply --vars '{"extension": "<extension>", "primary_number": "<primary_number>", "workspace_id": "<workspace_id>"}'
```

