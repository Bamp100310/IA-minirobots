import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from pyproj import Transformer

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data", "services.csv")
OUT = os.path.join(BASE, "figures")

os.makedirs(OUT, exist_ok=True)

df = pd.read_csv(DATA)

# -----------------------------------------------------------------------------
# Sistema de coordenadas
# -----------------------------------------------------------------------------
# EPSG:9377 = MAGNA-SIRGAS / Origen-Nacional.
# Se trabaja en metros para calcular las distancias euclidianas.
TO_9377 = Transformer.from_crs(
    "EPSG:4326",
    "EPSG:9377",
    always_xy=True
)


def project(lon, lat):
    x, y = TO_9377.transform(lon, lat)
    return np.asarray(x), np.asarray(y)


def xy(sub):
    x, y = project(
        sub.lon.to_numpy(),
        sub.lat.to_numpy()
    )
    return np.column_stack((x, y))


# -----------------------------------------------------------------------------
# Ventana de análisis
# -----------------------------------------------------------------------------
# Los datos corresponden a establecimientos de la cabecera municipal.
#
# IMPORTANTE:
# Esta ventana NO representa el perímetro urbano legal.
# Se utiliza únicamente como dominio espacial para poder visualizar y
# comparar las regiones de Voronoi.

ALL_POINTS = xy(df)

MIN_X = ALL_POINTS[:, 0].min()
MAX_X = ALL_POINTS[:, 0].max()
MIN_Y = ALL_POINTS[:, 1].min()
MAX_Y = ALL_POINTS[:, 1].max()

MARGIN = 1300.0

PLOT_BOUNDS = (
    MIN_X - MARGIN,
    MIN_Y - MARGIN,
    MAX_X + MARGIN,
    MAX_Y + MARGIN,
)

STUDY_WINDOW = Polygon([
    (PLOT_BOUNDS[0], PLOT_BOUNDS[1]),
    (PLOT_BOUNDS[2], PLOT_BOUNDS[1]),
    (PLOT_BOUNDS[2], PLOT_BOUNDS[3]),
    (PLOT_BOUNDS[0], PLOT_BOUNDS[3]),
])


# -----------------------------------------------------------------------------
# Voronoi mediante intersección de semiplanos
# -----------------------------------------------------------------------------
def clip_polygon_with_halfplane(polygon, a, b, c, eps=1e-9):
    """
    Recorta un polígono conservando los puntos que cumplen:

        a*x + b*y <= c

    Se utiliza el algoritmo de Sutherland-Hodgman.
    """

    if polygon.is_empty:
        return polygon

    coords = list(polygon.exterior.coords)

    result = []

    def value(point):
        x, y = point
        return a * x + b * y - c

    for i in range(len(coords) - 1):
        current = np.asarray(coords[i], dtype=float)
        next_point = np.asarray(coords[i + 1], dtype=float)

        current_value = value(current)
        next_value = value(next_point)

        current_inside = current_value <= eps
        next_inside = next_value <= eps

        if current_inside and next_inside:
            # Ambos puntos están dentro.
            result.append(next_point)

        elif current_inside and not next_inside:
            # Sale del semiplano.
            direction = next_point - current
            denominator = (
                a * direction[0] +
                b * direction[1]
            )

            if abs(denominator) > eps:
                t = -current_value / denominator
                intersection = current + t * direction
                result.append(intersection)

        elif not current_inside and next_inside:
            # Entra al semiplano.
            direction = next_point - current
            denominator = (
                a * direction[0] +
                b * direction[1]
            )

            if abs(denominator) > eps:
                t = -current_value / denominator
                intersection = current + t * direction
                result.append(intersection)

            result.append(next_point)

    if len(result) < 3:
        return Polygon()

    return Polygon(result).buffer(0)


