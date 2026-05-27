@echo off
setlocal
A:
cd "\Acreditraciones\dist\codigo_cheques"
call ent\Scripts\activate.bat
python main.py
endlocal
exit