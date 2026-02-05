# UNIVERSAL EXECUTABLE SPEC TERM SHEET (WEBEX BULK PROVISION BOT)

(API SCRIPT/BOT — RESILIENT, AUTONOMOUS, NASA POWER OF 10 COMPLIANT)
**REQUEST FOR DEVELOPMENT (implementación directa, sin investigación adicional)**

---

## 1) ALCANCE OPERATIVO

### IN-SCOPE (el bot debe hacer)

* Aprovisionamiento **100% automatizado** (sin pasos manuales) de:

  * **Locations**
  * **Users**
  * **Extensions / números / asignaciones**
  * **Configuraciones Calling** exigidas por la especificación (policies/settings) siempre que exista operación API.
* Ejecución resiliente para CSVs de **3.000–21.000** filas:

  * batching (default 500),
  * continue-on-error por fila,
  * reinicio seguro con checkpoint,
  * sin bloqueos (timeouts obligatorios),
  * sin crash por fallos externos.
* Idempotencia basada en **estado remoto**:

  * lookup por clave estable,
  * upsert determinista (create si no existe / update si existe),
  * re-ejecutar el mismo CSV no cambia el estado final.
* Artefactos obligatorios:

  * `results.csv` (append seguro)
  * `pending_rows.csv` (append seguro, con motivo)
  * `rejected_rows.csv` (errores de datos pre-API)
  * `checkpoint.json` (reanudación)

### OUT-OF-SCOPE (el bot no hace)

* UI, dashboards, multi-tenant/multi-org.
* Provisioning de credenciales / OAuth app registration / secret storage (solo consumo vía env vars).
* “Manual post-steps”: no existen.

  * Si una acción no es automatizable por API ⇒ fila a `pending_rows.csv` con `reason_code` explícito.
* Corrección inventada de datos (solo normaliza/valida; si falla ⇒ rejected/pending).
* Rollback perfecto garantizado (compensación opcional y segura únicamente).

---

## 2) PROPÓSITO Y GARANTÍAS

**Propósito**: programa autónomo para alta masiva de Webex (locations/users/extensions/config) que permita “activar una sede completa” sin operación manual.

**Garantías terminales**

* No crash por fallos externos.
* No bloqueo indefinido.
* Cada fila termina exactamente en: `success` (results) o `pending` o `rejected`.
* Reinicio/relanzado: reanuda desde checkpoint sin duplicar entidades (lookup+upsert).

---

## 3) MODELO DE EJECUCIÓN (FASES FIJAS)

### 3.1 Fases obligatorias (orden fijo, sin grafo de dependencias)

* **Fase 1: Locations** (crear/actualizar)
* **Fase 2: Users** (crear/actualizar + habilitar Calling si aplica)
* **Fase 3: Extensions / Números / Asignaciones + settings finales**

La ejecución debe respetar este orden, procesando el CSV en modo “filtrado por entity_type” o mediante tres runs internos sobre el mismo input.

### 3.2 Batching + límites estáticos

* Batches con tamaño fijo (default 500) y límites estáticos:

  * `MAX_ROWS`, `MAX_BATCHES`, `MAX_RETRIES`.
* Flujo:

  1. pipeline de datos (pre-API)
  2. ejecución por fase → por batch → por fila
  3. persistencia incremental de resultados + pending + checkpoint

---

## 4) CONTRATO ÚNICO DE ENTRADA (OBLIGATORIO)

### 4.1 Un solo CSV (single source of truth)

* Se define **un único CSV** con columnas mínimas para cubrir:

  * `location`
  * `user`
  * `extension/number`
  * `calling_settings` (solo lo que se va a aplicar en esta primera activación)

### 4.2 Validación estricta pre-API

* El pipeline debe validar:

  * columnas requeridas por `entity_type`,
  * tipos/patrones (email, extensión, etc.),
  * unicidad mínima por clave estable,
  * normalización mínima determinista.
* Si falla ⇒ `rejected_rows.csv` con `reason_code` y `reason_message`.

**Entregable explícito**: `input_schema.md` (schema versionado) que define exactamente:

