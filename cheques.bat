@echo off
setlocal
pushd "%~dp0"
call ent\Scripts\activate.bat
python main.py
popd
endlocal
pause