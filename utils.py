import os
import sys
import re

def ruta_absoluta(*paths):
    """
    Devuelve una ruta absoluta a partir del archivo que llama.
    Ej:
    ruta_absoluta("..", "archivo.xlsx")
    """
    base = os.path.dirname(os.path.abspath(sys.argv[0]))
    return os.path.abspath(os.path.join(base, *paths))


def normalizar_texto(valor: str) -> str:
    """
    Normaliza texto para comparaciones:
    - pasa a minúsculas
    - quita espacios extra
    """
    if valor is None:
        return ""
    return re.sub(r"\s+", " ", str(valor).strip().lower())


def contiene_palabra(texto: str, palabra: str) -> bool:
    """
    True si `palabra` aparece como palabra completa dentro de `texto`
    (case insensitive)
    """
    if not texto or not palabra:
        return False
    patron = rf"\b{re.escape(palabra)}\b"
    return bool(re.search(patron, texto, re.IGNORECASE))


def asegurar_directorio(path: str):
    """
    Crea el directorio si no existe
    """
    if path and not os.path.exists(path):
        os.makedirs(path)


def safe_get(df, columna, default=""):
    """
    Devuelve df[columna] si existe, sino una serie con valor default
    """
    if columna in df.colum
