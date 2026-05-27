Set fso = CreateObject("Scripting.FileSystemObject")
Set shell = CreateObject("WScript.Shell")
Dim carpeta
carpeta = fso.GetParentFolderName(WScript.ScriptFullName)

' Ventana pequeña con mensaje
Dim oMensaje
Set oMensaje = shell.Exec("cmd /k title Mensaje && mode con cols=50 lines=3 && echo. && echo   Importando cheques, ya casi termina...")

' Ventana Rick
Dim oRick
Set oRick = shell.Exec("cmd /k title Rick Astley && curl ascii.live/rick")

' Guardar PIDs
Set f = fso.OpenTextFile(carpeta & "\pids.txt", 2, True)
f.WriteLine oMensaje.ProcessID
f.WriteLine oRick.ProcessID
f.Close

' Python invisible
shell.Run "cmd /c pushd """ & carpeta & "\codigo_cheques"" && call ent\Scripts\activate.bat && python main.py", 0, False
