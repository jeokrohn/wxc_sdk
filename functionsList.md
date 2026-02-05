DEVELOPMENT TERM SHEET SPECIFICATIONS
UNIVERSAL WEBEX BULK PROVISION BOT — Post-LDAP (Users) → Webex Calling & Telephony Features


Version: v1.0   |   Date: 2026-02-05   |   Scope: Implementation specification for developer



Scope statement


This document specifies the implementation contract for the Webex bulk provision bot to configure telephony capabilities after users already exist in Webex via LDAP synchronization. User identity creation/modification is out-of-scope; all user-level operations are performed by lookup (email) and subsequent calling/settings/assignments where supported by API.
Non-negotiables


Single CSV input (single source of truth).
Deterministic idempotency via remote lookup + upsert; re-run must not duplicate resources.
Bounded loops and retries (NASA Power of 10 adapted): static maxima for rows, batches, retries.
No manual steps: if no API/SDK exposure, mark row as pending with reason_code=out_of_scope.
Per-row terminal state exactly one of: rejected (pre-API), pending (runtime), success.
No secrets in logs; tokens read from env vars only.

Integration into program skeleton


The features in the table below are implemented as additional entity_types and steps inside the existing skeleton modules (config.py, data_pipeline.py, batch_iterator.py, connection_client.py, actions_registry.py, action_helpers.py, executor.py, error_handling.py, writers.py, state_store.py, startup_checks.py). The executor MUST preserve a fixed phase order and process only the entity_types assigned to each phase.
Phase order and entity_type mapping (fixed)


Phase 1 — Location + site-level telephony routing: location, trunk, route_group, internal_dialing, dial_plan, location_call_profiles, location_number_state, schedules, announcements_repo
Phase 2 — Existing users/workspaces calling settings: user_calling_settings, user_numbers, user_forwarding, user_recording, user_monitoring, user_exec_assistant, workspace, workspace_numbers, workspace_forwarding, workspace_recording, workspace_monitoring
Phase 3 — Shared telephony services and membership-based constructs: groups, group_membership, feature_access, call_pickup_group, call_queue, hunt_group, auto_attendant, devices, number_removal
Note: entity_type names above are implementation-side labels (CSV entity_type values). They map to concrete Webex resources via actions_registry steps.

CSV contract extensions (post-LDAP)


Baseline columns are required for all rows: entity_type, entity_key, location_key (when scoped to a location), row_ref (optional). For post-LDAP user rows, email is mandatory and is used for remote lookup. Identity fields (display_name, first_name, last_name, etc.) are rejected for user entities.
Key derivation (entity_key)


location: location_external_id if present else location_name
trunk: trunk_name (or provider-specific trunk_external_id if available)
route_group: route_group_name
dial_plan / routing_rule: rule_name (or composite: location_id + priority + pattern)
user_*: email
workspace: workspace_display_name (or workspace_external_id if available)
assignment/numbers: composite (location_id + extension) or (location_id + phone_number)
call_queue/hunt_group/auto_attendant/call_pickup_group: composite (location_id + name) or (location_id + extension)

Runtime reason codes (extensions)


In addition to the baseline error model, the following reason codes are mandatory for these features:
user_not_found: User (email) not present in Webex; LDAP sync not completed.
workspace_not_found: Workspace not present when update expected.
number_inventory_missing: Requested phone number not available in location inventory (precheck fail).
license_or_feature_missing: Required license/feature not assigned or not supported (precheck fail).
resource_dependency_missing: Prerequisite resource missing (e.g., route_group referenced by internal_dialing).
invalid_dial_plan_collision: Dial plan pattern collides with internal extension range/pattern.
sdk_method_missing: Feature not exposed by installed wxc_sdk version; treat as out_of_scope unless REST endpoint implemented.

