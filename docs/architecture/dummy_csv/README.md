# Dummy CSVs de referencia (alineados al plan v3)

Esta carpeta contiene ejemplos **dummy** para acelerar validación de formato sin salir del alcance definido.

## Contenido
- `01_input_base_minimo.csv`: columnas base mínimas del contrato de entrada.
- `02_phase1_location_routing_dummy.csv`: ejemplos de entity_type de fase 1.
- `03_phase2_users_workspaces_dummy.csv`: ejemplos de entity_type de fase 2.
- `04_phase3_shared_services_dummy.csv`: ejemplos de entity_type de fase 3.
- `90_output_results_dummy.csv`: formato esperado de `results.csv`.
- `91_output_pending_rows_dummy.csv`: formato esperado de `pending_rows.csv`.
- `92_output_rejected_rows_dummy.csv`: formato esperado de `rejected_rows.csv`.

## Notas
- Son archivos de ejemplo/documentación, no datasets productivos.
- Incluyen una fila mínima por entity_type relevante para verificar headers, parseo y mapeo.
- Campos no aplicables en una fila se dejan vacíos intencionadamente.