def voronoi_cells(points, bounding_polygon):
    """
    Construye las celdas de Voronoi directamente dentro del dominio
    de análisis.

    Para cada punto p_i se conserva la región:

        ||x - p_i|| <= ||x - p_j||

    para todos los demás puntos p_j.

    Esto garantiza que cada celda contiene exactamente los puntos
    cuyo sitio generador es el más cercano.
    """

    n = len(points)

    if n == 0:
        return []

    cells = []

    for i in range(n):
        cell = bounding_polygon

        p_i = points[i]

        for j in range(n):
            if i == j:
                continue

            p_j = points[j]

            # Condición:
            #
            # ||x-p_i||² <= ||x-p_j||²
            #
            # Se simplifica a:
            #
            # 2(p_j-p_i)·x <= ||p_j||² - ||p_i||²

            direction = p_j - p_i

            a = 2.0 * direction[0]
            b = 2.0 * direction[1]

            c = (
                np.dot(p_j, p_j)
                - np.dot(p_i, p_i)
            )

            cell = clip_polygon_with_halfplane(
                cell,
                a,
                b,
                c
            )

            if cell.is_empty:
                break

        cells.append(cell)

    return cells


# -----------------------------------------------------------------------------
# Dibujar polígonos
# -----------------------------------------------------------------------------
def draw_polygon(ax, geom, alpha=0.20):
    """
    Dibuja una celda de Voronoi.
    """

    if geom.is_empty:
        return

    if geom.geom_type == "Polygon":

        x, y = geom.exterior.xy

        ax.fill(
            x,
            y,
            alpha=alpha
        )

        ax.plot(
            x,
            y,
            linewidth=0.8
        )

    elif geom.geom_type == "MultiPolygon":

        for part in geom.geoms:

            x, y = part.exterior.xy

            ax.fill(
                x,
                y,
                alpha=alpha
            )

            ax.plot(
                x,
                y,
                linewidth=0.8
            )


# -----------------------------------------------------------------------------
# Etiquetas
# -----------------------------------------------------------------------------
def annotate_points(ax, points, sub, prefix):
    """
    Coloca etiquetas con desplazamientos diferentes para reducir
    el traslape visual.

    Se utiliza una caja blanca y una línea de conexión para mantener
    la identificación asociada al punto.
    """

    offsets = [
        (8, 8),
        (8, -14),
        (-8, 8),
        (-8, -14),
        (12, 20),
        (-12, 20),
        (12, -26),
        (-12, -26),
    ]

    for i, row in sub.iterrows():

        x, y = points[i]

        dx, dy = offsets[i % len(offsets)]

        ha = "left" if dx > 0 else "right"
        va = "bottom" if dy > 0 else "top"

        ax.annotate(
            f"{prefix}{i + 1}",
            xy=(x, y),
            xytext=(dx, dy),
            textcoords="offset points",
            fontsize=9,
            fontweight="bold",
            ha=ha,
            va=va,
            bbox=dict(
                boxstyle="round,pad=0.25",
                facecolor="white",
                edgecolor="black",
                alpha=0.85,
            ),
            arrowprops=dict(
                arrowstyle="-",
                linewidth=0.6,
                alpha=0.7,
            ),
            zorder=5,
        )


