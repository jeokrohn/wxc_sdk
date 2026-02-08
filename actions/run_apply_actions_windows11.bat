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

set "CONTINUE_FLAG=--continue-on-error"
if /I "%~2"=="--fail-fast" set "CONTINUE_FLAG="

echo [INFO] Ejecutando acciones en modo apply...
python actions\run_apply_actions.py --token "%WEBEX_ACCESS_TOKEN%" %CONTINUE_FLAG%
set "EXIT_CODE=%ERRORLEVEL%"

if "%EXIT_CODE%"=="0" (
  echo [OK] Runner completado.
) else (
  echo [ERROR] Runner finalizado con errores. Revisa actions\logs\apply_runner_*.log
)

popd >nul
exit /b %EXIT_CODE%
