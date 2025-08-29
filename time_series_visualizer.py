import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from calendar import month_name

# Importar datos con índice de fecha
# El archivo debe llamarse exactamente 'fcc-forum-pageviews.csv' y tener columnas: 'date','value'
df = pd.read_csv(
    "fcc-forum-pageviews.csv",
    parse_dates=["date"],
    index_col="date"
)

# Limpiar datos: quitar 2.5% inferior y 2.5% superior de 'value'
df = df[(df["value"] >= df["value"].quantile(0.025)) &
        (df["value"] <= df["value"].quantile(0.975))].copy()

def draw_line_plot():
    """
    Dibuja línea de page views diarios.
    Título: Daily freeCodeCamp Forum Page Views 5/2016-12/2019
    Ejes: x='Date', y='Page Views'
    Guarda como 'line_plot.png' y retorna fig.
    """
    df_line = df.copy()

    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df_line.index, df_line["value"])
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    fig.savefig("line_plot.png")
    return fig


def draw_bar_plot():
    """
    Barras: promedio diario por mes agrupado por año (como en Figure_2.png).
    - Leyenda de meses con título 'Months'
    - Ejes: x='Years', y='Average Page Views'
    Guarda como 'bar_plot.png' y retorna fig.
    """
    df_bar = df.copy()
    df_bar["year"] = df_bar.index.year
    df_bar["month"] = df_bar.index.month

    # Promedio por año/mes
    grouped = df_bar.groupby(["year", "month"])["value"].mean().round(2)

    # Pivot para que columnas sean meses en orden 1..12
    pivot = grouped.unstack(level="month")

    # Etiquetas de meses en texto completo (Jan..Dec en inglés largo para leyenda)
    month_labels = [month_name[m] for m in range(1, 13)]

    # Plot
    fig = pivot.plot(kind="bar", figsize=(15, 8)).get_figure()
    ax = plt.gca()
    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")
    ax.legend(title="Months", labels=month_labels)

    fig.tight_layout()
    fig.savefig("bar_plot.png")
    return fig


def draw_box_plot():
    """
    Box plots lado a lado:
    - Year-wise Box Plot (Trend): distribución por año
    - Month-wise Box Plot (Seasonality): distribución por mes (Jan..Dec)
    Guarda como 'box_plot.png' y retorna fig.
    """
    # Preparación de datos para box plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box["year"] = df_box["date"].dt.year
    df_box["month"] = df_box["date"].dt.strftime("%b")

    # Orden de meses
    month_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    # Figura con dos subplots adyacentes
    fig, axes = plt.subplots(1, 2, figsize=(18, 6))

    # Year-wise
    sns.boxplot(
        x="year", y="value",
        data=df_box, ax=axes[0]
    )
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # Month-wise
    sns.boxplot(
        x="month", y="value",
        data=df_box,
        order=month_order,
        ax=axes[1]
    )
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    fig.tight_layout()
    fig.savefig("box_plot.png")
    return fig