# -----------------------------------------------------------------------------
# Gráficos individuales
# -----------------------------------------------------------------------------
def plot_type(kind, title, filename, prefix):

    sub = (
        df[df.tipo == kind]
        .copy()
        .reset_index(drop=True)
    )

    points = xy(sub)

    fig, ax = plt.subplots(
        figsize=(10, 8)
    )

    # -------------------------------------------------------------------------
    # Calcular Voronoi
    # -------------------------------------------------------------------------

    if len(points) >= 1:

        cells = voronoi_cells(
            points,
            STUDY_WINDOW
        )

        for cell in cells:
            draw_polygon(
                ax,
                cell
            )

    # -------------------------------------------------------------------------
    # Ventana de análisis
    # -------------------------------------------------------------------------

    bx, by = STUDY_WINDOW.exterior.xy

    ax.plot(
        bx,
        by,
        linewidth=1.5,
        linestyle="--",
        label="Ventana de análisis",
        zorder=4,
    )

    # -------------------------------------------------------------------------
    # Puntos
    # -------------------------------------------------------------------------

    ax.scatter(
        points[:, 0],
        points[:, 1],
        s=70,
        edgecolor="black",
        zorder=6,
    )

    # -------------------------------------------------------------------------
    # Etiquetas
    # -------------------------------------------------------------------------

    annotate_points(
        ax,
        points,
        sub,
        prefix
    )

    # -------------------------------------------------------------------------
    # Identificación de establecimientos
    # -------------------------------------------------------------------------

    legend_text = "\n".join(
        [
            f"{prefix}{i + 1}: {row['nombre']}"
            for i, row in sub.iterrows()
        ]
    )

    ax.text(
        0.02,
        0.98,
        legend_text,
        transform=ax.transAxes,
        va="top",
        ha="left",
        fontsize=7,
        bbox=dict(
            boxstyle="round,pad=0.5",
            facecolor="white",
            edgecolor="black",
            alpha=0.9,
        ),
        zorder=10,
    )

    # -------------------------------------------------------------------------
    # Configuración
    # -------------------------------------------------------------------------

    ax.set_xlim(
        PLOT_BOUNDS[0],
        PLOT_BOUNDS[2]
    )

    ax.set_ylim(
        PLOT_BOUNDS[1],
        PLOT_BOUNDS[3]
    )

    ax.set_aspect(
        "equal",
        adjustable="box"
    )

    ax.set_xlabel(
        "Este (m) — EPSG:9377"
    )

    ax.set_ylabel(
        "Norte (m) — EPSG:9377"
    )

    ax.set_title(title)

    ax.grid(
        alpha=0.2
    )

    ax.legend(
        loc="lower left",
        fontsize=8
    )

    ax.text(
        0.01,
        0.01,
        "Ejercicio académico: análisis de proximidad en la cabecera municipal.\n"
        "La ventana mostrada no representa el perímetro urbano legal.",
        transform=ax.transAxes,
        fontsize=7,
        bbox=dict(
            boxstyle="round,pad=0.3",
            facecolor="white",
            alpha=0.8,
        ),
    )

    fig.tight_layout()

    fig.savefig(
        os.path.join(
            OUT,
            filename
        ),
        dpi=220,
        bbox_inches="tight"
    )

    plt.close(fig)


# -----------------------------------------------------------------------------
# Generación de los diagramas
# -----------------------------------------------------------------------------

plot_type(
    "farmacia",
    "Diagrama de Voronoi — Droguerías/Farmacias (cabecera municipal)",
    "voronoi_farmacias.png",
    "F",
)

plot_type(
    "salud",
    "Diagrama de Voronoi — Centros de atención de salud (cabecera municipal)",
    "voronoi_salud.png",
    "S",
)

plot_type(
    "colegio",
    "Diagrama de Voronoi — Instituciones educativas (cabecera municipal)",
    "voronoi_colegios.png",
    "C",
)


# -----------------------------------------------------------------------------
# Comparación de los tres tipos de servicio
# -----------------------------------------------------------------------------

fig, ax = plt.subplots(
    figsize=(10, 8)
)

markers = {
    "farmacia": "o",
    "salud": "s",
    "colegio": "^",
}

labels = {
    "farmacia": "Droguerías",
    "salud": "Salud",
    "colegio": "Colegios",
}

for kind in [
    "farmacia",
    "salud",
    "colegio"
]:

    sub = df[df.tipo == kind]

    points = xy(sub)

    ax.scatter(
        points[:, 0],
        points[:, 1],
        s=55,
        marker=markers[kind],
        label=labels[kind],
        alpha=0.85,
        edgecolor="black",
    )


bx, by = STUDY_WINDOW.exterior.xy

ax.plot(
    bx,
    by,
    linewidth=1.5,
    linestyle="--",
    label="Ventana de análisis",
)

ax.set_xlim(
    PLOT_BOUNDS[0],
    PLOT_BOUNDS[2]
)

ax.set_ylim(
    PLOT_BOUNDS[1],
    PLOT_BOUNDS[3]
)

ax.set_aspect(
    "equal",
    adjustable="box"
)

ax.grid(
    alpha=0.2
)

ax.legend()

ax.set_xlabel(
    "Este (m) — EPSG:9377"
)

ax.set_ylabel(
    "Norte (m) — EPSG:9377"
)

ax.set_title(
    "Distribución conjunta de servicios — cabecera municipal"
)

fig.tight_layout()

fig.savefig(
    os.path.join(
        OUT,
        "distribucion_conjunta.png"
    ),
    dpi=220,
    bbox_inches="tight"
)

plt.close(fig)