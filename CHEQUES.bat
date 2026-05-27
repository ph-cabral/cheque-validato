@echo off
cd /d "%~dp0"

if exist "codigo_cheques\terminado.flag" del "codigo_cheques\terminado.flag"
if exist "pids.txt" del "pids.txt"

wscript "CHEQUES.vbs"

:loop
if not exist "codigo_cheques\terminado.flag" (
    timeout /t 1 >nul
    goto loop
)

del "codigo_cheques\terminado.flag"

REM Cerrar por PID
for /f "tokens=*" %%i in (pids.txt) do (
    taskkill /PID %%i /F /T >nul 2>&1
)-
del "pids.txt"

exit