Apartado (post-LDAP → Webex)
Subtareas / pasos intermedios necesarios (si aplica)
APIs utilizadas (SDK / endpoint clave)
Campos necesarios (por método)
Enrutamiento de extensiones internas desconocidas de la sede hacia SBC
- Precondiciones: Trunk hacia SBC creado y operativo; Route Group creado y con trunks asociados; PSTN de la sede configurado como ROUTE_GROUP/TRUNK según modelo.
- Idempotencia: lookup trunk por nombre; upsert trunk. lookup route_group por nombre; upsert route_group.
- Actualizar PSTN settings de la sede (si aplica) para usar route_group/trunk.
- Configurar internal dialing: activar 'route unknown extensions' hacia route_group_id/trunk_id.
- Validar dependencias: si route_group_id/trunk_id referenciado no existe -> pending(resource_dependency_missing).
wxc_sdk: api.telephony.prem_pstn.trunk.*
wxc_sdk: api.telephony.prem_pstn.route_group.create/update/...
wxc_sdk: api.telephony.location.update(location_id, settings=TelephonyLocation(...))
wxc_sdk: api.telephony.location.internal_dialing.update(location_id, ...)
Comunes: oauth_access_token, admin_scopes[] (spark-admin:telephony_config_write), org_id (si partner-managed).
trunk.*: trunk_id (read/update/delete) | trunk_name, sbc_address/sip_server, sip_port, transport, authentication (si aplica).
route_group.*: route_group_id (read/update/delete) | route_group_name, trunk_ids[].
location.update: location_id, settings (PSTN model: TRUNK/ROUTE_GROUP; route_group_id/trunk_id; opcional routing_prefix/outside_dial_digit si se mutan).
internal_dialing.update: location_id, internal_dialing_settings (incluye 'route_unknown_extensions' -> route_group_id/trunk_id según modelo).
Intercomunicación entre plataformas (Webex ↔ Legacy)
- Definir dial plan: patrones hacia Legacy (prefijos/patrones) + prioridad.
- Asociar acción: enviar por trunk/route_group (o route list según tenant).
- Precheck: validar que los patrones NO colisionan con extensiones internas (rango/longitud/prefijos). Si colisiona -> rejected/ pending(invalid_dial_plan_collision) según detecte pre-API vs runtime.
- Idempotencia: lookup rule por nombre o clave compuesta; upsert ruleset completo (sin diff fino).
wxc_sdk: api.telephony.prem_pstn.dial_plan.*
wxc_sdk (si expuesto): api.telephony.call_routing.* (translation patterns / rules)
wxc_sdk: api.telephony.prem_pstn.trunk.* / route_group.*
Comunes: oauth_access_token, admin_scopes[] (spark-admin:telephony_config_write), org_id (si partner-managed).
dial_plan.*: dial_plan_id (read/update/delete) | dial_plan_payload (pattern(s), action, priority, target route_group_id/trunk_id).
call_routing.* (si aplica): routing_rules_payload / translation_patterns_payload (según método).
Dependencias: trunk_id/route_group_id deben existir (si no -> pending(resource_dependency_missing)).
Alta/Modificación de usuarios Nominales (ya provisionados desde LDAP)
- Lookup person_id por email (idempotencia). Si no existe -> pending(user_not_found).
- (Opcional) Asignar licencias (incl. Calling) ANTES de settings de calling si el tenant lo requiere.
- Asegurar location_id (si el modelo fija sede por usuario).
- Configurar extensión + DDI principal + secundarios (si aplica) mediante person_settings.numbers.update.
- Configurar permisos salientes / caller ID / otras settings si están en CSV.
wxc_sdk: api.people.list(...) / api.people.update(...) (NO create en post-LDAP salvo excepción explícita)
wxc_sdk: api.person_settings.numbers.read/update(...)
wxc_sdk (si aplica): api.person_settings.permissions_out.*
wxc_sdk (si aplica): api.person_settings.caller_id.*
Comunes: oauth_access_token, org_id (si partner-managed).
people.list: admin_scopes[] (spark-admin:people_read), filtro por email/external_id.
people.update (solo post-LDAP): admin_scopes[] (spark-admin:people_write), person_id, license_assignment (incl. Calling) y/o location_id (si se fija sede).
person_settings.numbers.update: admin_scopes[] (spark-admin:telephony_config_write), person_id, extension (si cambia), phone_number_primary (si cambia), phone_number_secondary[] (si cambia). Precheck: number_inventory_exists (si se asignan E.164).
permissions_out / caller_id (si se muta): admin_scopes[] (spark-admin:telephony_config_write), person_id, payload específico.
Alta/Modificación de usuarios No Nominales (Workspaces)
- Lookup workspace por display_name o external_id (idempotencia).
- Crear/actualizar workspace.
- Asignar Calling/servicio al workspace (si el tenant lo requiere).
- Configurar números/extensión y settings de calling del workspace.
wxc_sdk: api.workspaces.list/create/update(...)
wxc_sdk: api.workspace_settings.numbers.update(workspace_id, ...)
wxc_sdk (si aplica): api.workspace_settings.permissions_out.*
wxc_sdk (si aplica): api.workspace_settings.caller_id.*
Comunes: oauth_access_token, org_id (si partner-managed).
workspaces.list: admin_scopes[] (spark-admin:workspaces_read), filtro por display_name/external_id.
workspaces.create/update: admin_scopes[] (spark-admin:workspaces_write), workspace_display_name, workspace_calling_location_id (=location_id), workspace_id (update), (si requerido) workspace_calling_license_id/plan.
workspace_settings.numbers.update: admin_scopes[] (spark-admin:telephony_config_write), workspace_id, workspace_extension (si aplica), workspace_phone_number (si aplica), phone_number_secondary[] (si aplica). Precheck: number_inventory_exists.
permissions_out / caller_id (si se muta): admin_scopes[] (spark-admin:telephony_config_write), workspace_id, payload específico.
Asignación automática de grupos (según acceso y funcionalidades)
- Resolver group_id por group_name (o crear grupo si procede y está permitido).
- Añadir/quitar miembros (batch si procede).
- (Opcional) Aplicar feature-access por persona si 'grupo funcional' implica capabilities de calling.
- Idempotencia: membership add/remove debe ser tolerante a ya-existe / no-existe.
wxc_sdk: api.groups.* / GroupsApi.list(...)
wxc_sdk: groups.membership.add/remove(...)
wxc_sdk (opcional): api.person_settings.feature_access.update(...)
Comunes: oauth_access_token, org_id (si partner-managed).
groups.*: admin_scopes[] (spark-admin:groups_read/write), group_id (read/update/delete) o group_name (create/resolve).
membership.add/remove: admin_scopes[] (spark-admin:memberships_write), group_id, person_id (o member_person_ids[] si wrapper lo soporta).
feature_access.update (opcional): admin_scopes[] (spark-admin:telephony_config_write), person_id, settings (FeatureAccessSettings).
Perfiles de llamadas (sede por defecto + por usuario + por workspace)
- Definir perfil base en sede (permisos salientes, CLID base, etc.) mediante location.update.
- Definir overrides por usuario/workspace (excepciones) mediante person/workspace settings.
- Idempotencia: upsert determinista (set payload completo por sección mutada).
wxc_sdk: api.telephony.location.update(location_id, settings=TelephonyLocation(...))
wxc_sdk: api.person_settings.permissions_out.*
wxc_sdk: api.workspace_settings.permissions_out.*
Comunes: oauth_access_token, admin_scopes[] (spark-admin:telephony_config_write), org_id (si partner-managed).
location.update: location_id, settings (location_outgoing_permissions_config, caller_id_settings, routing_prefix, outside_dial_digit, etc. solo si se mutan).
person permissions_out: person_id, entity_outgoing_permissions_override (payload).
workspace permissions_out: workspace_id, entity_outgoing_permissions_override (payload).
Numeraciones secundarias (Nominales y Workspaces)
- Precheck: números existen en inventario de la sede (number_inventory_exists).
- (Si LGW / non-integrated) activar números en sede si aplica (manage_number_state).
- Asignar secundarios a persona/workspace (numbers.update).
wxc_sdk: api.telephony.location.number.manage_number_state(...)
wxc_sdk: api.person_settings.numbers.update(...)
wxc_sdk: api.workspace_settings.numbers.update(...)
Comunes: oauth_access_token, admin_scopes[] (spark-admin:telephony_config_write), org_id (si partner-managed).
manage_number_state: location_id, phone_numbers[] (E.164), action (ACTIVATE/DEACTIVATE). Precheck: activation_required.
person numbers.update: person_id, phone_number_secondary[] (si cambia), (y primary/extension si se muta). Precheck: number_inventory_exists.
workspace numbers.update: workspace_id, phone_number_secondary[] (si cambia), (y primary/extension si se muta). Precheck: number_inventory_exists.
Servicios de grabación por usuario
- Precheck: licencia/feature de recording en la org y región disponible (si aplica).
- Configurar recording por usuario (proveedor/estado/política).
- (Si aplica) compliance announcement en sede.
wxc_sdk: api.person_settings.call_recording.read/update(...)
wxc_sdk (si aplica): api.telephony.call_recording.update_location_compliance_announcement(...)
Comunes: oauth_access_token, admin_scopes[] (spark-admin:telephony_config_write), org_id (si partner-managed).
person_settings.call_recording.update: person_id, call_recording_setting (provider, enabled, policy, notifications según modelo).
location compliance announcement (si aplica): location_id, settings (LocationComplianceAnnouncement).
Desvíos de usuarios Webex → Legacy (prefijo 53) con alta y retirada
- Definir destino legacy (formato de número/patrón).
- Precondición: prefijo 53 enruta a Legacy (dial plan / routing).
- Implementar modo idempotente: set si difiere / unset si existe (según columna del CSV).
wxc_sdk: api.person_settings.forwarding.configure(entity_id=person_id, ...)
wxc_sdk: api.workspace_settings.forwarding.configure(entity_id=workspace_id, ...)
Comunes: oauth_access_token, admin_scopes[] (spark-admin:telephony_config_write), org_id (si partner-managed).
person forwarding.configure: person_id, forwarding_enabled, forward_to_destination, idempotent_set_unset_mode.
workspace forwarding.configure: workspace_id, forwarding_enabled, forward_to_destination, idempotent_set_unset_mode.
Call Pickup Groups (si 100% SoftPhone)
- Definir grupos, extensión de pickup, y miembros (targets).
- Mantener mapping 'grupo → targets' en CSV.
- Idempotencia: lookup por (location_id + name/extension) y upsert.
wxc_sdk: api.telephony.callpickup.create/update/details/delete_pickup(...)
Comunes: oauth_access_token, admin_scopes[] (spark-admin:telephony_config_write), org_id (si partner-managed).
callpickup.create/update: location_id, call_pickup_group_name, call_pickup_extension, call_pickup_targets[].
callpickup details/delete: call_pickup_group_id (o clave equivalente).
Call Queues (Operadora, si 100% SoftPhone)
- Crear cola(s) + asignar agentes.
- (Si usáis locuciones) subir ficheros de anuncio/greetings a repo de announcements.
- Configurar idioma y caller ID externo de la cola.
- Idempotencia: lookup por (location_id + name/extension) y upsert. Agent membership update debe ser idempotente.
wxc_sdk: api.telephony.callqueue.create/update/details/delete_queue(...)
wxc_sdk (si aplica): api.telephony.announcements_repo.upload_announcement(...)
wxc_sdk (si aplica): api.telephony.callqueue.agents.update_call_queue_settings(...)
Comunes: oauth_access_token, admin_scopes[] (spark-admin:telephony_config_write), org_id (si partner-managed).
callqueue.create: location_id, call_queue_name, call_queue_extension_or_number, call_queue_language, call_queue_agents[], external_caller_id_number (si se setea), call_queue_greeting_announcement_id (si se setea).
callqueue.update/details/delete: call_queue_id.
announcements_repo.upload: name, file (bytes/path), location_id (si aplica).
agents.update_call_queue_settings: queue_id, agent_ids/settings[] (según wrapper).
Hunt Groups (Grups de Salt, si 100% SoftPhone)
- Crear HG + política de reparto + miembros.
- Definir extensión/número del grupo.
- Idempotencia: lookup por (location_id + name/extension) y upsert.
wxc_sdk: api.telephony.huntgroup.create/update/details/delete_hunt_group(...)
Comunes: oauth_access_token, admin_scopes[] (spark-admin:telephony_config_write), org_id (si partner-managed).
huntgroup.create: location_id, hunt_group_name, hunt_group_routing_policy, hunt_group_members[], hunt_group_extension_or_number.
huntgroup.update/details/delete: hunt_group_id.
Supervisión de usuarios (monitoring/BLF + opcional barge, si 100% SoftPhone)
- Identificar supervisor(es) y targets.
- Precheck: licencia/soporte de monitoring (evitar 403).
- (Opcional) aplicar barge si el tenant lo soporta.
- Idempotencia: upsert lista completa de targets por supervisor.
wxc_sdk: api.person_settings.monitoring.read/update(...)
wxc_sdk (si aplica): api.person_settings.barge.*
Comunes: oauth_access_token, admin_scopes[] (spark-admin:telephony_config_write), org_id (si partner-managed).
monitoring.update: monitoring_supervisor_person_id, monitoring_target_ids[]. Precheck: monitoring_license_supported.
barge.* (si aplica): person_id, barge_settings_payload.
Manager–Assistant (M-A): configuración Manager y Assistant
- Resolver person_id de executive y assistants por email.
- Aplicar roles y políticas (call_filter_policy / ring_options / listas).
- Idempotencia: upsert configuración completa por executive.
wxc_sdk: api.person_settings.exec_assistant.read/update(...)
Comunes: oauth_access_token, admin_scopes[] (spark-admin:telephony_config_write), org_id (si partner-managed).
exec_assistant.update: executive_person_id, assistant_person_ids[], executive_assistant_roles[], call_filter_policy, ring_options, filter_lists[], executive_service_enabled.
Operadora Automática (Auto Attendant)
- Crear schedules (business hours / holidays).
- Preparar locuciones (formato WAV válido) y subir a announcements repo.
- Crear AA + menús + acciones por horario.
- Idempotencia: lookup por (location_id + name/extension) y upsert; schedules/announcements por clave estable.
wxc_sdk: api.telephony.auto_attendant.create/update/details/delete_auto_attendant(...)
wxc_sdk: api.telephony.announcements_repo.upload_announcement(...)
wxc_sdk (si aplica): api.telephony.schedules.*
Comunes: oauth_access_token, admin_scopes[] (spark-admin:telephony_config_write), org_id (si partner-managed).
auto_attendant.create: location_id, settings (name, extension/number, schedules, menus/actions, greetings/announcement_ids, language, caller_id si aplica).
auto_attendant.update/details/delete: auto_attendant_id.
announcements_repo.upload: name, file, location_id (si aplica).
schedules.*: location_id (si aplica), schedule_payload (business_hours, holidays).
Gestores Delegados (delegated admin / location admin)
- Objetivo: asignar rol(es) admin y ámbito (sede/org).
- Estado: no hay contrato estable en wxc_sdk 1.27.1 para role assignment/delegation; si no hay endpoint soportado -> pending(out_of_scope).
- Si se implementa por REST directo: requiere discovery formal del endpoint y contrato (fuera de este spec salvo que se aporte endpoint).
No expuesto (wxc_sdk 1.27.1): role assignment / delegation.
Operación típicamente realizada en Control Hub (manual) -> en este bot: pending(out_of_scope).
N/A (sin endpoint/SDK expuesto, no hay contrato de campos estable).
Activación Día T de numeraciones (propias) + enmascaramientos (Caller ID)
- (Si LGW / non-integrated) activar números en sede (manage_number_state).
- Ajustar caller ID por entidad (location/person/workspace/queues si aplica).
- (Opcional) validar números disponibles para external caller ID antes de setear.
wxc_sdk: api.telephony.location.number.manage_number_state(...)
wxc_sdk: api.person_settings.caller_id.* / api.workspace_settings.caller_id.*
wxc_sdk (si aplica): api.telephony.location.phone_numbers_available_for_external_caller_id(...)
Comunes: oauth_access_token, org_id (si partner-managed).
manage_number_state: admin_scopes[] (spark-admin:telephony_config_write), location_id, phone_numbers[], action, activation_required (precheck).
caller_id.*: admin_scopes[] (spark-admin:telephony_config_write), person_id/workspace_id, caller_id_settings (policy + external number).
available_for_external_caller_id (si aplica): admin_scopes[] (spark-admin:telephony_config_read), location_id.
Supresión de numeraciones (propias) de la sede
- Precheck: número NO asignado a ninguna entidad (persona/workspace/servicio).
- Retirar del inventario de sede (remove numbers).
- Idempotencia: si el número no existe ya -> considerar success o pending según endpoint; 404 puede ser aceptable como idempotente.
wxc_sdk (si expuesto): api.telephony.location.numbers.remove(location_id, phone_numbers) o equivalente según versión.
Comunes: oauth_access_token, admin_scopes[] (spark-admin:telephony_config_write), org_id (si partner-managed).
remove numbers: location_id, phone_numbers[]. Precheck: number_assigned_to_entity=false.
Dispositivos (alta / asignación / activation code / gestión)
- Para teléfonos/RoomOS: crear o aprovisionar device + asociar a persona/workspace.
- Generar activation code cuando aplique.
- Idempotencia: lookup por device serial/MAC si disponible; si no, tratar como create-once y registrar device_id.
wxc_sdk: api.devices.* (Devices API)
wxc_sdk (Workspaces): api.workspace_settings.devices.*
Comunes: oauth_access_token, org_id (si partner-managed).
devices.*: admin_scopes[] (spark-admin:devices_read/write), personId o workspaceId (exactamente uno), model (si phone), y campos requeridos por el método (serial/mac, activationCode, tags).
workspace_settings.devices.*: admin_scopes[] (spark-admin:telephony_config_read/write), workspace_id, hoteling (si se muta).


