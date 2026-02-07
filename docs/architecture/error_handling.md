# Requisitos de error handling (error_handling.py)

## Clases de error
- `RETRYABLE_EXTERNAL`
- `NON_RETRYABLE_EXTERNAL`
- `ASSERTION_FAILURE`

## Reason codes base
- `invalid_input_schema` (rejected)
- `duplicate_key` (rejected)
- `out_of_scope` (pending)
- `non_retryable_external` (pending)
- `permission_denied` (pending)
- `auth_invalid` (pending)
- `retry_exhausted` (pending)
- `invalid_response_schema` (pending)
- `half_applied` (pending)
- `unhandled_exception` (pending)
- `user_not_found` (pending)
- `precondition_missing` (pending)

## Reason codes extendidos
- `workspace_not_found`
- `number_inventory_missing`
- `license_or_feature_missing`
- `resource_dependency_missing`
- `invalid_dial_plan_collision`
- `sdk_method_missing`

## Mapeo mínimo
- retryables agotados => `retry_exhausted`
- 401 => `auth_invalid`
- 403 => `permission_denied`
- otros 4xx => `non_retryable_external`
- invariantes/excepción no controlada => `unhandled_exception`