* columnas por entidad,
* obligatorias/opcionales,
* reglas de unicidad mínimas.

---

## 5) NASA POWER OF 10 — REGLAS RUNTIME (OBLIGATORIAS)

* Validación de inputs al entrar en funciones críticas.
* Validación mínima de respuestas API antes de usar contenido.
* Invariantes tras mutaciones locales:

  * writers y checkpoint consistentes,
  * progreso “done” solo tras éxito real.
* Loops acotados (sin loops infinitos).
* Retries acotados y visibles en logs.
* Sin ejecución dinámica/reflection.
* Assertions habilitadas en producción:

  * fallo ⇒ degradación controlada (pending + log), nunca crash.

---

## 6) IDENTITY + IDEMPOTENCIA (REMOTE-STATE FOCUSED)

### 6.1 Claves estables (obligatorias)

* User: `email`
* Location: `location_name` o `location_external_id`
* Extension/Number: clave compuesta (p.ej. `location_id + extension` o `location_id + number`)

### 6.2 Regla de idempotencia (mínima, sin “diff” completo)

Por cada fila y entidad:

* **Lookup remoto por clave estable**.
* Si existe ⇒ usar `remote_id` y ejecutar **update** determinista.
* Si no existe ⇒ **create** y persistir `remote_id` en results.

No se exige comparación campo-a-campo “desired vs actual”. La no duplicación se resuelve con lookup + upsert.

---

## 7) ESTADO Y REANUDACIÓN (CHECKPOINT SIMPLE POR FASE)

### 7.1 Reglas mínimas anti-corrupción

* Nunca crear sin lookup previo por clave estable.
* Guardar progreso solo después de éxito del conjunto de calls requeridos para esa fila.

### 7.2 Checkpoint mínimo (sin ingeniería extra)

`checkpoint.json` debe incluir como mínimo:

* `phase`
* `last_row_id`
* `input_hash`

En `resume`, reanudar desde checkpoint y repetir lookup+upsert:

* evita duplicados tras crash,
* completa filas “half-applied” sin complejidad adicional.

---

## 8) MODELO DE ERRORES (SIMPLIFICADO)

### 8.1 Clases

* **RETRYABLE_EXTERNAL**: timeouts, network, 429, 5xx.
* **NON_RETRYABLE_EXTERNAL**: 4xx por datos/permiso/contrato, auth inválida persistente.
* **ASSERTION_FAILURE**: invariantes locales/bug detectado por assertion.

### 8.2 Reglas

* Retryable ⇒ retry acotado (tenacity) y si se agota ⇒ `pending_rows.csv`.
* Non-retryable ⇒ `pending_rows.csv` sin retry ciego.
* Assertion failure ⇒ `pending_rows.csv` + log crítico y continuar.

No se implementa contador de intentos como feature persistida. Los retries se registran en logs.

---

## 9) RETRY & TIMEOUTS (TENACITY) — ACOTADO

* Timeouts obligatorios por request (no bloqueos).
* Tenacity: exponential backoff + jitter.
* Máximo de retries configurable y fijo.
* Exhaustión ⇒ pending + continuar.

---

## 10) STARTUP SAFETY CHECKS (PRE-FLIGHT MÍNIMO) — OBLIGATORIO

Antes de procesar miles de filas:

* Validar env vars requeridas (token/base_url/org si aplica).
* Ejecutar 1–2 llamadas baratas para confirmar:

  * token válido,
  * base_url correcto (LAB/PROD),
  * permisos/scopes efectivos (en la medida que la API lo refleje).
    Si falla ⇒ salida controlada antes de procesar filas.

---

## 11) CIRCUIT BREAKER (SIMPLE, OBLIGATORIO)

* Si en un batch supera un umbral de `NON_RETRYABLE_EXTERNAL` por permisos/auth (p.ej. 80%):

  * finalizar ejecución controladamente,
  * checkpoint hasta último batch completo,
  * log crítico con causa probable (token/scopes/org/base_url).

---

