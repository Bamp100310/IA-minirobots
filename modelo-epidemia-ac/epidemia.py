import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# ============================================================
# MODELO DE DIFUSIÓN DE UNA ENFERMEDAD
# Autómata Celular Probabilístico
# ============================================================

# -------------------------
# Parámetros del modelo
# -------------------------

TAMANO_GRID = 50

# Probabilidad de contagio por cada vecino infectado
PROB_CONTAGIO = 0.2

# Probabilidad de recuperación de una persona infectada
PROB_RECUPERACION = 0.05

# Cantidad inicial de personas infectadas
INFECTADOS_INICIALES = 5

# Cantidad de pasos de tiempo de la simulación
PASOS = 200

# Velocidad de la animación (milisegundos)
INTERVALO = 100


# -------------------------
# Estados de las células
# -------------------------

SUSCEPTIBLE = 0
INFECTADO = 1
RECUPERADO = 2


# ============================================================
# CREACIÓN DE LA POBLACIÓN
# ============================================================

def crear_poblacion():
    """
    Crea una cuadrícula donde cada celda representa una persona.

    Inicialmente todas las personas son susceptibles.
    Luego se seleccionan algunas personas aleatoriamente
    para comenzar la epidemia.
    """

    poblacion = np.full(
        (TAMANO_GRID, TAMANO_GRID),
        SUSCEPTIBLE,
        dtype=int
    )

    # Seleccionar posiciones aleatorias para los infectados
    posiciones = np.random.choice(
        TAMANO_GRID * TAMANO_GRID,
        INFECTADOS_INICIALES,
        replace=False
    )

    for posicion in posiciones:
        fila = posicion // TAMANO_GRID
        columna = posicion % TAMANO_GRID

        poblacion[fila, columna] = INFECTADO

    return poblacion


# ============================================================
# CONTAR VECINOS INFECTADOS
# ============================================================

def contar_vecinos_infectados(poblacion, fila, columna):
    """
    Cuenta cuántos vecinos infectados tiene una persona.

    Se utiliza una vecindad de Moore:
    las 8 celdas que rodean a la celda actual.

        X X X
        X C X
        X X X

    C = celda actual
    X = vecinos
    """

    cantidad = 0

    filas, columnas = poblacion.shape

    for df in [-1, 0, 1]:
        for dc in [-1, 0, 1]:

            # No contar la celda actual
            if df == 0 and dc == 0:
                continue

            nueva_fila = fila + df
            nueva_columna = columna + dc

            # Verificar que el vecino esté dentro de la cuadrícula
            if (
                0 <= nueva_fila < filas
                and 0 <= nueva_columna < columnas
            ):
                if poblacion[nueva_fila, nueva_columna] == INFECTADO:
                    cantidad += 1

    return cantidad


# ============================================================
# ACTUALIZACIÓN DEL AUTÓMATA CELULAR
# ============================================================

def actualizar(poblacion):
    """
    Calcula el siguiente estado de toda la población.

    Reglas:

    1. SUSCEPTIBLE:
       Si tiene vecinos infectados, existe una probabilidad
       de contagiarse.

       P(infección) = 1 - (1 - beta)^n

       donde:
       beta = probabilidad de contagio por contacto
       n = número de vecinos infectados

    2. INFECTADO:
       Existe una probabilidad de recuperarse.

    3. RECUPERADO:
       Permanece recuperado.
    """

    nueva_poblacion = poblacion.copy()

    filas, columnas = poblacion.shape

    for fila in range(filas):
        for columna in range(columnas):

            estado = poblacion[fila, columna]

            # ---------------------------------------------
            # Persona susceptible
            # ---------------------------------------------

            if estado == SUSCEPTIBLE:

                vecinos_infectados = contar_vecinos_infectados(
                    poblacion,
                    fila,
                    columna
                )

                if vecinos_infectados > 0:

                    # Probabilidad de infectarse
                    probabilidad = (
                        1 - (1 - PROB_CONTAGIO) ** vecinos_infectados
                    )

                    # Número aleatorio entre 0 y 1
                    if np.random.random() < probabilidad:
                        nueva_poblacion[fila, columna] = INFECTADO

            # ---------------------------------------------
            # Persona infectada
            # ---------------------------------------------

            elif estado == INFECTADO:

                # Probabilidad de recuperación
                if np.random.random() < PROB_RECUPERACION:
                    nueva_poblacion[fila, columna] = RECUPERADO

            # ---------------------------------------------
            # Persona recuperada
            # ---------------------------------------------

            elif estado == RECUPERADO:

                # Los recuperados permanecen recuperados
                nueva_poblacion[fila, columna] = RECUPERADO

    return nueva_poblacion


