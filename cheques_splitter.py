# def dividir_por_responsable(df):    
#     vals = df['Responsable'].fillna('').astype(str).str.strip().str.lower()
    
    
#     df_martin = df[
#         vals.str.contains(r'\bmartin\b|^contado$', na=False)
#         | vals.str.contains('contado', na=False)
#     ].copy()

#     df_lorena = df[
#         vals.str.contains('lore g|anticipado', na=False)
#     ].copy()


#     df_martin = df[vals.str.contains('martin|contado', na=False)].copy()
#     df_lorena = df[vals.str.contains('lore g|anticipado', na=False)].copy()

#     df_martin.to_excel("../martin.xlsx", index=False, sheet_name="Sheet 1")
#     df_lorena.to_excel("../lorena.xlsx", index=False, sheet_name="Sheet 1")

#     return df_martin, df_lorena
import pandas as pd


def _agrupar_con_subtotales(df):
    """Mantiene filas y agrega subtotal de Importe debajo de cada CUIT Librador."""
    if df.empty:
        return df.copy()

    df = df.copy()
    df['Importe'] = pd.to_numeric(df['Importe'], errors='coerce')

    bloques = []
    for cuit, grupo in df.groupby('CUIT Librador', sort=False, dropna=False):
        bloques.append(grupo)
        if len(grupo) > 1:
            fila_sum = pd.DataFrame([{c: None for c in df.columns}])
            fila_sum.at[0, 'Importe'] = grupo['Importe'].sum()
            bloques.append(fila_sum)

    return pd.concat(bloques, ignore_index=True)


def dividir_por_responsable(df):
    vals = df['Responsable'].fillna('').astype(str).str.strip().str.lower()

    df_martin = df[vals.str.contains('martin|contado', na=False)].copy()
    df_lorena = df[vals.str.contains('lore g|anticipado', na=False)].copy()

    df_martin.to_excel("../martin.xlsx", index=False, sheet_name="Sheet 1")
    df_lorena.to_excel("../lorena.xlsx", index=False, sheet_name="Sheet 1")

    _agrupar_con_subtotales(df_martin).to_excel(
        "../martin_sumados.xlsx", index=False, sheet_name="Sheet 1"
    )
    _agrupar_con_subtotales(df_lorena).to_excel(
        "../lorena_sumados.xlsx", index=False, sheet_name="Sheet 1"
    )

    return df_martin, df_lorena