import os
import time
import requests
from openpyxl import Workbook
from openpyxl.styles import PatternFill

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CERT_PATH = os.path.join(BASE_DIR, "cert.pem")


def validar_cuit(cuit: str) -> bool:
    if len(cuit) != 11 or not cuit.isdigit():
        return False
    pesos = [5,4,3,2,7,6,5,4,3,2]
    s = sum(int(cuit[i]) * pesos[i] for i in range(10))
    return ((11 - (s % 11)) % 11) == int(cuit[-1])


def generar_cheques_rechazados(cuits):
    wb = Workbook()
    ws = wb.active
    ws.append(["CUIT", "NOMBRE", "NUM CHEQUE", "FECHA RECHAZO", "MONTO"])

    base_url = "https://api.bcra.gob.ar/CentralDeDeudores/v1.0/Deudas/ChequesRechazados"
    colors = ["FFFFDF20", "FF9AE630", "FF7C86FF"]
    color_index = 0
    
    if not os.path.exists(CERT_PATH):
        raise FileNotFoundError(f"No se encontró el certificado: {CERT_PATH}")


    for cuit in cuits:
        if not validar_cuit(cuit):
            continue

        r = requests.get(
            f"{base_url}/{cuit}",
            timeout=10,
            verify=CERT_PATH
        )

        if r.status_code != 200:
            continue

        data = r.json().get("results", {})
        fill = PatternFill(
            start_color=colors[color_index % 3],
            end_color=colors[color_index % 3],
            fill_type="solid"
        )

        for causal in data.get("causales", []):
            for entidad in causal.get("entidades", []):
                for det in entidad.get("detalle", []):
                    ws.append([
                        data.get("identificacion", ""),
                        data.get("denominacion", ""),
                        det.get("nroCheque", ""),
                        det.get("fechaRechazo", ""),
                        det.get("monto", "")
                    ])
                    for cell in ws[ws.max_row]:
                        cell.fill = fill

        color_index += 1
        time.sleep(3)

    wb.save("../cheques_Rechazados.xlsx")
