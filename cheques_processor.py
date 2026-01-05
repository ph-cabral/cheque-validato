import pandas as pd
from datetime import datetime
from excel_utils import limpiar_fecha

def obtener_codigo_banco(nombre_banco, df_codigos):
    if pd.isna(nombre_banco):
        return ''
    nb = str(nombre_banco).lower()
    for _, row in df_codigos.iterrows():
        if str(row['NombreBanco']).lower() in nb:
            return row['Codigo']
    return ''

def procesar_cheques(df, df_codigos):
    if df.shape[1] > 20:
        df.rename(columns={df.columns[20]: 'Responsable'}, inplace=True)
        
    df['Fecha de emisión'] = df['Fecha de emisión'].apply(limpiar_fecha)
    df['Fecha de pago'] = df['Fecha de pago'].apply(limpiar_fecha)
    df = df[df['Fecha de emisión'].notna()].copy()

    df_nuevo = pd.DataFrame()
    fecha_recepcion = datetime.today().strftime('%d/%m/%Y')

    df_nuevo["ID"] = df.get('ID del cheque', '')
    df_nuevo['Fecha Recepción'] = fecha_recepcion
    df_nuevo['Importe'] = df.get('Importe', '')
    df_nuevo['Es Cheque Electrónico SI o NO'] = 'SI'

    df_nuevo['Fecha Emisión'] = df['Fecha de emisión'].dt.strftime('%d/%m/%Y')
    df_nuevo['Fecha Disponibilidad'] = df['Fecha de pago'].dt.strftime('%d/%m/%Y')
    df_nuevo['Fecha Acreditación'] = (df['Fecha de pago'] + pd.Timedelta(days=2)).dt.strftime('%d/%m/%Y')

    df_nuevo['Código Banco'] = df['Banco emisor'].apply(lambda x: obtener_codigo_banco(x, df_codigos))
    df_nuevo['Nombre Banco'] = ''
    df_nuevo['Plaza Código Postal'] = df.get('C.P del cheque', '')
    df_nuevo['Número Cheque'] = df.get('Nº de cheque', '')
    df_nuevo['Cuenta Librador'] = ''
    df_nuevo['CUIT Librador'] = df.get('CUIT/CUIL/CDI.2', '')
    df_nuevo['Nombre Librador'] = df.get('Razón social', '')
    df_nuevo['Observaciones'] =  df.get('Cláusula', '')
    df_nuevo['Propio SI o NO'] = ''
    df_nuevo['Cuit Ultimo Endoso'] = ''
    df_nuevo['Responsable'] = df.get('Responsable', '')
    
    # máscara: contiene la palabra 'no' como palabra independiente (captura "no", "no a la orden", etc.)
    mask_no = df_nuevo['Observaciones'].str.contains(r'\bno\b', case=False, na=False)

    # dejar el texto en mayúsculas si cumple, sino cadena vacía
    df_nuevo['Observaciones'] = df_nuevo['Observaciones'].where(mask_no, '').str.upper()

    # Asegurar que sea la ÚLTIMA columna y con ese nombre
    cols = [c for c in df_nuevo.columns if c != 'Responsable'] + ['Responsable']
    df_nuevo = df_nuevo[cols]
    return df_nuevo