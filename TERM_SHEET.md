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