Implementation notes (developer checklist)


Actions registry: each apartado above maps to one or more steps; each step must declare: success HTTP codes, minimum response fields, and which reason_code to emit on failure.
Prechecks are mandatory when referenced (number inventory, license/feature support, activation_required, dependency existence). If a precheck cannot be done via API, treat as out_of_scope (pending).
When wxc_sdk method is not present in the installed version, set pending(sdk_method_missing) unless a REST endpoint is explicitly implemented and contract-verified.
Idempotency: prefer lookup by stable keys (name, extension, E.164). If no lookup exists, the bot must persist remote_id on success and require it for updates.
All writes must be guarded by request timeouts and bounded retries (429/5xx/timeouts only).
Outputs: results.csv and pending_rows.csv are append+flush per row; checkpoint.json is written atomically (tmp + rename).

Admin scopes quick reference (minimum)


Scope
Used for
spark-admin:telephony_config_write
Telephony configuration writes (locations, trunks, route groups, dial plan, numbers, queues, AA, etc.)
spark-admin:telephony_config_read
Telephony configuration reads / prechecks (where applicable)
spark-admin:people_read
Lookup persons by email/external_id
spark-admin:people_write
Assign licenses/location or update allowed person attributes (post-LDAP only)
spark-admin:workspaces_read
Lookup workspaces
spark-admin:workspaces_write
Create/update workspaces
spark-admin:groups_read/write
Resolve/create/update groups
spark-admin:memberships_write
Add/remove group members
spark-admin:devices_read/write
Device provisioning and assignment