## 12) CONTRATO DE ENTRADAS/SALIDAS

### Input

* Un CSV con schema definido en `input_schema.md`.
* Config por env vars (LAB/PROD sin cambios de código).

### Output files (obligatorios)

* `rejected_rows.csv`: inválidas antes de tocar Webex (`reason_code`, `reason_message`).
* `results.csv` (append seguro): `timestamp,batch_id,row_id,phase,entity_type,entity_key,step,status,http_status,message,remote_id`.
* `pending_rows.csv` (append seguro): `timestamp,batch_id,row_id,phase,entity_type,entity_key,step,reason_code,reason_message,http_status,raw_row_minified`.
* `checkpoint.json`: `input_hash,pipeline_version,phase,last_row_id,started_at`.

---

## 13) SUCCESS CONDITION POR ENDPOINT (OBLIGATORIO)

Cada step define éxito por:

* HTTP status esperado, y
* presencia de campos mínimos (p.ej. `id`) cuando aplique.
  No se depende de mensajes de texto.

---

## 14) ESTRUCTURA DE MÓDULOS (MÍNIMA, SIN “GOD MODULES”)

* `config.py`: carga env vars + defaults seguros.
* `data_pipeline.py`: ingest/normalize/validate/dedupe → ready/rejected.
* `batch_iterator.py`: streaming + batches + bounds.
* `connection_client.py`: request() único con timeouts + tenacity + validación response.
* `actions_registry.py`: steps declarativos por fase (endpoints/payload builder/success condition).
* `action_helpers.py`: lógica pura (payload builders/normalizadores).
* `executor.py`: orquestación fase→batch→row→steps, lookup+upsert, writes + checkpoint.
* `error_handling.py`: mapping a `reason_code` mínimo (8–10 códigos prácticos).
* `writers.py`: append seguro results/pending/rejected.
* `state_store.py`: checkpoint atómico (tmp + rename).
* `startup_checks.py`: preflight mínimo antes del run.

---

## 15) ROLLBACK / COMPENSATION (LO MÁS CONVENIENTE: MÍNIMO)

* Por defecto: **sin rollback automático**.
* Si una fila queda “half-applied”:

  * se registra como pending con `reason_code=half_applied`,
  * la re-ejecución (lookup+upsert) completa lo pendiente sin duplicar.
* Compensación opcional solo si:

  * es segura (delete idempotente y soportado),
  * se activa por config (`ENABLE_SAFE_COMPENSATION=true`).

---

## 16) LOGGING (MÍNIMO, SUFICIENTE)

* Structured logs (key=value o JSON).
* Eventos mínimos:

  * inicio/fin de fase y batch,
  * errores por fila (`entity_key`, `step`, `http_status` si aplica),
  * retry attempts y agotamiento,
  * circuit breaker trigger,
  * assertion failures,
  * resultado de startup safety checks.
* Sin log spam loops.

---

## 17) TESTING (MÍNIMO, PERO SUFICIENTE PARA CERTEZA)

### 17.1 Unit (sin red)

* pipeline (validación/normalización)
* writers/checkpoint
* iterator
* error mapping

### 17.2 Behavioural (mock HTTP) — 6 escenarios mínimos

1. create success
2. update success
3. 429→retry→success
4. 5xx→retry agotado→pending
5. 4xx→pending sin retry
6. crash/restart simulado→resume sin duplicar (lookup+upsert)

---

## 18) CRITERIOS DE ACEPTACIÓN

* Ejecuta sobre 21.000 filas sin crash por fallos externos.
* No bloqueos (timeouts siempre).
* Fases respetadas: locations → users → extensions/settings.
* Cada fila termina en results/pending/rejected con trazabilidad completa.
* Re-ejecución del mismo CSV no duplica entidades (lookup+upsert).
* Startup safety checks previenen runs inválidos.
* Reanudación desde checkpoint funciona y no corrompe outputs.

## bulk_after_users

UNIVERSAL WEBEX BULK PROVISION BOT\
TERM SHEET — v1.1 — 2026-02-05 — usuarios provisionados por LDAP (fuera de scope).\
REQUEST FOR DEVELOPMENT

