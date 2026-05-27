@echo off
setlocal
A:
cd "\Acreditraciones\dist\codigo_cheques"
if exist terminado.flag del terminado.flag
call ent\Scripts\activate.bat
start /b python rickroll_runner.py
:wait
timeout /t 1 /nobreak >nul
if not exist terminado.flag goto wait
taskkill /f /im python.exe >nul 2>&1
del terminado.flag
endlocal
exit