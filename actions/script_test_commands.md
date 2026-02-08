# Comandos de prueba por script (laboratorio)

> Comandos listos para copiar/pegar, con datos dummy ya rellenos y formato correcto de `--vars`.
> Requiere `WEBEX_ACCESS_TOKEN` válido y recursos existentes en tenant para que `--mode apply` funcione realmente.

## Paso 0: generar usuarios dummy

```bash
python actions/generate_dummy_users.py --count 15 --domain lab.example.com --format json --output actions/dummy_users.json
python actions/generate_dummy_users.py --count 15 --domain lab.example.com --format csv --output actions/dummy_users.csv
```

## Paso 1: export de token

```bash
export WEBEX_ACCESS_TOKEN="tu_token_real"
```

## Paso 2: comandos por script (apply)

### action_auto_attendant.py
- Required `--vars`: `aa_name, extension, location_id, schedule_name`
- Optional `--vars`: `(none)`
- Dependencias/espera de servidor: Paso previo: crear/usar schedule y announcement si faltan. / Paso posterior: validar menús y horario en lectura final.
```bash
python actions/action_auto_attendant.py --mode apply --vars '{"aa_name": "AA-LAB-MADRID", "extension": "5101", "location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OUy9NQURSSUQ=", "schedule_name": "Horario-LAB-LV"}'
```

### action_call_pickup_group.py
- Required `--vars`: `extension, location_id, member_id, pickup_name`
- Optional `--vars`: `(none)`
- Dependencias/espera de servidor: Paso previo: lookup por location+name/extension. / Paso posterior: releer grupo para validar miembros.
```bash
python actions/action_call_pickup_group.py --mode apply --vars '{"extension": "5101", "location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OUy9NQURSSUQ=", "member_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9NRU1CRVIx", "pickup_name": "PG-LAB-RECEPCION"}'
```

### action_call_profiles.py
- Required `--vars`: `location_id`
- Optional `--vars`: `(none)`
- Dependencias/espera de servidor: Paso previo: confirmar entidad destino y licencia. / Paso posterior: releer configuración para confirmar estado final.
```bash
python actions/action_call_profiles.py --mode apply --vars '{"location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OUy9NQURSSUQ="}'
```

### action_call_queue.py
- Required `--vars`: `extension, location_id, member_id, queue_id, queue_name`
- Optional `--vars`: `(none)`
- Dependencias/espera de servidor: Paso previo: validar location y announcement opcional. / Paso posterior: actualizar agentes de la cola.
```bash
python actions/action_call_queue.py --mode apply --vars '{"extension": "5101", "location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OUy9NQURSSUQ=", "member_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9NRU1CRVIx", "queue_id": "Y2lzY29zcGFyazovL3VzL0NBTExfUVVFVUUvUTE=", "queue_name": "CQ-LAB-VENTAS"}'
```

### action_day_t_numbers_caller_id.py
- Required `--vars`: `location_id, person_id, primary_number`
- Optional `--vars`: `(none)`
- Dependencias/espera de servidor: Paso previo: validar inventario y disponibilidad para external caller id. / Paso posterior: leer caller-id final para comprobar cambio.
```bash
python actions/action_day_t_numbers_caller_id.py --mode apply --vars '{"location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OUy9NQURSSUQ=", "person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9OT01JTkFMMQ==", "primary_number": "+34915550101"}'
```

### action_delegated_admin.py
- Required `--vars`: `principal_id, role_id, scope`
- Optional `--vars`: `(none)`
- Dependencias/espera de servidor: Paso previo: confirmar endpoint oficial soportado en tenant/version. / Paso posterior: si no existe contrato estable => marcar out_of_scope.
```bash
python actions/action_delegated_admin.py --mode apply --vars '{"principal_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9BRE1JTjE=", "role_id": "Y2lzY29zcGFyazovL3VzL1JPTEVTL1JPTEUx", "scope": "organization"}'
```

### action_devices.py
- Required `--vars`: `device_model, workspace_id`
- Optional `--vars`: `serial`
- Dependencias/espera de servidor: Paso previo: lookup por serial/MAC. / Paso posterior: confirmar asignación a persona/workspace.
```bash
python actions/action_devices.py --mode apply --vars '{"device_model": "Cisco 8851", "workspace_id": "Y2lzY29zcGFyazovL3VzL1dPUktTUEFDRVMvV1Mx"}'
```

### action_group_assignment.py
- Required `--vars`: `group_id, group_name, member_id`
- Optional `--vars`: `(none)`
- Dependencias/espera de servidor: Paso previo: resolver group_id por nombre. / Paso posterior: sincronizar miembros (add/remove) de forma idempotente.
```bash
python actions/action_group_assignment.py --mode apply --vars '{"group_id": "Y2lzY29zcGFyazovL3VzL0dST1VQUy9HUk9VUDE=", "group_name": "LAB-GROUP-VOICE", "member_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9NRU1CRVIx"}'
```

### action_hunt_group.py
- Required `--vars`: `extension, hunt_name, location_id, member_id`
- Optional `--vars`: `(none)`
- Dependencias/espera de servidor: Paso previo: lookup del hunt group. / Paso posterior: comprobar política y miembros.
```bash
python actions/action_hunt_group.py --mode apply --vars '{"extension": "5101", "hunt_name": "HG-LAB-SOPORTE", "location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OUy9NQURSSUQ=", "member_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9NRU1CRVIx"}'
```