Objetivo operativo: ejecutar alta completa de sede/location (locations → usuarios existentes → extensiones/números/settings) vía API, a gran escala, sin intervención manual y con validación en remoto.

Modificación de alcance (obligatoria): los usuarios se cargan desde LDAP fuera del scope del proyecto. El bot NO crea ni modifica identidad de usuarios. Solo opera sobre usuarios ya existentes en Webex (lookup por email) para habilitar/configurar Calling y realizar asignaciones de extensiones/números/settings definidas por el CSV.

### 0) DEFINICIONES

Fila: registro del CSV que representa una unidad de trabajo para una entidad en una fase (entity_type + entity_key).

Entidad: recurso Webex a crear/actualizar/configurar. Tipos mínimos: location, user (existente por LDAP), extension_assignment (o equivalente).

Clave estable (entity_key): identificador determinista para lookup remoto antes de mutar.

Fase: etapa fija del run (1=locations, 2=users_existing_calling, 3=extensions/settings).

Step: llamada API concreta dentro de una fila (p. ej. user_lookup, enable_calling, apply_calling_settings, assign_extension).

Estado final por fila: exactamente uno de: rejected (pre-API), pending (fallo durante ejecución o no automatizable), success (completada).

Half-applied: algunos steps success y otros fallan → fila pending con reason_code=half_applied.

### 1) ALCANCE OPERATIVO

#### 1.1 IN-SCOPE (el bot debe hacer)

Provisión 100% automatizada (sin post-steps manuales) de:

Locations (sede/ubicación)

Create/update de locations.

Captura y persistencia de remote_id por location.

Users (existentes por LDAP)

Lookup por email (user_lookup).

Aplicar Calling enable y calling settings SOLO si el usuario existe y si hay operación API para el ajuste requerido.

El bot NO ejecuta user_create ni user_update de identidad (nombre, atributos de perfil, etc.).

Extensions / números / asignaciones + settings finales

Asignar extensión y/o número al usuario o recurso según el contrato del CSV.

Aplicar settings finales definidos por el CSV (solo los soportados por API).

Ejecución resiliente para CSVs de 3.000–21.000 filas

Batching fijo (BATCH_SIZE provisional=500).

Continue-on-error por fila.

Reanudación segura con checkpoint.

Timeouts obligatorios por request.

No crash por fallos externos.

Idempotencia por estado remoto (mínima y suficiente)

Lookup por clave estable antes de create/update/config.

Upsert determinista: si existe → update/config; si no existe → create SOLO para entidades creables (p. ej. location).

Re-ejecutar el mismo CSV no duplica entidades.

Para user inexistente (LDAP no sincronizado): NO crear; marcar pending con reason_code=user_not_found.

Artefactos obligatorios (re-procesables)

results.csv (append seguro).

pending_rows.csv (append seguro, con motivo y step).

rejected_rows.csv (fallos pre-API).

checkpoint.json (reanudación).

#### 1.2 OUT-OF-SCOPE (el bot no hace)

UI/dashboards.

Multi-tenant/multi-org.

Provisioning de credenciales/OAuth app/secret storage (solo consume env vars).

Pasos manuales: prohibidos. Si no existe operación API → pending con reason_code=out_of_scope.

Inventar datos faltantes: si no cumple schema/validación → rejected.

Rollback perfecto: no garantizado (ver Rollback mínimo).

Usuarios (identidad) fuera de scope: creación, modificación de atributos de identidad, forzar sincronización LDAP, lifecycle de usuario fuera de calling/settings.

### 2) PROPÓSITO Y GARANTÍAS

#### 2.1 Propósito

Automatizar lo que hoy hace inviable la ejecución manual: activar completamente una sede/location a gran escala, con un programa único, determinista, reiniciable y seguro, asumiendo usuarios preexistentes (LDAP).

#### 2.2 Garantías terminales (no negociables)

No crash por fallos externos.

No bloqueo indefinido (timeouts).

Cada fila termina exactamente en uno de: rejected / pending / success.

