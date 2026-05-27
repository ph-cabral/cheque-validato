@echo off
setlocal
cd /d "%~dp0"
call ent\Scripts\activate.bat
python main.py
endlocal
exit