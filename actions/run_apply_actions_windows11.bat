@echo off
setlocal EnableExtensions

REM -----------------------------------------------------------------------------
REM Webex Calling actions runner (Windows 11 / PowerShell friendly)
REM Uso recomendado (PowerShell):
REM   $env:WEBEX_ACCESS_TOKEN = "<tu_token>"
REM   .\actions\run_apply_actions_windows11.bat
REM
REM Alternativa pasando token como argumento:
REM   .\actions\run_apply_actions_windows11.bat "<tu_token>"
REM -----------------------------------------------------------------------------

set "SCRIPT_DIR=%~dp0"
pushd "%SCRIPT_DIR%.." >nul

if not "%~1"=="" set "WEBEX_ACCESS_TOKEN=%~1"

if "%WEBEX_ACCESS_TOKEN%"=="" (
  echo [ERROR] WEBEX_ACCESS_TOKEN no esta definido.
  echo.
  echo En PowerShell ejecuta:
  echo   $env:WEBEX_ACCESS_TOKEN = "<tu_token>"
  echo   .\actions\run_apply_actions_windows11.bat
  echo.
  echo O pasa el token como primer argumento del .bat.
  popd >nul
  exit /b 2
)

echo [INFO] Ejecutando acciones en modo apply...

python actions\action_auto_attendant.py --mode apply --token "%WEBEX_ACCESS_TOKEN%" --vars "{\"aa_name\":\"AA-LAB-MADRID\",\"extension\":\"5101\",\"location_id\":\"Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2ZjODY3OGRhLTBiOGItNDBlZS04ZWVjLTNhNzFlODFiMzc0OA\",\"schedule_name\":\"Horario-LAB-LV\"}"
if errorlevel 1 goto :failed

python actions\action_call_pickup_group.py --mode apply --token "%WEBEX_ACCESS_TOKEN%" --vars "{\"extension\":\"5101\",\"location_id\":\"Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2ZjODY3OGRhLTBiOGItNDBlZS04ZWVjLTNhNzFlODFiMzc0OA\",\"member_id\":\"Y2lzY29zcGFyazovL3VzL1BFT1BMRS80OWZhZTIyMC02OGZlLTQ2NzEtYmU1My03Y2UxZDgzZTQ1ZDE\",\"pickup_name\":\"PG-LAB-RECEPCION\"}"
if errorlevel 1 goto :failed

python actions\action_call_profiles.py --mode apply --token "%WEBEX_ACCESS_TOKEN%" --vars "{\"location_id\":\"Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2ZjODY3OGRhLTBiOGItNDBlZS04ZWVjLTNhNzFlODFiMzc0OA\"}"
if errorlevel 1 goto :failed

python actions\action_call_queue.py --mode apply --token "%WEBEX_ACCESS_TOKEN%" --vars "{\"extension\":\"5101\",\"location_id\":\"Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2ZjODY3OGRhLTBiOGItNDBlZS04ZWVjLTNhNzFlODFiMzc0OA\",\"member_id\":\"Y2lzY29zcGFyazovL3VzL1BFT1BMRS80OWZhZTIyMC02OGZlLTQ2NzEtYmU1My03Y2UxZDgzZTQ1ZDE\",\"queue_id\":\"MISSING_queue_id\",\"queue_name\":\"CQ-LAB-VENTAS\"}"
if errorlevel 1 goto :failed

python actions\action_day_t_numbers_caller_id.py --mode apply --token "%WEBEX_ACCESS_TOKEN%" --vars "{\"location_id\":\"Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2ZjODY3OGRhLTBiOGItNDBlZS04ZWVjLTNhNzFlODFiMzc0OA\",\"person_id\":\"Y2lzY29zcGFyazovL3VzL1BFT1BMRS80OWZhZTIyMC02OGZlLTQ2NzEtYmU1My03Y2UxZDgzZTQ1ZDE\",\"primary_number\":\"+34915559742549\"}"
if errorlevel 1 goto :failed

python actions\action_delegated_admin.py --mode apply --token "%WEBEX_ACCESS_TOKEN%" --vars "{\"principal_id\":\"Y2lzY29zcGFyazovL3VzL1BFT1BMRS80OWZhZTIyMC02OGZlLTQ2NzEtYmU1My03Y2UxZDgzZTQ1ZDE\",\"role_id\":\"Y2lzY29zcGFyazovL3VzL1JPTEUvaWRfdXNlcl9hZG1pbg\",\"scope\":\"organization\"}"
if errorlevel 1 goto :failed

python actions\action_devices.py --mode apply --token "%WEBEX_ACCESS_TOKEN%" --vars "{\"device_model\":\"Cisco 8851\",\"workspace_id\":\"Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1BMQUNFLzQyOGI3NzVhLWYxNTgtNDVkOC1hOTJhLTg1OTllNTVjM2UxYw==\"}"
if errorlevel 1 goto :failed

python actions\action_group_assignment.py --mode apply --token "%WEBEX_ACCESS_TOKEN%" --vars "{\"group_id\":\"MISSING_group_id\",\"group_name\":\"LAB-GROUP-VOICE\",\"member_id\":\"Y2lzY29zcGFyazovL3VzL1BFT1BMRS80OWZhZTIyMC02OGZlLTQ2NzEtYmU1My03Y2UxZDgzZTQ1ZDE\"}"
if errorlevel 1 goto :failed