Restart safe: reinicio o re-run no duplica entidades (lookup+upsert).

### 3) MODELO DE EJECUCIÓN

#### 3.1 Fases

Fase 1: Locations — objetivo: que todas las locations requeridas existan en Webex y tengan remote_id.

Fase 2: Users (existentes) — objetivo: usuarios ya existentes con calling habilitado/config aplicado si procede. Si user_lookup no encuentra → pending user_not_found.

Fase 3: Extensions / Numbers / Assignments + settings finales — objetivo: asignaciones de extensión/número y ajustes finales definidos por el CSV.

Procesamiento por entity_type (definición)

Procesar todas las filas entity_type=location.

Procesar todas las filas entity_type=user.

Procesar todas las filas entity_type=extension_assignment (o equivalente).

#### 3.2 Batching + límites estáticos

Clave

Valor

BATCH_SIZE (provisional)

500

MAX_ROWS (provisional)

21000

MAX_BATCHES (provisional)

ceil(MAX_ROWS/BATCH_SIZE); tope adicional opcional MAX_BATCHES=1000

MAX_RETRIES por request (provisional)

5

Regla: ningún bucle puede superar estos límites. Si se alcanza un límite → salida controlada con checkpoint.

### 4) CONTRATO ÚNICO DE ENTRADA (CSV) — DEFINICIÓN PROVISIONAL (OBLIGATORIA)

#### 4.1 Un único CSV (single source of truth)

El bot consumirá un solo CSV como input. Debe contener las filas de todas las fases.

#### 4.2 Columnas mínimas (definición provisional)

Comunes (todas las filas)

entity_type ∈ {location, user, extension_assignment}

entity_key (derivado o explícito; ver sección 6)

location_key (para user y extension_assignment; p. ej. nombre o external_id)

row_ref (opcional; si no existe se usa índice de lectura como row_id)

Location

location_name (obligatorio si no hay location_external_id)

location_external_id (opcional pero recomendado)

time_zone (obligatorio)

address_* (campos mínimos acordados; si faltan → rejected)

User (existente, LDAP)

email (obligatorio)

location_key (obligatorio)

calling_enabled (provisional boolean; default true)

calling_settings_* (solo campos realmente aplicados)

Restricción de scope: si aparecen campos de identidad (p. ej. display_name, first_name, last_name, etc.) → rejected con reason_code=out_of_scope.

Extension / Number assignment

email (clave del usuario) o user_key equivalente (obligatorio)

extension y/o phone_number (al menos uno, según política)

location_key (obligatorio)

#### 4.3 Reglas de validación pre-API (provisional)

email: formato válido.

location_key: no vacío.

entity_type: en enumeración.

extension: numérica y dentro de rango definido (provisional: 2–8 dígitos).

phone_number: formato acordado (si E.164 requerido, se valida).

Unicidad mínima: user.email único en el CSV; location_key único para filas location; extension único por location_key (si aplica).

Salida si falla: fila a rejected_rows.csv con reason_code + reason_message.

Entregable obligatorio: input_schema.md (con esta definición formalizada y cerrada antes de codear).

### 5) REGLAS RUNTIME

#### 5.1 Validaciones en runtime

Validar inputs en entrypoints críticos (executor, client, writers, state_store).

Validar respuestas API mínimas: status esperado, JSON parseable, campos mínimos presentes cuando aplican.

#### 5.2 Invariantes internos (provisional)

Nunca marcar success sin completar todos los steps obligatorios de la fase para esa fila.

Nunca escribir checkpoint “avanzado” sin haber persistido results/pending de la fila actual.

Nunca ejecutar loops sin límites configurados (sección 3.2).

Fallo de invariante: pending + log crítico, continuar.

### 6) IDENTITY + IDEMPOTENCIA (REMOTE-STATE FOCUSED)

#### 6.1 Claves estables

Location: location_external_id si existe; si no location_name.

User: email (usuario existente por LDAP).

Assignment: (location_id, extension) o (location_id, phone_number) según lo que se asigne.

