# 1) Definir qué estamos construyendo

## Qué es la aplicación
Un bot de provisión masiva para Webex Calling que, a partir de un CSV único, ejecuta:
- provisión/actualización de recursos de telefonía por fase,
- configuración de usuarios ya existentes en Webex (post-LDAP),
- asignación de extensiones/números/settings,
- registro de resultados auditables y reanudables.

## Para quién es
- Equipos de ingeniería de colaboración/voz.
- Equipos de operación técnica de despliegues de sedes.
- PMs técnicos responsables de cumplimiento del rollout.

## Problema que resuelve
- Evita operación manual inviable a gran escala.
- Estandariza ejecución y diagnóstico de errores.
- Permite reiniciar/re-ejecutar sin duplicar entidades.

## Cómo funcionará
1. Se ingiere un CSV único.
2. Se valida esquema y se rechaza todo lo inválido pre-API.
3. Se procesa por fases fijas (1→2→3).
4. Cada fila ejecuta steps API con lookup+upsert.
5. Se persisten resultados por fila y checkpoint.
6. Si hay interrupción, se reanuda por `phase + last_row_id`.

## Conceptos principales y relaciones
- **Fila**: unidad de trabajo del CSV.
- **Entity type**: categoría funcional que define steps.
- **Entity key**: clave estable para lookup remoto.
- **Step**: llamada API concreta y validable.
- **Fase**: orden global de dependencias.
- **Reason code**: clasificación de error/pendiente.
- **Checkpoint**: punto de recuperación con hash de input.

Relaciones:
- una fila pertenece a una fase;
- una fase contiene múltiples entity_types;
- un entity_type define una secuencia de steps;
- cada step tiene criterios de éxito y error;
- el estado final de la fila depende del conjunto de steps.

## Principios de implementación
- Diseño/implementación en paralelo con prototipo temprano.
- Prioridad MVP: estabilidad operativa y trazabilidad.
- Menos es más: retirar complejidad no indispensable.
- Ninguna lógica de identidad de usuarios (fuera de alcance post-LDAP).
