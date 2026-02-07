# Mapeo de variables por script (`--vars`)

Fuente de validación:
- Implementación del repositorio (scripts en `actions/` + helper `actions/_shared.py`).
- Especificación oficial de Webex Developer capturada en `developer.webex.com/generated/full_spec.yml`.
- Referencia SDK async: `wxc_sdk/as_api.py` (base de wrappers, p.ej. `AsWebhookApi.list()`).

> Convención: **Obligatorias** = variables requeridas por este SDK para `--mode apply` (placeholders en `apply_calls`).
>
> En cada endpoint: se listan también **requeridos/opcionales del servidor** según el snapshot de docs. Si hay diferencia, `--vars` por sí solo no garantiza cumplir el contrato API.

## Revisión endpoint por endpoint (método + campos requeridos/opcionales)

- Si aparece **NO ENCONTRADO**, ese método/ruta no está en `full_spec.yml` generado y debe validarse manualmente en docs live de Webex Calling antes de usarlo en producción.

### `action_auto_attendant.py`
- `PROBE GET telephony/config/locations/{location_id}/autoAttendants`
  - `--vars` usados por script: `location_id`
  - Contrato servidor (snapshot): **NO ENCONTRADO**.
- `APPLY POST telephony/config/locations/{location_id}/autoAttendants`
  - `--vars` usados por script: `aa_name, extension, location_id, schedule_name`
  - Servidor requeridos: path=`(none)`, query=`(none)`, body=`name, businessSchedule, businessHoursMenu, afterHoursMenu`
  - Servidor opcionales: path=`(none)`, query=`orgId`, body=`phoneNumber, extension, firstName, lastName, alternateNumbers, languageCode, holidaySchedule, extensionDialing, nameDialing, timeZone`
  - Doc: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/create-an-auto-attendant

### `action_call_pickup_group.py`
- `PROBE GET telephony/config/locations/{location_id}/callPickups`
  - `--vars` usados por script: `location_id`
  - Servidor requeridos: path=`(none)`, query=`(none)`, body=`(none)`
  - Servidor opcionales: path=`(none)`, query=`orgId, max, start, order, name`, body=`(none)`
  - Doc: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/read-the-list-of-call-pickups
- `APPLY POST telephony/config/locations/{location_id}/callPickups`
  - `--vars` usados por script: `extension, location_id, member_id, pickup_name`
  - Servidor requeridos: path=`(none)`, query=`(none)`, body=`name`
  - Servidor opcionales: path=`(none)`, query=`orgId`, body=`agents`
  - Doc: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/create-a-call-pickup

### `action_call_profiles.py`
- `PROBE GET telephony/config/locations/{location_id}/callingBehavior`
  - `--vars` usados por script: `location_id`
  - Contrato servidor (snapshot): **NO ENCONTRADO**.
- `APPLY PUT telephony/config/locations/{location_id}/callingBehavior`
  - `--vars` usados por script: `location_id`
  - Contrato servidor (snapshot): **NO ENCONTRADO**.

### `action_call_queue.py`
- `PROBE GET telephony/config/locations/{location_id}/queues`
  - `--vars` usados por script: `location_id`
  - Contrato servidor (snapshot): **NO ENCONTRADO**.
- `APPLY POST telephony/config/locations/{location_id}/queues`
  - `--vars` usados por script: `extension, location_id, queue_name`
  - Servidor requeridos: path=`(none)`, query=`(none)`, body=`name, callPolicies, queueSettings, agents`
  - Servidor opcionales: path=`(none)`, query=`orgId`, body=`phoneNumber, extension, languageCode, firstName, lastName, timeZone, allowAgentJoinEnabled, phoneNumberForOutgoingCallsEnabled`
  - Doc: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/create-a-call-queue
- `APPLY PUT telephony/config/locations/{location_id}/queues/{queue_id}/agents`
  - `--vars` usados por script: `location_id, member_id, queue_id`
  - Contrato servidor (snapshot): **NO ENCONTRADO**.

