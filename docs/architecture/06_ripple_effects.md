# 6) Identificar ripple effects

## Acciones fuera de diseño/implementación
- Actualizar runbooks de operación y soporte.
- Definir proceso de triage para filas `pending`.
- Definir ownership de remediación por reason_code.

## Documentación a actualizar
- plantilla de CSV por cada entity_type,
- guía de reason_codes y remediación,
- guía de re-run/resume,
- checklist de preflight y post-run.

## Comunicación a usuarios existentes
- anunciar cambio de operación manual a pipeline automatizado,
- establecer ventanas de ejecución recomendadas,
- comunicar limitaciones explícitas (post-LDAP, sin identidad).

## Sistemas externos a coordinar
- Control Hub / Webex API,
- proveedores de trunk/SBC,
- LDAP (sin operación directa, pero dependencia de sincronización),
- observabilidad/alertado corporativo.

## Por qué esto impacta tiempos en enterprise
- dependencia de permisos y compliance,
- coordinación entre varios equipos,
- variabilidad de contratos SDK/API y rate limits.
