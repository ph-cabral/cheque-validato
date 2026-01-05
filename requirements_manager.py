import os
import sys
import subprocess

# ---------------------------
# CONSTANTES
# ---------------------------
OPERADORES = ("==", ">=", "<=", "!=", ">", "<")


# ---------------------------
# PARSING
# ---------------------------
def parsear_requerimiento(linea: str):
    """
    Devuelve (nombre, version | None)
    """
    for op in OPERADORES:
        if op in linea:
            nombre, version = linea.split(op, 1)
            return nombre.strip().lower(), version.strip()
    return linea.strip().lower(), None


def obtener_requerimientos(requirements_path):
    """
    Lee requirements.txt y devuelve:
    [(paquete, version | None), ...]
    """
    if not os.path.exists(requirements_path):
        return []

    with open(requirements_path, encoding="utf-8") as f:
        return [
            parsear_requerimiento(linea)
            for linea in map(str.strip, f)
            if linea and not linea.startswith("#")
        ]


# ---------------------------
# INSTALADOS
# ---------------------------
def obtener_paquetes_instalados():
    """
    Ejecuta pip freeze y devuelve:
    {paquete: version}
    """
    try:
        resultado = subprocess.run(
            [sys.executable, "-m", "pip", "freeze"],
            capture_output=True,
            text=True,
            check=True
        )

        return {
            nombre.lower(): version
            for nombre, version in (
                linea.split("==", 1)
                for linea in resultado.stdout.splitlines()
                if "==" in linea
            )
        }

    except subprocess.CalledProcessError:
        return {}


# ---------------------------
# COMPARACIÓN
# ---------------------------
def encontrar_paquetes_faltantes(requirements_path):
    """
    Devuelve lista de paquetes faltantes:
    ['pandas', 'requests==2.31.0', ...]
    """
    instalados = obtener_paquetes_instalados()
    requerimientos = obtener_requerimientos(requirements_path)

    return [
        nombre if not version else f"{nombre}=={version}"
        for nombre, version in requerimientos
        if nombre not in instalados
    ]


# ---------------------------
# INSTALACIÓN
# ---------------------------
def instalar_requerimientos():
    """
    Instala solo los paquetes faltantes
    """
    req_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    if not os.path.exists(req_path):
        return

    for paquete in encontrar_paquetes_faltantes(req_path):
        subprocess.call([sys.executable, "-m", "pip", "install", paquete])