### `action_day_t_numbers_caller_id.py`
- `PROBE GET telephony/config/locations/{location_id}/numbers`
  - `--vars` usados por script: `location_id`
  - Contrato servidor (snapshot): **NO ENCONTRADO**.
- `APPLY POST telephony/config/locations/{location_id}/numbers/actions/activate`
  - `--vars` usados por script: `location_id, primary_number`
  - Contrato servidor (snapshot): **NO ENCONTRADO**.
- `APPLY PUT telephony/config/people/{person_id}/callerId`
  - `--vars` usados por script: `person_id`
  - Contrato servidor (snapshot): **NO ENCONTRADO**.

### `action_delegated_admin.py`
- `PROBE GET roles`
  - `--vars` usados por script: `(none)`
  - Servidor requeridos: path=`(none)`, query=`(none)`, body=`(none)`
  - Servidor opcionales: path=`(none)`, query=`(none)`, body=`(none)`
  - Doc: https://developer.webex.com/docs/api/v1/roles/list-roles
- `APPLY POST roleAssignments`
  - `--vars` usados por script: `principal_id, role_id, scope`
  - Contrato servidor (snapshot): **NO ENCONTRADO**.

### `action_devices.py`
- `PROBE GET devices`
  - `--vars` usados por script: `serial`
  - Servidor requeridos: path=`(none)`, query=`(none)`, body=`(none)`
  - Servidor opcionales: path=`(none)`, query=`personId, workspaceId, orgId, workspaceLocationId, displayName, product, type, tag, connectionStatus, serial, software, upgradeChannel, errorCode, capability, permission, start, max`, body=`(none)`
  - Doc: https://developer.webex.com/docs/api/v1/devices/list-devices
- `APPLY POST devices`
  - `--vars` usados por script: `device_model, workspace_id`
  - Contrato servidor (snapshot): **NO ENCONTRADO**.

### `action_group_assignment.py`
- `PROBE GET groups`
  - `--vars` usados por script: `group_name`
  - Servidor requeridos: path=`(none)`, query=`(none)`, body=`(none)`
  - Servidor opcionales: path=`(none)`, query=`orgId, filter, attributes, sortBy, sortOrder, includeMembers, startIndex, count`, body=`(none)`
  - Doc: https://developer.webex.com/docs/api/v1/groups/list-and-search-groups
- `PROBE POST groups/{group_id}/members`
  - `--vars` usados por script: `group_id, member_id`
  - Contrato servidor (snapshot): **NO ENCONTRADO**.
- `APPLY POST groups`
  - `--vars` usados por script: `group_name`
  - Servidor requeridos: path=`(none)`, query=`(none)`, body=`displayName`
  - Servidor opcionales: path=`(none)`, query=`(none)`, body=`orgId, description, members`
  - Doc: https://developer.webex.com/docs/api/v1/groups/create-a-group
- `APPLY POST groups/{group_id}/members`
  - `--vars` usados por script: `group_id, member_id`
  - Contrato servidor (snapshot): **NO ENCONTRADO**.

### `action_hunt_group.py`
- `PROBE GET telephony/config/locations/{location_id}/huntGroups`
  - `--vars` usados por script: `location_id`
  - Contrato servidor (snapshot): **NO ENCONTRADO**.
- `APPLY POST telephony/config/locations/{location_id}/huntGroups`
  - `--vars` usados por script: `extension, hunt_name, location_id, member_id`
  - Servidor requeridos: path=`(none)`, query=`(none)`, body=`name, callPolicies, agents, enabled`
  - Servidor opcionales: path=`(none)`, query=`orgId`, body=`phoneNumber, extension, languageCode, firstName, lastName, timeZone`
  - Doc: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/create-a-hunt-group

