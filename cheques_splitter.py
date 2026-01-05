def dividir_por_responsable(df):    
    vals = df['Responsable'].fillna('').astype(str).str.strip().str.lower()
    
    
    df_martin = df[
        vals.str.contains(r'\bmartin\b|^contado$', na=False)
        | vals.str.contains('contado', na=False)
    ].copy()

    df_lorena = df[
        vals.str.contains('lore g|anticipado', na=False)
    ].copy()


    df_martin = df[vals.str.contains('martin|contado', na=False)].copy()
    df_lorena = df[vals.str.contains('lore g|anticipado', na=False)].copy()

    df_martin.to_excel("../martin.xlsx", index=False, sheet_name="Sheet 1")
    df_lorena.to_excel("../lorena.xlsx", index=False, sheet_name="Sheet 1")

    return df_martin, df_lorena
