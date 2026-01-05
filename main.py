import os
import threading

from animacion import correr_animacion
from requirements_manager import instalar_requerimientos

instalar_requerimientos()

import pandas as pd
from cheques_loader import obtener_ultima_tabla
from cheques_processor import procesar_cheques
from cheques_rechazados import generar_cheques_rechazados
from cheques_splitter import dividir_por_responsable
from duplicados import controlar_duplicados

def proceso_principal():
    """Ejecuta todo el procesamiento de cheques"""
    
    archivo = os.path.abspath("../../Cheques Electronicos 2026.xlsx")

    df_origen = pd.read_excel(
        archivo,
        header=2,
        dtype=str
    )
    
    df = obtener_ultima_tabla(df_origen.iloc[:, :21])

    df_codigos = pd.read_excel(
        "../codigos_bancos.xlsx",
        header=None,
        names=['Codigo', 'NombreBanco']
    )

    df_final = procesar_cheques(df, df_codigos)
    df_control = controlar_duplicados(df_final)
    dividir_por_responsable(df_control)

    # df_control.to_excel("control.xlsx", index=False)
    generar_cheques_rechazados(df_control['CUIT Librador'].unique())


if __name__ == "__main__":
    # Evento para detener la animación
    stop_event = threading.Event()

    # Iniciar animación en hilo separado
    hilo_animacion = threading.Thread(
        target=correr_animacion,
        args=(stop_event,),
        daemon=True
    )
    hilo_animacion.start()

    try:
        # Ejecutar proceso principal
        proceso_principal()
        
    except Exception as e:
        # Si hay error, detener animación y mostrar
        stop_event.set()
        os.system("cls" if os.name == "nt" else "clear")
        print("\n")
        print("❌ ERROR:")
        print(f"   {str(e)}")
        raise
        
    finally:
        # Detener animación
        stop_event.set()
        