### `action_internal_extensions_sbc.py`
- `PROBE GET telephony/config/locations/{location_id}/internalDialing`
  - `--vars` usados por script: `location_id`
  - Servidor requeridos: path=`(none)`, query=`(none)`, body=`(none)`
  - Servidor opcionales: path=`(none)`, query=`orgId`, body=`(none)`
  - Doc: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/read-the-internal-dialing-configuration-for-a-location
- `PROBE GET telephony/config/premisePstn/routeGroups/{route_group_id}`
  - `--vars` usados por script: `route_group_id`
  - Servidor requeridos: path=`(none)`, query=`(none)`, body=`(none)`
  - Servidor opcionales: path=`(none)`, query=`orgId`, body=`(none)`
  - Doc: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/read-a-route-group-for-a-organization
- `APPLY POST telephony/config/premisePstn/trunks`
  - `--vars` usados por script: `trunk_name`
  - Servidor requeridos: path=`(none)`, query=`(none)`, body=`name, locationId, password, trunkType`
  - Servidor opcionales: path=`(none)`, query=`orgId`, body=`dualIdentitySupportEnabled, deviceType, address, domain, port, maxConcurrentCalls`
  - Doc: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/create-a-trunk
- `APPLY POST telephony/config/premisePstn/routeGroups`
  - `--vars` usados por script: `route_group_name, trunk_id`
  - Servidor requeridos: path=`(none)`, query=`(none)`, body=`name, localGateways`
  - Servidor opcionales: path=`(none)`, query=`orgId`, body=`(none)`
  - Doc: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/create-route-group-for-a-organization
- `APPLY PUT telephony/config/locations/{location_id}/internalDialing`
  - `--vars` usados por script: `location_id, route_group_id`
  - Servidor requeridos: path=`(none)`, query=`(none)`, body=`(none)`
  - Servidor opcionales: path=`(none)`, query=`orgId`, body=`enableUnknownExtensionRoutePolicy, unknownExtensionRouteIdentity`
  - Doc: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/modify-the-internal-dialing-configuration-for-a-location

### `action_interplatform_dial_plan.py`
- `PROBE GET telephony/config/dialPlans`
  - `--vars` usados por script: `(none)`
  - Contrato servidor (snapshot): **NO ENCONTRADO**.
- `PROBE POST telephony/config/dialPlans`
  - `--vars` usados por script: `(none)`
  - Contrato servidor (snapshot): **NO ENCONTRADO**.
- `APPLY POST telephony/config/dialPlans`
  - `--vars` usados por script: `dial_pattern, dial_plan_name, route_group_id`
  - Contrato servidor (snapshot): **NO ENCONTRADO**.

### `action_legacy_forwarding.py`
- `PROBE GET telephony/config/people/{person_id}/callForwarding`
  - `--vars` usados por script: `person_id`
  - Contrato servidor (snapshot): **NO ENCONTRADO**.
- `APPLY PUT telephony/config/people/{person_id}/callForwarding`
  - `--vars` usados por script: `forward_destination, person_id`
  - Contrato servidor (snapshot): **NO ENCONTRADO**.

### `action_location_number_removal.py`
- `PROBE GET telephony/config/locations/{location_id}/numbers`
  - `--vars` usados por script: `location_id`
  - Contrato servidor (snapshot): **NO ENCONTRADO**.
- `APPLY DELETE telephony/config/locations/{location_id}/numbers`
  - `--vars` usados por script: `location_id, primary_number`
  - Servidor requeridos: path=`(none)`, query=`(none)`, body=`phoneNumbers, state`
  - Servidor opcionales: path=`(none)`, query=`orgId`, body=`(none)`
  - Doc: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/remove-phone-numbers-from-a-location

### `action_manager_assistant.py`
- `PROBE GET telephony/config/people/{person_id}/executiveAssistant`
  - `--vars` usados por script: `person_id`
  - Contrato servidor (snapshot): **NO ENCONTRADO**.
