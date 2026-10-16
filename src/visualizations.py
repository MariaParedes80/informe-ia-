import matplotlib.pyplot as plt
import seaborn as sns


def generar_grafico_distribucion(df, columna_numerica):
    """Genera un gráfico estadístico seguro de distribución."""
    fig, ax = plt.subplots(figsize=(8, 4))
    if columna_numerica in df.columns:
        sns.histplot(df[columna_numerica], kde=True, ax=ax, color="#1f77b4")
        ax.set_title(f"Distribución de {columna_numerica}")
    return fig