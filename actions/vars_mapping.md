# Mapeo de variables por script (`--vars`)

Fuente de validación:
- Implementación del repositorio (scripts en `actions/` + helper `actions/_shared.py`).
- Especificación oficial de Webex Developer capturada en `developer.webex.com/generated/full_spec.yml`.

> Convención: **Obligatorias** = requeridas para `--mode apply` en este SDK. **Opcionales** = usadas solo en `probe`.
>
> Validación adicional realizada en esta revisión: comparación de paridad entre (a) endpoint/campos del script, (b) wrappers del SDK `wxc_sdk` 1.27, y (c) endpoints publicados en `developer.webex.com/generated/full_spec.yml`.

## `action_auto_attendant.py`
- Objetivo: Orquesta prerequisitos simples (schedule/announcement) y upsert de auto attendant.
- Variables obligatorias (`apply`): `aa_name, extension, location_id, schedule_name`
- Variables opcionales (`probe-only`): `(none)`
- Paridad: ✅ endpoint y campos base (`name`, `extension`, `businessSchedule`) están alineados con SDK `AutoAttendantApi.create()` y la ruta de location.
- Endpoints tocados:
- `GET telephony/config/locations/{location_id}/autoAttendants` (probe_auto_attendant_list)
- `POST telephony/config/locations/{location_id}/autoAttendants` (upsert_auto_attendant)

## `action_call_pickup_group.py`
- Objetivo: Create/update de call pickup group y sincronización de miembros.
- Variables obligatorias (`apply`): `extension, location_id, member_id, pickup_name`
- Variables opcionales (`probe-only`): `(none)`
- Paridad: ✅ endpoint alineado con SDK `CallPickupApi.create()` en location; payload mínimo de script usa `name`, `extension`, `agents`.
- Endpoints tocados:
- `GET telephony/config/locations/{location_id}/callPickups` (probe_pickup_list)
- `POST telephony/config/locations/{location_id}/callPickups` (upsert_pickup)

## `action_call_profiles.py`
- Objetivo: Actualiza perfiles de llamada de location/person/workspace según payload simplificado.
- Variables obligatorias (`apply`): `location_id`
- Variables opcionales (`probe-only`): `(none)`
- Paridad: ⚠️ parcial. El script usa `telephony/config/locations/{location_id}/callingBehavior`; en SDK la gestión de `callingBehavior` está modelada como feature API y no aparece como wrapper de location dedicado.
- Endpoints tocados:
- `GET telephony/config/locations/{location_id}/callingBehavior` (probe_location_calling)
- `PUT telephony/config/locations/{location_id}/callingBehavior` (update_location_calling)

## `action_call_queue.py`
- Objetivo: Create/update de cola y actualización de agentes en segundo paso.
- Variables obligatorias (`apply`): `extension, location_id, member_id, queue_id, queue_name`
- Variables opcionales (`probe-only`): `(none)`
- Paridad: ⚠️ parcial. `POST .../queues` coincide con SDK `CallQueueApi.create()`, pero `PUT .../queues/{queue_id}/agents` no tiene wrapper equivalente directo en SDK 1.27 (SDK expone `telephony/config/queues/agents/...`).
- Endpoints tocados:
- `GET telephony/config/locations/{location_id}/queues` (probe_queue_list)
- `POST telephony/config/locations/{location_id}/queues` (upsert_queue)
- `PUT telephony/config/locations/{location_id}/queues/{queue_id}/agents` (queue_agents_update)

## `action_day_t_numbers_caller_id.py`
- Objetivo: Activa números de sede y aplica caller-id básico por entidad.
- Variables obligatorias (`apply`): `location_id, person_id, primary_number`
- Variables opcionales (`probe-only`): `(none)`
- Paridad: ❌ desalineación en activación de números: script usa `POST .../numbers/actions/activate`, SDK 1.27 usa `PUT .../locations/{location_id}/numbers` con body `{"phoneNumbers": [...], "action": "ACTIVATE"}`.
- Endpoints tocados:
- `GET telephony/config/locations/{location_id}/numbers` (probe_location_numbers)
- `POST telephony/config/locations/{location_id}/numbers/actions/activate` (activate_numbers)
- `PUT telephony/config/people/{person_id}/callerId` (update_person_caller_id)

