# Runbook MVP: laboratorio ready-to-run

Este documento deja el flujo **completo y ejecutable** para validar acciones del laboratorio de Webex con el mínimo de fricción.

## 1) Qué se está construyendo (MVP)
- **Feature**: flujo de provisión mínima para un lab (`context + apply commands`) y ejecución guiada de acciones.
- **Para quién**: operadores/devs que validan endpoints remotos con scripts `actions/action_*.py`.
- **Problema que resuelve**: elimina configuración manual dispersa y estandariza un camino reproducible.
- **Cómo funciona**:
  1. generar usuarios dummy,
  2. cargar/asegurar usuarios en tenant,
  3. generar `lab_context.json` + `lab_apply_commands.sh`,
  4. validar primer script crítico,
  5. ejecutar lote completo.

## 2) Happy flow (step-by-step)

### Paso 0 — Token
```bash
export WEBEX_ACCESS_TOKEN="<TOKEN_VALIDO>"
```

### Paso 1 — Generar usuarios dummy (json/csv)
```bash
python actions/generate_dummy_users.py --count 15 --domain lab.example.com --format json --output actions/dummy_users.json
python actions/generate_dummy_users.py --count 15 --domain lab.example.com --format csv --output actions/dummy_users.csv
```

### Paso 2 — Cargar usuarios al tenant (script de subida)
`provision_lab_dependencies.py` en `--mode apply` realiza creación/lookup de users y construye contexto:
```bash
python actions/provision_lab_dependencies.py --mode apply --token "$WEBEX_ACCESS_TOKEN" --domain lab.example.com --user-count 3
```

Salida esperada:
- `actions/lab_context.json`
- `actions/lab_apply_commands.sh`

### Paso 3 — Verificar contexto generado
```bash
python -m json.tool actions/lab_context.json > /dev/null
```
Verifica que existan al menos:
- `location_id`
- `person_id`, `member_id`, `assistant_person_id`
- `extension`, `primary_number`

### Paso 4 — Probar el primer script (gate de calidad)
Primero `probe` y luego `apply` del script base recomendado `action_nominal_users.py`.

#### 4.1 Probe
```bash
python actions/action_nominal_users.py --mode probe --vars "$(python - <<'PY'
import json
c=json.load(open('actions/lab_context.json',encoding='utf-8'))
print(json.dumps({
  'person_id': c['person_id'],
  'extension': c['extension'],
  'primary_number': c['primary_number'],
  'email': c['users'][0]['email']
}, ensure_ascii=False))
PY
)"
```

#### 4.2 Apply
```bash
python actions/action_nominal_users.py --mode apply --vars "$(python - <<'PY'
import json
c=json.load(open('actions/lab_context.json',encoding='utf-8'))
print(json.dumps({
  'person_id': c['person_id'],
  'extension': c['extension'],
  'primary_number': c['primary_number'],
  'email': c['users'][0]['email']
}, ensure_ascii=False))
PY
)"
```

### Paso 5 — Ejecutar lote completo de acciones
```bash
bash actions/lab_apply_commands.sh
```

## 3) Flujos alternativos
- Si no quieres crear usuarios nuevos, usa `--mode plan` y reutiliza users existentes del tenant.
- Si el tenant no tiene usuarios suficientes, vuelve a `Paso 2` con `--mode apply`.
- Si una acción no aplica al tenant (licencias/capabilities), ejecutar primero en `probe` para capturar limitaciones.

## 4) Validaciones mínimas de seguridad
- Nunca commitear el token.
- Ejecutar contra tenant de laboratorio, no producción.
- Revisar payloads de `--vars` antes de `--mode apply`.

## 5) Definition of Done (MVP)
- [ ] `lab_context.json` generado sin errores.
- [ ] `action_nominal_users.py` funciona en `probe` y `apply`.
- [ ] `lab_apply_commands.sh` ejecuta el lote en orden.
- [ ] El operador puede repetir el flujo completo con un token nuevo sin tocar código.
