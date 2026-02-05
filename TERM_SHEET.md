# UNIVERSAL EXECUTABLE SPEC TERM SHEET (WEBEX BULK PROVISION BOT)

(API SCRIPT/BOT — RESILIENT, AUTONOMOUS, NASA POWER OF 10 COMPLIANT)
**REQUEST FOR DEVELOPMENT (implementación directa, sin investigación adicional)**

---

## 1) ALCANCE OPERATIVO

### IN-SCOPE (el bot **debe** hacer)

* Aprovisionamiento **100% automatizado** (sin pasos manuales) de:
  * **Locations**
  * **Users**
  * **Extensions / números / asignaciones** (según contrato de entrada)
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

### OUT-OF-SCOPE (el bot **no** hace)

* UI, dashboards, multi-tenant/multi-org.
* Provisioning de credenciales / OAuth app registration / secret storage (solo consumo vía env vars).
* “Manual post-steps”: **no existen**.
  * Si una acción no es automatizable por API ⇒ fila a `pending_rows.csv` con `reason_code` explícito.
* Corrección inventada de datos (solo normaliza/valida; si falla ⇒ rejected/pending).
* Rollback perfecto garantizado (solo compensación opcional y segura; ver sección Rollback).

---

## 2) PROPÓSITO Y GARANTÍAS

**Propósito**: programa autónomo para alta masiva de Webex (locations/users/extensions/config), con degradación segura y reinicio sin efectos secundarios.

**Garantías terminales**

* No crash por fallos externos.
* No bloqueo indefinido.
* Cada fila termina exactamente en: `success` (results) o `pending` o `rejected`.
* Reinicio/relanzado: reanuda desde checkpoint sin duplicar entidades (lookup+upsert).

---

## 3) MODELO DE EJECUCIÓN

* Proceso long-running.
* Batches con tamaño fijo (default 500) y límites estáticos:
  * `MAX_ROWS`, `MAX_BATCHES`, `MAX_RETRIES`.
* Flujo:
  1. pipeline de datos (pre-API)
  2. ejecución por batch
  3. persistencia incremental de resultados y checkpoint

---

## 4) NASA POWER OF 10 — REGLAS RUNTIME (OBLIGATORIAS)

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

## 5) IDENTITY + IDEMPOTENCIA (REMOTE-STATE FOCUSED)

### Claves estables (obligatorias)

* User: `email`
* Location: `location_name` o `location_external_id`
* Extension/Number: clave compuesta (p.ej. `location_id + extension`)

### Regla de idempotencia (mínima, sin “diff” completo)

Por cada fila y entidad:

* **Lookup remoto por clave estable**.
* Si existe ⇒ usar `remote_id` y ejecutar **update** determinista.
* Si no existe ⇒ **create** y persistir `remote_id` en results.

> No se exige comparación campo-a-campo “desired vs actual”. El control de duplicados se resuelve con lookup + upsert determinista.

---

## 6) ESTADO Y REANUDACIÓN (ANTI-CORRUPCIÓN MÍNIMA)

* Nunca crear sin lookup previo por clave estable.
* Guardar progreso **solo** después de éxito del conjunto de calls requeridos para esa fila.
* En `resume`, reanudar desde `checkpoint.json` y repetir lookup+upsert:
  * evita duplicados tras crash,
  * permite completar filas “half-applied” sin introducir complejidad extra.

---

## 7) MODELO DE ERRORES (SIMPLIFICADO)

Se reduce a lo mínimo operativo (se elimina sobre-diseño):

### Clases

* **RETRYABLE_EXTERNAL**: timeouts, network, 429, 5xx.
* **NON_RETRYABLE_EXTERNAL**: 4xx por datos/permiso/contrato, auth inválida persistente.
* **ASSERTION_FAILURE**: invariantes locales/bug detectado por assertion.

### Reglas

* Retryable ⇒ retry acotado (tenacity) y si se agota ⇒ `pending_rows.csv`.
* Non-retryable ⇒ `pending_rows.csv` sin retry ciego.
* Assertion failure ⇒ `pending_rows.csv` + log crítico y continuar.

> No se implementa “contador de intentos” como feature persistida. Los retries se registran en logs (suficiente).

---

## 8) RETRY & TIMEOUTS (TENACITY) — ACOTADO

* Timeouts obligatorios por request (no bloqueos).
* Tenacity: exponential backoff + jitter.
* Máximo de retries configurable y fijo.
* Exhaustión ⇒ pending + continuar.

---

