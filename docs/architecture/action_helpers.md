# Requisitos de action helpers (action_helpers.py)

## Responsabilidad
Funciones puras para:
- derivar `entity_key`,
- construir payloads por step/entity_type,
- normalizar campos semánticos del CSV.

## Reglas
- sin llamadas de red,
- sin side effects,
- rechazo de campos de identidad fuera de alcance en user_* post-LDAP,
- helpers reutilizables para phone_number, extension, flags booleanas.

## Diseño recomendado
- firmas pequeñas y explícitas,
- validaciones previas a construcción de payload,
- salida deterministicamente serializable.
