# 5) Planificar el trabajo

## Coste/tiempo estimado
- MVP: 4–6 semanas.
- Hardening productivo: +2–4 semanas.

## Pasos y duración (orientativo)
1. Cierre contrato CSV y validadores: 4–5 días.
2. Núcleo runtime (executor/writers/checkpoint): 5–7 días.
3. Integraciones fase 1: 5–7 días.
4. Integraciones fase 2: 5–8 días.
5. Integraciones fase 3: 5–8 días.
6. Test automation + resiliencia: 5–7 días.
7. Documentación operativa y handover: 2–3 días.

## Milestones
- M1: input_schema + data_pipeline completos.
- M2: procesamiento por fases con resume.
- M3: acciones core post-LDAP estables.
- M4: pruebas de error y aceptación de operación.

## Scripts de migración
- No requeridos en MVP (sin DB).
- Requeridos scripts de generación/validación de CSV de prueba.

## Riesgos y rutas alternativas
- Riesgo 1: cambios/faltas de SDK.
  - Alternativa: endpoint REST validado.
  - Si no viable: `pending(sdk_method_missing|out_of_scope)`.
- Riesgo 2: límites/rate limits externos.
  - Alternativa: tuning de batch y backoff.
- Riesgo 3: prechecks no automatizables.
  - Alternativa: pendiente explícito y runbook de remediación.

## Definition of Done
### Requerido
- Estados terminales correctos por fila.
- No crash por fallos externos.
- Timeouts/retries/circuit breaker funcionando.
- Resume seguro con checkpoint atómico.
- Artefactos consistentes y append-safe.

### Opcional
- dry-run con validación remota sin escritura,
- compensación segura por step,
- observabilidad avanzada y paneles.