# ============================================================
# CONTAR ESTADOS
# ============================================================

def contar_estados(poblacion):
    """
    Cuenta cuántas personas existen en cada estado.
    """

    susceptibles = np.sum(poblacion == SUSCEPTIBLE)
    infectados = np.sum(poblacion == INFECTADO)
    recuperados = np.sum(poblacion == RECUPERADO)

    return susceptibles, infectados, recuperados


# ============================================================
# INICIALIZAR SIMULACIÓN
# ============================================================

poblacion = crear_poblacion()

historial_susceptibles = []
historial_infectados = []
historial_recuperados = []


# ============================================================
# CONFIGURACIÓN DE LA FIGURA
# ============================================================

fig, (ax_grid, ax_stats) = plt.subplots(
    1,
    2,
    figsize=(12, 5)
)


# -------------------------
# Visualización del grid
# -------------------------

imagen = ax_grid.imshow(
    poblacion,
    vmin=0,
    vmax=2,
    interpolation="nearest"
)

ax_grid.set_title("Difusión de una enfermedad")
ax_grid.set_xlabel("Población")
ax_grid.set_ylabel("Población")


# -------------------------
# Gráfica de estadísticas
# -------------------------

linea_susceptibles, = ax_stats.plot(
    [],
    [],
    label="Susceptibles"
)

linea_infectados, = ax_stats.plot(
    [],
    [],
    label="Infectados"
)

linea_recuperados, = ax_stats.plot(
    [],
    [],
    label="Recuperados"
)

ax_stats.set_xlim(0, PASOS)
ax_stats.set_ylim(0, TAMANO_GRID * TAMANO_GRID)

ax_stats.set_xlabel("Paso de tiempo")
ax_stats.set_ylabel("Cantidad de personas")
ax_stats.set_title("Evolución de la población")

ax_stats.legend()


# Texto para mostrar las cantidades
texto = ax_grid.text(
    0.02,
    0.95,
    "",
    transform=ax_grid.transAxes,
    verticalalignment="top",
    bbox=dict(facecolor="white", alpha=0.8)
)


# ============================================================
# FUNCIÓN DE ANIMACIÓN
# ============================================================

def animar(paso):
    """
    Ejecuta un paso de la simulación y actualiza
    las gráficas.
    """

    global poblacion

    # Actualizar el estado de la población
    poblacion = actualizar(poblacion)

    # Contar los estados actuales
    susceptibles, infectados, recuperados = contar_estados(
        poblacion
    )

    # Guardar estadísticas
    historial_susceptibles.append(susceptibles)
    historial_infectados.append(infectados)
    historial_recuperados.append(recuperados)

    # Actualizar la imagen de la cuadrícula
    imagen.set_data(poblacion)

    # Actualizar las líneas de la gráfica
    pasos_actuales = range(len(historial_susceptibles))

    linea_susceptibles.set_data(
        pasos_actuales,
        historial_susceptibles
    )

    linea_infectados.set_data(
        pasos_actuales,
        historial_infectados
    )

    linea_recuperados.set_data(
        pasos_actuales,
        historial_recuperados
    )

    # Actualizar información
    texto.set_text(
        f"Paso: {paso + 1}\n"
        f"Susceptibles: {susceptibles}\n"
        f"Infectados: {infectados}\n"
        f"Recuperados: {recuperados}"
    )

    return (
        imagen,
        linea_susceptibles,
        linea_infectados,
        linea_recuperados,
        texto
    )


# ============================================================
# EJECUTAR ANIMACIÓN
# ============================================================

animacion = FuncAnimation(
    fig,
    animar,
    frames=PASOS,
    interval=INTERVALO,
    repeat=False
)


plt.tight_layout()
plt.show()