## 9) CIRCUIT BREAKER (SIMPLE, OBLIGATORIO)

Para evitar runs inútiles y proteger la ejecución:

* Si un batch supera un umbral de `NON_RETRYABLE_EXTERNAL` por permisos/auth (p.ej. 80%):
  * finalizar ejecución controladamente,
  * checkpoint hasta último batch completo,
  * log crítico con causa probable (token/scopes/org/base_url).

---

## 10) CONTRATO DE ENTRADAS/SALIDAS

### Input

* CSV(s) con schema ya acordado (no investigación adicional).
* Config por env vars (LAB/PROD sin cambios de código).

### Output files (obligatorios)

* `rejected_rows.csv`: inválidas antes de tocar Webex (`reason_code`, `reason_message`).
* `results.csv` (append seguro): `timestamp,batch_id,row_id,entity_type,entity_key,step,status,http_status,message,remote_id`.
* `pending_rows.csv` (append seguro): `timestamp,batch_id,row_id,entity_type,entity_key,step,reason_code,reason_message,http_status,raw_row_minified`.
* `checkpoint.json`: `input_hash,pipeline_version,last_completed_batch_id,last_completed_row_id,started_at`.

---

## 11) SUCCESS CONDITION POR ENDPOINT (OBLIGATORIO)

Cada step define éxito por:

* HTTP status esperado, y
* presencia de campos mínimos (p.ej. `id`) cuando aplique.
  No se depende de mensajes de texto.

---

## 12) ESTRUCTURA DE MÓDULOS (MÍNIMA, SIN “GOD MODULES”)

* `config.py`: carga env vars + defaults seguros.
* `data_pipeline.py`: ingest/normalize/validate/dedupe → ready/rejected.
* `batch_iterator.py`: streaming + batches + bounds.
* `connection_client.py`: request() único con timeouts + tenacity + validación response.
* `actions_registry.py`: steps declarativos (endpoints/payload builder/success condition).
* `action_helpers.py`: lógica pura (payload builders/normalizadores).
* `executor.py`: orquestación batch→row→steps, lookup+upsert, writes + checkpoint.
* `error_handling.py`: mapping a `reason_code` mínimo.
* `writers.py`: append seguro results/pending/rejected.
* `state_store.py`: checkpoint atómico (tmp + rename).

---

## 13) ROLLBACK / COMPENSATION (LO MÁS CONVENIENTE: MÍNIMO)

* **Por defecto: sin rollback automático.**
* Si una fila queda “half-applied”:
  * se registra como pending con `reason_code=half_applied`,
  * la re-ejecución (lookup+upsert) completa lo pendiente sin duplicar.
* Compensación **opcional** solo si:
  * es segura (delete idempotente y soportado),
  * se activa por config (`ENABLE_SAFE_COMPENSATION=true`).

---

## 14) LOGGING (MÍNIMO, SUFICIENTE)

* Structured logs (key=value o JSON).
* Eventos mínimos:
  * inicio/fin de batch,
  * errores por fila (con `entity_key`, `step`, `http_status` si aplica),
  * retry attempts y agotamiento,
  * circuit breaker trigger,
  * assertion failures.
* Sin “log spam loops” (rate limit básico por repetición de error).

---

## 15) TESTING (OBLIGATORIO)

### Unit (sin red)

* pipeline, helpers, iterator, writers/state_store, error mapping.

### Behavioural (mock HTTP)

* 429/5xx/timeouts ⇒ retry ⇒ success o pending si se agota.
* 4xx ⇒ pending sin retry.
* mezcla success/fail por fila ⇒ el run continúa.
* crash/restart ⇒ resume sin duplicar (lookup+upsert).
* circuit breaker ⇒ salida controlada.

---

## 16) CRITERIOS DE ACEPTACIÓN

* Ejecuta sobre 21.000 filas sin crash por fallos externos.
* No bloqueos (timeouts siempre).
* Cada fila termina en results/pending/rejected con trazabilidad completa.
* Re-ejecución del mismo CSV no duplica entidades (lookup+upsert).
* Reanudación desde checkpoint funciona y no corrompe outputs.

---

## Sugerencias optimizadas (mínimo esfuerzo, máxima certeza en 1ª puesta en servidor)

### A. Imprescindible para ejecutar “una sede completa” sin intervención

1. **Contrato único de entrada (CSV) y nada más**
   * **Qué hacer**: definir **un solo CSV** con columnas mínimas para: `location`, `user`, `extension/number`, `calling_settings` (las que realmente vais a aplicar).
   * **Por qué**: sin esto, el pipeline y el executor quedan ambiguos y habrá fallos “por datos”.
   * **Entregable**: `input_schema.md` + validación estricta → `rejected_rows.csv`.