#### 6.2 Regla de idempotencia

Por cada fila: lookup remoto por clave estable.

Si existe → remote_id y ejecutar update/config determinista.

Si no existe → create SOLO si la entidad es creable (p. ej. location).

User inexistente: NO crear; registrar pending con reason_code=user_not_found.

Nota: No se implementa diff “desired vs actual”. Upsert determinista + re-run es el mecanismo.

### 7) ESTADO Y REANUDACIÓN — CHECKPOINT SIMPLE POR FASE

#### 7.1 Checkpoint (definición provisional cerrada)

checkpoint.json contendrá:

pipeline_version (provisional=1)

input_hash (sha256 del contenido del CSV)

phase ∈ {1,2,3}

last_row_id (entero, índice secuencial de filas procesadas en esa fase)

started_at (timestamp)

updated_at (timestamp)

#### 7.2 Semántica de reanudación

Si input_hash cambia → el bot debe abortar controladamente o iniciar run nuevo (definición: abortar con log crítico).

En resume: volver a ejecutar desde phase y last_row_id+1, manteniendo lookup+upsert para evitar duplicados.

### 8) MODELO DE ERRORES (SIMPLIFICADO, OPERATIVO)

#### 8.1 Clases (cerradas)

RETRYABLE_EXTERNAL: 429, 5xx, timeout, network.

NON_RETRYABLE_EXTERNAL: 4xx no recuperable (permiso/contrato/datos).

ASSERTION_FAILURE: invariantes internas.

#### 8.2 Reason codes (cerrados)

reason_code

status

uso

invalid_input_schema

rejected

schema/validación pre-API falla

duplicate_key

rejected

colisión de claves (CSV)

out_of_scope

pending

operación no disponible por API o fuera del alcance

non_retryable_external

pending

4xx no recuperable en ejecución

permission_denied

pending

permisos insuficientes

auth_invalid

pending

token inválido/expirado

retry_exhausted

pending

reintentos agotados en error retryable

invalid_response_schema

pending

respuesta OK pero faltan campos mínimos

half_applied

pending

parcialmente aplicado

unhandled_exception

pending

excepción no contemplada

user_not_found

pending

usuario no existe en Webex (LDAP aún no sincronizado)

precondition_missing

pending

precondición no satisfecha (p. ej. licencia/servicio requerido para calling)

#### 8.3 Política cerrada

Si RETRYABLE_EXTERNAL → retry acotado; si agota → pending (retry_exhausted).

Si NON_RETRYABLE_EXTERNAL → pending directo (non_retryable_external / permission_denied / auth_invalid según mapeo).

Si assertion/unhandled → pending + continuar.

### 9) RETRY & TIMEOUTS (TENACITY) — DEFINICIÓN PROVISIONAL

#### 9.1 Timeouts (provisional)

Clave

Valor

REQUEST_TIMEOUT_SECONDS

20

CONNECT_TIMEOUT_SECONDS (si aplica)

5

#### 9.2 Retries (provisional)

MAX_RETRIES (provisional=5).

Backoff: exponencial con jitter (tenacity standard).

Reintentar solo si status ∈ {429, 500–599} o timeout/network.

#### 9.3 Exhaustión

Registrar pending con reason_code=retry_exhausted, step y http_status si existe.

### 10) STARTUP SAFETY CHECKS (PRE-FLIGHT)

Pasos antes de procesar la primera fila:

Validar env vars requeridas:

WEBEX_TOKEN

WEBEX_BASE_URL

ENVIRONMENT ∈ {lab, prod}

Validar accesibilidad (1–2 llamadas GET “baratas”):

locations_list (o equivalente).

people_me / token_validation (o equivalente) para validar auth/alcance sin listar masivamente usuarios.

Si fallan por auth/permisos → abortar controlado sin procesar filas.

Registrar resultado en log: startup_checks=pass|fail + causa.

### 11) CIRCUIT BREAKER (SIMPLE) — DEFINICIÓN PROVISIONAL

Clave

Valor

CIRCUIT_BREAKER_THRESHOLD (provisional)

