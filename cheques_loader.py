import pandas as pd

def obtener_ultima_tabla(df):
    df_work = df.copy()
    cols = df_work.columns[1:19] if df_work.shape[1] >= 19 else df_work.columns[1:]

    not_empty = df_work[cols].fillna('').astype(str).apply(lambda c: c.str.strip().ne(''))
    mask = not_empty.any(axis=1)

    grupos = (mask != mask.shift(fill_value=False)).cumsum()
    ultimo_grupo = grupos[mask].unique()[-1]
    idxs = grupos[grupos == ultimo_grupo].index

    return df_work.loc[idxs[0]:idxs[-1]].copy()