## `action_delegated_admin.py`
- Objetivo: Documenta y prueba de viabilidad mínima para delegated admin (sin contrato estable en SDK).
- Variables obligatorias (`apply`): `principal_id, role_id, scope`
- Variables opcionales (`probe-only`): `(none)`
- Paridad: ⚠️ parcial. `roles` sí está en SDK (`RolesApi`), pero `roleAssignments` no tiene wrapper SDK 1.27.
- Endpoints tocados:
- `GET roles` (probe_org_roles)
- `POST roleAssignments` (attempt_delegate_assignment)

## `action_devices.py`
- Objetivo: Prueba alta o asignación de dispositivos con payload mínimo.
- Variables obligatorias (`apply`): `device_model, workspace_id`
- Variables opcionales (`probe-only`): `serial`
- Paridad: ✅ para campos usados (`model`, `workspaceId`) y endpoint `devices` con SDK `DevicesApi` (create by MAC/activation code).
- Endpoints tocados:
- `GET devices` (probe_devices)
- `POST devices` (create_or_assign_device)

## `action_group_assignment.py`
- Objetivo: Valida lookup y upsert de grupos + membresías idempotentes.
- Variables obligatorias (`apply`): `group_id, group_name, member_id`
- Variables opcionales (`probe-only`): `(none)`
- Paridad: ⚠️ parcial. SDK usa `GroupsApi` sobre `groups`, pero membresía se gestiona vía `PATCH /groups/{id}` (objeto group), no con `POST /groups/{group_id}/members` como en script.
- Endpoints tocados:
- `GET groups` (lookup_group)
- `POST groups/{group_id}/members` (probe_membership_add)
- `POST groups` (upsert_group)
- `POST groups/{group_id}/members` (add_membership)

## `action_hunt_group.py`
- Objetivo: Create/update de hunt group con política de routing y miembros.
- Variables obligatorias (`apply`): `extension, hunt_name, location_id, member_id`
- Variables opcionales (`probe-only`): `(none)`
- Paridad: ✅ endpoint de location y campos base alineados con SDK `HuntGroupApi.create()`.
- Endpoints tocados:
- `GET telephony/config/locations/{location_id}/huntGroups` (probe_hunt_list)
- `POST telephony/config/locations/{location_id}/huntGroups` (upsert_hunt_group)

## `action_internal_extensions_sbc.py`
- Objetivo: Valida y ejecuta trunk + route group + internal dialing para enrutar extensiones internas desconocidas.
- Variables obligatorias (`apply`): `location_id, route_group_id, route_group_name, trunk_id, trunk_name`
- Variables opcionales (`probe-only`): `(none)`
- Paridad: ⚠️ parcial. Trunk y Route Group coinciden; `internalDialing` también. Pero payload de script para `unknownExtensionRouteIdentity` usa string, mientras SDK modela objeto `RouteIdentity`.
- Endpoints tocados:
- `GET telephony/config/locations/{location_id}/internalDialing` (probe_missing_location)
- `GET telephony/config/premisePstn/routeGroups/{route_group_id}` (probe_missing_route_group)
- `POST telephony/config/premisePstn/trunks` (upsert_trunk_like)
- `POST telephony/config/premisePstn/routeGroups` (upsert_route_group_like)
- `PUT telephony/config/locations/{location_id}/internalDialing` (update_internal_dialing)

## `action_interplatform_dial_plan.py`
- Objetivo: Valida y aplica reglas de dial plan contra Legacy con control básico de colisiones vía respuesta API.
- Variables obligatorias (`apply`): `dial_pattern, dial_plan_name, route_group_id`
- Variables opcionales (`probe-only`): `(none)`
- Paridad: ❌ desalineación de endpoint: script usa `telephony/config/dialPlans`; SDK 1.27 usa `telephony/config/premisePstn/dialPlans` (`DialPlanApi`).
- Endpoints tocados:
- `GET telephony/config/dialPlans` (probe_dial_plan_list)
- `POST telephony/config/dialPlans` (probe_invalid_target)
- `POST telephony/config/dialPlans` (create_or_update_dial_plan)

## `action_legacy_forwarding.py`
- Objetivo: Configura o desconfigura desvío a prefijo legacy (ej. 53) en persona/workspace.
- Variables obligatorias (`apply`): `forward_destination, person_id`
- Variables opcionales (`probe-only`): `(none)`
- Paridad: ⚠️ parcial. Script usa `telephony/config/people/{person_id}/callForwarding`; SDK `ForwardingApi` usa endpoint de feature (`.../features/callForwarding`) con mapeos internos según entidad.
- Endpoints tocados:
- `GET telephony/config/people/{person_id}/callForwarding` (probe_forwarding)
- `PUT telephony/config/people/{person_id}/callForwarding` (update_forwarding)