0.80

Se evalúa al finalizar cada batch por fase:

Si (non_retryable_external + auth_invalid + permission_denied) ≥ 80% de filas del batch:

Abortar run controladamente.

Persistir checkpoint al último batch completado.

Log crítico con resumen (counts por reason_code).

### 12) CONTRATO DE ENTRADAS/SALIDAS (ARCHIVOS)

#### 12.1 Output: rejected_rows.csv

Contiene solo fallos detectados pre-API.

Columnas mínimas: timestamp,row_id,entity_type,entity_key,reason_code,reason_message,raw_row_minified

#### 12.2 Output: results.csv (append seguro)

Una fila por resultado final de la fila de input en su fase.

Columnas mínimas: timestamp,batch_id,row_id,phase,entity_type,entity_key,step,status,http_status,message,remote_id

status ∈ {success,pending} (rejected se registra en rejected_rows.csv).

#### 12.3 Output: pending_rows.csv (append seguro)

Filas que fallan durante ejecución o son out-of-scope.

Columnas mínimas: timestamp,batch_id,row_id,phase,entity_type,entity_key,step,reason_code,reason_message,http_status,raw_row_minified

#### 12.4 Output: checkpoint.json

Se escribe de forma atómica (tmp + rename).

Campos definidos en sección 7.

#### 12.5 Append seguro (definición)

Modo append con flush tras cada registro.

Si se detecta corrupción: abortar controlado con log crítico (definición: no esconder corrupción).

No continuar en presencia de outputs corruptos sin intervención.

### 13) SUCCESS CONDITION POR ENDPOINT (OBLIGATORIO)

#### 13.1 Reglas generales

Cada step define: status esperado + campos mínimos.

Status esperados (provisional): create=200/201; update=200/204; delete=200/204/404 (404 aceptable como idempotente si aplica).

En create: presencia de id (o campo equivalente).

#### 13.2 Fallo de schema de respuesta

Si status es “ok” pero faltan campos mínimos: pending con reason_code=invalid_response_schema y continuar.

### 14) ESTRUCTURA DE MÓDULOS (MÍNIMA, DEFINIDA)

#### 14.1 config.py

Lee env vars y aplica defaults seguros.

ENVIRONMENT, WEBEX_BASE_URL, WEBEX_TOKEN

BATCH_SIZE=500, MAX_ROWS=21000, MAX_RETRIES=5

REQUEST_TIMEOUT_SECONDS=20

CIRCUIT_BREAKER_THRESHOLD=0.80

OUTPUT_DIR

ENABLE_SAFE_COMPENSATION=false

PIPELINE_VERSION=1

#### 14.2 data_pipeline.py

Validar/normalizar/dedupe mínimo y emitir ready_to_load.csv + rejected_rows.csv.

ready_to_load.csv mantiene el schema del input, pero normalizado.

#### 14.3 batch_iterator.py

Streaming sobre ready_to_load.csv por phase/entity_type.

Produce batches con batch_id determinista (phase + sequential_batch_number).

#### 14.4 connection_client.py

request() único con: timeouts, tenacity para retryables, parse JSON, validación de status/campos mínimos según step.

#### 14.5 actions_registry.py

Define steps por fase y entity_type.

Fase 1 Location: location_lookup → (location_create | location_update)

Fase 2 User (existente): user_lookup → user_enable_calling (si calling_enabled=true) → user_apply_calling_settings (si hay campos)

Fase 3 Assignment: assignment_lookup (si aplica) → assign_extension_or_number → apply_final_settings (si aplica)

Prohibido: user_create, user_update_identity.

#### 14.6 action_helpers.py

Builders puros: payloads desde fila normalizada.

Normalización auxiliar y composición de entity_key si no viene.

Rechazar campos out-of-scope en filas user.

#### 14.7 executor.py

Orquesta fases → batches → filas → steps.

Política: error por fila ⇒ pending y continuar.

Progreso/checkpoint solo tras registrar outputs de la fila actual.

Debe escribir results/pending inmediatamente por fila.