- `APPLY PUT telephony/config/people/{person_id}/executiveAssistant`
  - `--vars` usados por script: `assistant_person_id, person_id`
  - Contrato servidor (snapshot): **NO ENCONTRADO**.

### `action_monitoring.py`
- `PROBE GET telephony/config/people/{person_id}/monitoring`
  - `--vars` usados por script: `person_id`
  - Contrato servidor (snapshot): **NO ENCONTRADO**.
- `APPLY PUT telephony/config/people/{person_id}/monitoring`
  - `--vars` usados por script: `person_id, target_person_id`
  - Contrato servidor (snapshot): **NO ENCONTRADO**.

### `action_nominal_users.py`
- `PROBE GET people`
  - `--vars` usados por script: `email`
  - Servidor requeridos: path=`(none)`, query=`(none)`, body=`(none)`
  - Servidor opcionales: path=`(none)`, query=`email, displayName, id, orgId, roles, callingData, locationId, max`, body=`(none)`
  - Doc: https://developer.webex.com/docs/api/v1/people/list-people
- `PROBE PUT telephony/config/people/{person_id}/numbers`
  - `--vars` usados por script: `person_id`
  - Servidor requeridos: path=`(none)`, query=`(none)`, body=`phoneNumbers`
  - Servidor opcionales: path=`(none)`, query=`orgId`, body=`enableDistinctiveRingPattern`
  - Doc: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/assign-or-unassign-numbers-to-a-person
- `APPLY PUT telephony/config/people/{person_id}/numbers`
  - `--vars` usados por script: `extension, person_id, primary_number`
  - Servidor requeridos: path=`(none)`, query=`(none)`, body=`phoneNumbers`
  - Servidor opcionales: path=`(none)`, query=`orgId`, body=`enableDistinctiveRingPattern`
  - Doc: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/assign-or-unassign-numbers-to-a-person

### `action_secondary_numbers.py`
- `PROBE GET telephony/config/people/{person_id}/numbers`
  - `--vars` usados por script: `person_id`
  - Contrato servidor (snapshot): **NO ENCONTRADO**.
- `APPLY PUT telephony/config/people/{person_id}/numbers`
  - `--vars` usados por script: `extension, person_id, secondary_number`
  - Servidor requeridos: path=`(none)`, query=`(none)`, body=`phoneNumbers`
  - Servidor opcionales: path=`(none)`, query=`orgId`, body=`enableDistinctiveRingPattern`
  - Doc: https://developer.webex.com/docs/api/v1/webex-calling-person-settings/assign-or-unassign-numbers-to-a-person

### `action_user_recording.py`
- `PROBE GET telephony/config/people/{person_id}/callRecording`
  - `--vars` usados por script: `person_id`
  - Contrato servidor (snapshot): **NO ENCONTRADO**.
- `APPLY PUT telephony/config/people/{person_id}/callRecording`
  - `--vars` usados por script: `person_id`
  - Contrato servidor (snapshot): **NO ENCONTRADO**.

### `action_workspaces.py`
- `PROBE GET workspaces`
  - `--vars` usados por script: `workspace_name`
  - Servidor requeridos: path=`(none)`, query=`(none)`, body=`(none)`
  - Servidor opcionales: path=`(none)`, query=`orgId, workspaceLocationId, floorId, displayName, capacity, type, start, max, calling, calendar`, body=`(none)`
  - Doc: https://developer.webex.com/docs/api/v1/workspaces/list-workspaces
- `PROBE PUT telephony/config/workspaces/{workspace_id}/numbers`
  - `--vars` usados por script: `workspace_id`
  - Contrato servidor (snapshot): **NO ENCONTRADO**.
- `APPLY PUT telephony/config/workspaces/{workspace_id}/numbers`
  - `--vars` usados por script: `extension, primary_number, workspace_id`
  - Contrato servidor (snapshot): **NO ENCONTRADO**.
