def obtener_resumen_estadistico(df):
    """Genera datos del análisis exploratorio descriptivo básico."""
    resumen = {
        "dimensiones": df.shape,
        "columnas": list(df.columns),
        "nulos": df.isnull().sum().to_dict(),
        "describir": df.describe(include="all").to_dict(),
    }
    return resumen