#### 14.8 error_handling.py

Mapea HTTP/status/excepciones a reason_code mínimo.

Sin lógica adicional.

#### 14.9 writers.py

Append seguro y serialización mínima de raw_row_minified.

raw_row_minified: JSON compactado de columnas relevantes.

#### 14.10 state_store.py

Write checkpoint atómico (tmp + rename).

Read checkpoint robusto: si JSON corrupto → abortar controlado con log crítico.

#### 14.11 startup_checks.py

Implementa preflight mínimo (sección 10).

### 15) ROLLBACK / COMPENSATION (MÍNIMO)

#### 15.1 Default

ENABLE_SAFE_COMPENSATION=false por defecto.

No se hacen deletes automáticos.

#### 15.2 Half-applied

Si un step success y un step posterior falla: fila pending con reason_code=half_applied.

Re-run completa por lookup+upsert.

#### 15.3 Compensación opcional (provisional)

Solo si se activa y el step lo soporta:

Si se creó un recurso y existe endpoint delete idempotente: intentar delete y registrar outcome.

Si delete falla: no abortar; registrar y continuar.

### 16) LOGGING (MÍNIMO, OPERATIVO)

#### 16.1 Formato

Structured logging (JSON o key=value), nivel INFO por defecto.

#### 16.2 Eventos obligatorios

Inicio/fin de run (con config efectiva sin secretos).

Inicio/fin de fase.

Inicio/fin de batch (counts).

Cada fila en error (entity_key, step, reason_code).

Retries (solo cuando ocurren).

Circuit breaker trigger.

Startup checks pass/fail.

#### 16.3 Prohibiciones

No log de tokens ni headers sensibles.

No spam: 1 log por fila fallida + 1 resumen por batch (counts por reason_code).

### 17) TESTING (SUFICIENTE)

#### 17.1 Unit tests (sin red)

data_pipeline: validación schema, normalización, dedupe mínimo, rejected output.

writers/state_store: append correcto, checkpoint atómico, lectura robusta.

batch_iterator: batching correcto por fase, límites MAX_ROWS/MAX_BATCHES.

#### 17.2 Behavioural tests (mock HTTP) — escenarios mínimos

create success (location/assignment) + user calling settings sobre usuario existente.

update success.

429 → retry → success.

5xx → retry agotado → pending (retry_exhausted).

4xx → pending sin retry (non_retryable_external / permission_denied / auth_invalid).

crash/restart simulado → resume sin duplicar (lookup+upsert).

user_lookup no encontrado → pending (user_not_found).

enable_calling falla por precondición → pending (precondition_missing).

Definición de crash test (provisional)

Simular excepción controlada en mitad de ejecución y reiniciar usando checkpoint escrito hasta el último success.

### 18) CRITERIOS DE ACEPTACIÓN

Procesa 21.000 filas con BATCH_SIZE=500 sin crash por fallos externos.

No hay bloqueos: cada request usa timeout.

Se respetan fases: locations → users_existing_calling → assignments/settings.

Outputs correctos y consistentes: cada fila termina en rejected/pending/success.

Re-run del mismo CSV no duplica entidades (lookup+upsert).

Startup checks previenen runs inválidos.

Circuit breaker detiene runs masivamente inválidos sin corromper outputs.

Resume desde checkpoint completa sin duplicar y sin perder trazabilidad.

Si un usuario no existe (LDAP no sincronizó): no crashea; marca pending user_not_found; continúa.

### 19) CONFIGURACIÓN (RESUMEN FINAL, DEFINICIÓN PROVISIONAL)

Env vars mínimas:

ENVIRONMENT=lab|prod

WEBEX_BASE_URL=...

WEBEX_TOKEN=...

OUTPUT_DIR=...

Opcionales:

BATCH_SIZE=500

MAX_ROWS=21000

MAX_RETRIES=5

REQUEST_TIMEOUT_SECONDS=20

CIRCUIT_BREAKER_THRESHOLD=0.80

ENABLE_SAFE_COMPENSATION=false

PIPELINE_VERSION=1
