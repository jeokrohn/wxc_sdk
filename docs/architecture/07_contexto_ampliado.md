# 7) Entender el contexto amplio

## Limitaciones actuales
- Alcance single-org en MVP.
- Dependencia fuerte de integraciones externas.
- Rollback perfecto fuera de alcance; estrategia principal: re-run idempotente.

## Extensiones futuras
- soporte multi-org/multi-tenant,
- modo dry-run avanzado con reporte de drift,
- reconciliación periódica desired vs actual,
- catálogo de plantillas por país/tenant.

## Otras consideraciones (coste/presupuesto)
- principal coste en integración y QA de resiliencia;
- coste recurrente por cambios de API/SDK y gobierno operativo.

## Moonshot ideas
- asistente de intentos declarativos -> CSV válido,
- motor de recomendaciones de remediación automática,
- simulador de impacto por lote antes de ejecutar.

## Evolución del diseño
- versionar pipeline y reason codes,
- mantener compatibilidad hacia atrás del CSV cuando sea posible,
- simplificar continuamente (eliminar complejidad que no aporte valor operativo).