2. **Orden fijo de fases (3 fases)**
   * **Qué hacer**: ejecutar siempre en este orden:
     * **Fase 1**: Locations (crear/actualizar)
     * **Fase 2**: Users (crear/actualizar + habilitar calling si aplica)
     * **Fase 3**: Extensions/Números/Asignaciones + settings finales
   * **Por qué**: evita dependencias rotas sin diseñar un grafo complejo.
   * **Entregable**: `executor` con `phase` y 3 runs internos o 3 filtros por `entity_type`.

3. **Lookup + Upsert por clave estable (idempotencia remota mínima)**
   * **Qué hacer**:
     * Location: lookup por `location_name` (o external_id si existe).
     * User: lookup por `email`.
     * Extension: lookup por (`location_id`, `extension`) o (`location_id`, `number`).
     * Si existe → update; si no → create.
   * **Por qué**: permite re-ejecutar sin duplicar y completa “half applied” tras reinicio.
   * **Nota**: no hacer diff “desired vs actual”.

4. **Checkpoint simple por fase**
   * **Qué hacer**: un `checkpoint.json` con:
     * `phase`, `last_row_id`, `input_hash`
   * **Por qué**: reanudación real sin ingeniería extra.
   * **No hacer**: índices complejos, dedupe de results, etc.

5. **Outputs mínimos re-procesables**
   * `results.csv`: una línea por fila con estado final (`success|pending|rejected`) y `remote_id` si aplica.
   * `pending_rows.csv`: fila + `reason_code` + `step` (para re-run).
   * `rejected_rows.csv`: fallos de validación pre-API.
   * **Por qué**: trazabilidad y “no se rompe el run”.

---

### B. Imprescindible para “certeza en servidor” (sin sobre-diseño)

6. **Startup safety checks (preflight mínimo)**
   * **Qué hacer antes de procesar 3.000–21.000**:
     * validar env vars requeridas,
     * hacer 1–2 llamadas “baratas” (p.ej. listar org/locations o un GET simple) para confirmar token/base_url/permisos.
   * **Por qué**: evita ejecutar 1 hora y descubrir que faltan scopes.

7. **Timeouts + retries acotados + circuito “hard stop”**
   * **Qué hacer**:
     * timeouts obligatorios,
     * retries solo para 429/5xx/timeouts,
     * circuit breaker por batch si dominan errores de permisos/auth.
   * **Por qué**: evita cuelgues y runs inútiles. Es poca complejidad y mucho valor.

8. **Success condition por endpoint (mínimo)**
   * **Qué hacer**: éxito = `http_status esperado` + `id` cuando sea create.
   * **Por qué**: elimina falsos positivos y “esperar mensajes”.

---

### C. Simplificaciones deliberadas (para no gastar esfuerzo ahora)

9. **No implementar**
   * catálogo extenso de `reason_code` (solo 8–10 códigos prácticos),
   * dedupe avanzado o “results de-duplication”,
   * rollback automático (por defecto NO),
   * concurrencia,
   * indexado masivo remoto previo,
   * polling async salvo que aparezca 202 en endpoints críticos.

10. **Rollback: enfoque más conveniente**
    * **Qué hacer**: no rollback.
    * **Qué sí**: registrar `half_applied` en pending y confiar en re-run (lookup+upsert) para completar.
    * **Por qué**: menor complejidad y suficiente para 1ª activación.

---

### D. Testing mínimo que da certeza real (sin batería infinita)

11. **2 capas y listo**
    * Unit tests: pipeline (validación/normalización) + writers/checkpoint.
    * Behavioural tests (mock HTTP): 6 escenarios:
      1. create success
      2. update success
      3. 429→retry→success
      4. 5xx→retry agotado→pending
      5. 4xx→pending sin retry
      6. crash/restart (simulado)→resume sin duplicar (lookup encuentra y se hace update o se marca success)

---

### Lista final “lo mínimo que cambia el juego” (prioridad absoluta)

1. CSV schema único + validación → rejected
2. 3 fases fijas (locations→users→extensions/settings)
3. lookup+upsert por clave estable (idempotencia remota)
4. checkpoint simple por fase
5. results/pending en CSV append seguro
6. startup safety checks
7. timeouts + retries acotados + circuit breaker
8. behavioural tests con mocks para los 6 flujos críticos
