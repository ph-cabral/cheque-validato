import os
import pandas as pd
import logging

# Configurar logger
logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def controlar_duplicados(df):
    """
    Controla duplicados comparando con archivo histórico de IDs.
    Actualiza automáticamente el control con cada ejecución.
    
    Maneja casos de:
    - Archivo no existente
    - Archivo vacío o corrupto
    - Archivo sin columna ID
    
    Args:
        df: DataFrame con columna 'ID'
        
    Returns:
        DataFrame sin IDs duplicados del histórico
    """
    control_path = "control.xlsx"
    
    # Validar que el DataFrame de entrada tenga la columna ID
    if "ID" not in df.columns:
        raise ValueError("El DataFrame de entrada no contiene la columna 'ID'")
    
    # Función auxiliar para inicializar/recrear el archivo de control
    def inicializar_control():
        df[["ID"]].to_excel(control_path, index=False)
        # logger.info("✅ Archivo de control inicializado")
        # logger.info(f"   Total IDs guardados: {len(df)}")
        return df
    
    # Si no existe el archivo, crearlo
    if not os.path.exists(control_path):
        # logger.info("ℹ️  Archivo de control no encontrado, creando uno nuevo...")
        return inicializar_control()
    
    try:
        # Leer control existente
        df_control = pd.read_excel(control_path)
        
        # Validar que no esté vacío
        if df_control.empty:
            # logger.warning("⚠️  Archivo de control vacío, reinicializando...")
            return inicializar_control()
        
        # Validar que tenga la columna ID
        if "ID" not in df_control.columns:
            # logger.warning("⚠️  Archivo de control corrupto (sin columna 'ID'), reinicializando...")
            return inicializar_control()
        
        # Validar que la columna ID tenga datos
        if df_control["ID"].isna().all():
            # logger.warning("⚠️  Columna 'ID' sin datos válidos, reinicializando...")
            return inicializar_control()
        
        # Obtener IDs ya procesados (convertir a string para evitar problemas de tipo)
        ids_procesados = set(df_control["ID"].dropna().astype(str))
        ids_actuales = set(df["ID"].dropna().astype(str))
        
        # Calcular IDs nuevos
        ids_nuevos_set = ids_actuales - ids_procesados
        
        # Filtrar duplicados
        df_limpio = df[df["ID"].astype(str).isin(ids_nuevos_set)].copy()
        
        # Si no hay IDs nuevos, retornar DataFrame vacío
        if df_limpio.empty:
            # logger.info("ℹ️  No hay IDs nuevos para procesar")
            # logger.info(f"   Total histórico en control: {len(ids_procesados)}")
            return df_limpio
        
        # Actualizar control con IDs nuevos
        ids_nuevos_df = df_limpio[["ID"]].drop_duplicates()
        df_control_actualizado = pd.concat([df_control, ids_nuevos_df], ignore_index=True)
        
        # Guardar con manejo de errores
        try:
            df_control_actualizado.to_excel(control_path, index=False)
        except PermissionError:
            # logger.error("❌ No se puede escribir en control.xlsx (archivo abierto o sin permisos)")
            raise
        
        # logger.info(f"✅ IDs nuevos procesados: {len(ids_nuevos_df)}")
        # logger.info(f"   Total histórico actualizado: {len(df_control_actualizado)}")
        
        return df_limpio
        
    except pd.errors.EmptyDataError:
        # logger.warning("⚠️  Archivo de control corrupto (vacío), reinicializando...")
        return inicializar_control()
        
    except Exception as e:
        # logger.error(f"❌ Error inesperado al controlar duplicados: {str(e)}")
        # logger.error(f"   Tipo de error: {type(e).__name__}")
        raise


# ============================================
# CÓDIGO DE PRUEBA (comentar en producción)
# ============================================
if __name__ == "__main__":
    # Crear DataFrame de prueba
    df_test = pd.DataFrame({
        'ID': ['001', '002', '003', '004', '005'],
        'Nombre': ['A', 'B', 'C', 'D', 'E']
    })
    
    # print("\n=== Prueba 1: Primera ejecución ===")
    resultado = controlar_duplicados(df_test)
    # print(f"IDs procesados: {len(resultado)}\n")
    
    # print("=== Prueba 2: Con duplicados ===")
    df_test2 = pd.DataFrame({
        'ID': ['003', '004', '006'],  # 003 y 004 son duplicados
        'Nombre': ['C', 'D', 'F']
    })
    resultado = controlar_duplicados(df_test2)
    # print(f"IDs nuevos: {len(resultado)}")
    # print(f"IDs filtrados: {resultado['ID'].tolist()}\n")
    
    # print("=== Prueba 3: Simulando archivo corrupto ===")
    # Crear archivo vacío
    pd.DataFrame().to_excel("control.xlsx", index=False)
    resultado = controlar_duplicados(df_test)
    # print(f"IDs procesados tras recuperación: {len(resultado)}\n")
