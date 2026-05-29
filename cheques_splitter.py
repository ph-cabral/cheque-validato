
import pandas as pd
from excel_utils import formatear_excel

columns_mag = [
    'Fecha Recepción',
    'Importe',
    'Es Cheque Electrónico SI o NO',
    'Fecha Emisión',
    'Fecha Disponibilidad',
    'Fecha Acreditación',
    'Código Banco',
    'Nombre Banco',
    'Plaza Código Postal',
    'Número Cheque',
    'Cuenta Librador',
    'CUIT Librador',
    'Nombre Librador',
    'Observaciones',
    'Propio SI o NO',
    'Cuit Ultimo Endoso',
    'Responsable']

columns = [
    'Número Cheque',
    'Observaciones',
    'Dueño',
    'Cliente CUIT/CUIL/CDI',
    'Fecha Disponibilidad',
    'Fecha Emisión',
    'Importe',
    'Nombre Banco',
    'CUIT Librador',
    'Plaza Código Postal'
    ]

def _agrupar_con_subtotales(df):
    """Mantiene filas y agrega subtotal de Importe debajo de cada CUIT Librador."""
    if df.empty:
        return df.copy()

    df = df.copy()
    df['Importe'] = pd.to_numeric(df['Importe'], errors='coerce')
    bloques = []
    for cuit, grupo in df.groupby('Cliente CUIT/CUIL/CDI', sort=False, dropna=False):
    # for cuit, grupo in df.groupby(df.iloc[:, 3], sort=False, dropna=False):    
        bloques.append(grupo)
        fila_sum = pd.DataFrame([{c: None for c in df.columns}])
        fila_sum.at[0, 'Importe'] = grupo['Importe'].sum()
        bloques.append(fila_sum)

    return pd.concat(bloques, ignore_index=True)


def dividir_por_responsable(df):

    vals = df['Responsable'].fillna('').astype(str).str.strip().str.lower()
    df['Importe'] = df['Importe'].astype(float)
    df['Número Cheque'] = df['Número Cheque'].astype(int)
    df['Código Banco'] = df['Código Banco'].astype(int)
    df['Plaza Código Postal'] = df['Plaza Código Postal'].astype(int)
    df['CUIT Librador'] = df['CUIT Librador'].astype(int)
    
    df_martin = df[vals.str.contains('martin|contado', na=False)].copy()
    df_lorena = df[vals.str.contains('lore g|anticipado', na=False)].copy()

    _agrupar_con_subtotales(df_martin[columns]).to_excel(
        "../martin_sumados.xlsx", index=False, sheet_name="Sheet 1"
    )
    _agrupar_con_subtotales(df_lorena[columns]).to_excel(
        "../lorena_sumados.xlsx", index=False, sheet_name="Sheet 1"
    )
    
    df_martin['Nombre Banco'] = ''
    df_lorena['Nombre Banco'] = ''
    
    df_martin[columns_mag].to_excel("../martin.xlsx", index=False, sheet_name="Sheet 1")
    df_lorena[columns_mag].to_excel("../lorena.xlsx", index=False, sheet_name="Sheet 1")
    
    formatear_excel("../lorena_sumados.xlsx")
    formatear_excel("../martin_sumados.xlsx")

    return df_martin, df_lorena