## `action_location_number_removal.py`
- Objetivo: Precheck mínimo y eliminación idempotente de números de inventario.
- Variables obligatorias (`apply`): `location_id, primary_number`
- Variables opcionales (`probe-only`): `(none)`
- Paridad: ✅ endpoint y body `phoneNumbers` alineados con SDK `LocationNumbersApi.remove()`.
- Endpoints tocados:
- `GET telephony/config/locations/{location_id}/numbers` (probe_number_inventory)
- `DELETE telephony/config/locations/{location_id}/numbers` (remove_numbers)

## `action_manager_assistant.py`
- Objetivo: Configura relación executive/assistants usando update idempotente completo.
- Variables obligatorias (`apply`): `assistant_person_id, person_id`
- Variables opcionales (`probe-only`): `(none)`
- Paridad: ⚠️ parcial. Script usa `telephony/config/people/{person_id}/executiveAssistant`; SDK `exec_assistant` va por endpoint de feature de persona.
- Endpoints tocados:
- `GET telephony/config/people/{person_id}/executiveAssistant` (probe_exec_assistant)
- `PUT telephony/config/people/{person_id}/executiveAssistant` (update_exec_assistant)

## `action_monitoring.py`
- Objetivo: Actualiza targets de monitoring y prueba errores de soporte/licencia.
- Variables obligatorias (`apply`): `person_id, target_person_id`
- Variables opcionales (`probe-only`): `(none)`
- Paridad: ⚠️ parcial. Script usa `telephony/config/people/{person_id}/monitoring`; SDK `MonitoringApi` usa endpoint de feature y serializa `monitoredElements` como lista de IDs.
- Endpoints tocados:
- `GET telephony/config/people/{person_id}/monitoring` (probe_monitoring)
- `PUT telephony/config/people/{person_id}/monitoring` (update_monitoring)

## `action_nominal_users.py`
- Objetivo: Resuelve usuario por email y prueba updates de calling/números sin crear identidad.
- Variables obligatorias (`apply`): `extension, person_id, primary_number`
- Variables opcionales (`probe-only`): `email`
- Paridad: ✅ `people` lookup y `telephony/config/people/{person_id}/numbers` alineados con SDK (`PeopleApi` + `NumbersApi`).
- Endpoints tocados:
- `GET people` (lookup_user)
- `PUT telephony/config/people/{person_id}/numbers` (probe_user_numbers_missing)
- `PUT telephony/config/people/{person_id}/numbers` (update_user_numbers)

## `action_secondary_numbers.py`
- Objetivo: Prueba asignación/remoción de números secundarios en persona/workspace.
- Variables obligatorias (`apply`): `extension, person_id, secondary_number`
- Variables opcionales (`probe-only`): `(none)`
- Paridad: ✅ endpoint `telephony/config/people/{person_id}/numbers` alineado; revisar contrato exacto de body para `additionalNumbers` según tenant/version.
- Endpoints tocados:
- `GET telephony/config/people/{person_id}/numbers` (probe_person_numbers)
- `PUT telephony/config/people/{person_id}/numbers` (update_person_numbers)

## `action_user_recording.py`
- Objetivo: Actualiza grabación de usuario y captura errores comunes de licencia.
- Variables obligatorias (`apply`): `person_id`
- Variables opcionales (`probe-only`): `(none)`
- Paridad: ⚠️ parcial. Script usa `telephony/config/people/{person_id}/callRecording`; SDK `CallRecordingApi` usa endpoint de feature.
- Endpoints tocados:
- `GET telephony/config/people/{person_id}/callRecording` (probe_recording)
- `PUT telephony/config/people/{person_id}/callRecording` (update_recording)

## `action_workspaces.py`
- Objetivo: Lookup/create/update de workspace y update de numeración de calling.
- Variables obligatorias (`apply`): `extension, primary_number, workspace_id`
- Variables opcionales (`probe-only`): `workspace_name`
- Paridad: ✅ `workspaces` lookup y `telephony/config/workspaces/{workspace_id}/numbers` alineados con SDK `WorkspaceNumbersApi.update()`.
- Endpoints tocados:
- `GET workspaces` (lookup_workspace)
- `PUT telephony/config/workspaces/{workspace_id}/numbers` (probe_workspace_numbers_missing)
- `PUT telephony/config/workspaces/{workspace_id}/numbers` (update_workspace_numbers)