python actions\action_hunt_group.py --mode apply --token "%WEBEX_ACCESS_TOKEN%" --vars "{\"extension\":\"5101\",\"hunt_name\":\"HG-LAB-SOPORTE\",\"location_id\":\"Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2ZjODY3OGRhLTBiOGItNDBlZS04ZWVjLTNhNzFlODFiMzc0OA\",\"member_id\":\"Y2lzY29zcGFyazovL3VzL1BFT1BMRS80OWZhZTIyMC02OGZlLTQ2NzEtYmU1My03Y2UxZDgzZTQ1ZDE\"}"
if errorlevel 1 goto :failed

python actions\action_internal_extensions_sbc.py --mode apply --token "%WEBEX_ACCESS_TOKEN%" --vars "{\"location_id\":\"Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2ZjODY3OGRhLTBiOGItNDBlZS04ZWVjLTNhNzFlODFiMzc0OA\",\"route_group_id\":\"MISSING_route_group_id\",\"route_group_name\":\"RG-LAB-SBC\",\"trunk_id\":\"MISSING_trunk_id\",\"trunk_name\":\"TRUNK-LAB-MAIN\"}"
if errorlevel 1 goto :failed

python actions\action_interplatform_dial_plan.py --mode apply --token "%WEBEX_ACCESS_TOKEN%" --vars "{\"dial_pattern\":\"+3491XXXXXXX\",\"dial_plan_name\":\"DP-LAB-INTERPLATFORM\",\"route_group_id\":\"MISSING_route_group_id\"}"
if errorlevel 1 goto :failed

python actions\action_legacy_forwarding.py --mode apply --token "%WEBEX_ACCESS_TOKEN%" --vars "{\"forward_destination\":\"+34915550123\",\"person_id\":\"Y2lzY29zcGFyazovL3VzL1BFT1BMRS80OWZhZTIyMC02OGZlLTQ2NzEtYmU1My03Y2UxZDgzZTQ1ZDE\"}"
if errorlevel 1 goto :failed

python actions\action_location_number_removal.py --mode apply --token "%WEBEX_ACCESS_TOKEN%" --vars "{\"location_id\":\"Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2ZjODY3OGRhLTBiOGItNDBlZS04ZWVjLTNhNzFlODFiMzc0OA\",\"primary_number\":\"+34915559742549\"}"
if errorlevel 1 goto :failed

python actions\action_manager_assistant.py --mode apply --token "%WEBEX_ACCESS_TOKEN%" --vars "{\"assistant_person_id\":\"Y2lzY29zcGFyazovL3VzL1BFT1BMRS81MjYxMWNkMS1jMTJmLTQxNjgtODc1My04MDdmODJiOTYwNGQ\",\"person_id\":\"Y2lzY29zcGFyazovL3VzL1BFT1BMRS80OWZhZTIyMC02OGZlLTQ2NzEtYmU1My03Y2UxZDgzZTQ1ZDE\"}"
if errorlevel 1 goto :failed

python actions\action_monitoring.py --mode apply --token "%WEBEX_ACCESS_TOKEN%" --vars "{\"person_id\":\"Y2lzY29zcGFyazovL3VzL1BFT1BMRS80OWZhZTIyMC02OGZlLTQ2NzEtYmU1My03Y2UxZDgzZTQ1ZDE\",\"target_person_id\":\"Y2lzY29zcGFyazovL3VzL1BFT1BMRS81MjYxMWNkMS1jMTJmLTQxNjgtODc1My04MDdmODJiOTYwNGQ\"}"
if errorlevel 1 goto :failed

python actions\action_nominal_users.py --mode apply --token "%WEBEX_ACCESS_TOKEN%" --vars "{\"extension\":\"5101\",\"person_id\":\"Y2lzY29zcGFyazovL3VzL1BFT1BMRS80OWZhZTIyMC02OGZlLTQ2NzEtYmU1My03Y2UxZDgzZTQ1ZDE\",\"primary_number\":\"+34915559742549\"}"
if errorlevel 1 goto :failed

python actions\action_secondary_numbers.py --mode apply --token "%WEBEX_ACCESS_TOKEN%" --vars "{\"extension\":\"5101\",\"person_id\":\"Y2lzY29zcGFyazovL3VzL1BFT1BMRS80OWZhZTIyMC02OGZlLTQ2NzEtYmU1My03Y2UxZDgzZTQ1ZDE\",\"secondary_number\":\"+34915555861252\"}"
if errorlevel 1 goto :failed

python actions\action_user_recording.py --mode apply --token "%WEBEX_ACCESS_TOKEN%" --vars "{\"person_id\":\"Y2lzY29zcGFyazovL3VzL1BFT1BMRS80OWZhZTIyMC02OGZlLTQ2NzEtYmU1My03Y2UxZDgzZTQ1ZDE\"}"
if errorlevel 1 goto :failed

python actions\action_workspaces.py --mode apply --token "%WEBEX_ACCESS_TOKEN%" --vars "{\"extension\":\"5101\",\"primary_number\":\"+34915559742549\",\"workspace_id\":\"Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1BMQUNFLzQyOGI3NzVhLWYxNTgtNDVkOC1hOTJhLTg1OTllNTVjM2UxYw==\"}"
if errorlevel 1 goto :failed

echo [OK] Runner completado.
popd >nul
exit /b 0

:failed
echo [ERROR] Fallo en una accion. Se detiene el runner (fail-fast).
popd >nul
exit /b 1