### action_internal_extensions_sbc.py
- Required `--vars`: `location_id, route_group_id, route_group_name, trunk_id, trunk_name`
- Optional `--vars`: `(none)`
- Dependencias/espera de servidor: Paso previo: confirmar trunk/route_group existentes o crearlos. / Paso posterior: verificar internal_dialing de la sede y PSTN asociado.
```bash
python actions/action_internal_extensions_sbc.py --mode apply --vars '{"location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OUy9NQURSSUQ=", "route_group_id": "Y2lzY29zcGFyazovL3VzL1JPVVRFX0dST1VQL1JHMQ==", "route_group_name": "RG-LAB-SBC", "trunk_id": "Y2lzY29zcGFyazovL3VzL1RSVU5LUy9UUlVOSzE=", "trunk_name": "TRUNK-LAB-MAIN"}'
```

### action_interplatform_dial_plan.py
- Required `--vars`: `dial_pattern, dial_plan_name, route_group_id`
- Optional `--vars`: `(none)`
- Dependencias/espera de servidor: Paso previo: validar trunk/route_group destino. / Paso posterior: comprobar regla creada/actualizada con GET por id.
```bash
python actions/action_interplatform_dial_plan.py --mode apply --vars '{"dial_pattern": "+3491XXXXXXX", "dial_plan_name": "DP-LAB-INTERPLATFORM", "route_group_id": "Y2lzY29zcGFyazovL3VzL1JPVVRFX0dST1VQL1JHMQ=="}'
```

### action_legacy_forwarding.py
- Required `--vars`: `forward_destination, person_id`
- Optional `--vars`: `(none)`
- Dependencias/espera de servidor: Paso previo: comprobar que el prefijo legacy enruta en dial plan. / Paso posterior: validar forwarding final en lectura de settings.
```bash
python actions/action_legacy_forwarding.py --mode apply --vars '{"forward_destination": "+34915550123", "person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9OT01JTkFMMQ=="}'
```

### action_location_number_removal.py
- Required `--vars`: `location_id, primary_number`
- Optional `--vars`: `(none)`
- Dependencias/espera de servidor: Paso previo: verificar que número no está asignado. / Paso posterior: aceptar 404 como idempotente cuando aplique.
```bash
python actions/action_location_number_removal.py --mode apply --vars '{"location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OUy9NQURSSUQ=", "primary_number": "+34915550101"}'
```

### action_manager_assistant.py
- Required `--vars`: `assistant_person_id, person_id`
- Optional `--vars`: `(none)`
- Dependencias/espera de servidor: Paso previo: resolver executive/assistants por email. / Paso posterior: releer configuración para verificar roles/políticas.
```bash
python actions/action_manager_assistant.py --mode apply --vars '{"assistant_person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9BU1NJU1RBTlQx", "person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9OT01JTkFMMQ=="}'
```

### action_monitoring.py
- Required `--vars`: `person_id, target_person_id`
- Optional `--vars`: `(none)`
- Dependencias/espera de servidor: Paso previo: precheck de licencia compatible. / Paso posterior: validar lista completa de monitored elements.
```bash
python actions/action_monitoring.py --mode apply --vars '{"person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9OT01JTkFMMQ==", "target_person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9UQVJHRVQx"}'
```

### action_nominal_users.py
- Required `--vars`: `extension, person_id, primary_number`
- Optional `--vars`: `email`
- Dependencias/espera de servidor: Paso previo: lookup de person por email. / Paso posterior: aplicar números/caller-id solo si user existe.
```bash
python actions/action_nominal_users.py --mode apply --vars '{"extension": "5101", "person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9OT01JTkFMMQ==", "primary_number": "+34915550101"}'
```

### action_secondary_numbers.py
- Required `--vars`: `extension, person_id, secondary_number`
- Optional `--vars`: `(none)`
- Dependencias/espera de servidor: Paso previo: precheck de inventario de número. / Paso posterior: verificación de asignación con GET numbers.
```bash
python actions/action_secondary_numbers.py --mode apply --vars '{"extension": "5101", "person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9OT01JTkFMMQ==", "secondary_number": "+34915550222"}'
```

### action_user_recording.py
- Required `--vars`: `person_id`
- Optional `--vars`: `(none)`
- Dependencias/espera de servidor: Paso previo: comprobar licencia/feature recording. / Paso posterior: confirmar modo aplicado con GET.
```bash
python actions/action_user_recording.py --mode apply --vars '{"person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9OT01JTkFMMQ=="}'
```

### action_workspaces.py
- Required `--vars`: `extension, primary_number, workspace_id`
- Optional `--vars`: `workspace_name`
- Dependencias/espera de servidor: Paso previo: lookup por displayName o externalId. / Paso posterior: verificar settings de números del workspace.
```bash
python actions/action_workspaces.py --mode apply --vars '{"extension": "5101", "primary_number": "+34915550101", "workspace_id": "Y2lzY29zcGFyazovL3VzL1dPUktTUEFDRVMvV1Mx"}'
```

## Paso 3: dummy ejecución sin tocar backend (opcional)

```bash
python actions/run_dummy_executions.py
```
