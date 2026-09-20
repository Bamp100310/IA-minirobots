# 2. Autómatas Celulares

Desarrollo de los ejercicios y problemas propuestos en la sección 2.10 del capítulo *Autómatas Celulares*
(José J. Martínez P.), curso de Inteligencia Artificial y Minirobots.

El documento [`Documento_Automatas_celulares.pdf`](Documento_Automatas_celulares.pdf) contiene las
respuestas escritas y remite a los programas, que están en la carpeta [`ejercicios`](ejercicios/).

## Ejercicios desarrollados

| Ejercicio | Enunciado | Solución |
|---|---|---|
| 1 | Observe sus comportamientos en la casa, en la universidad y en el medio de transporte que utiliza. Encuentre las reglas básicas de cada escenario. | En el documento. Describe cada escenario como un sistema con reglas explícitas e implícitas y lista sus reglas básicas: 6 para la casa, 6 para la universidad y 7 para el transporte público (TransMilenio). |
| 2 | Desarrolle un modelo de difusión de una enfermedad, un incendio forestal o una moda usando ACs probabilísticos, o simule un robot con dos ruedas que evite obstáculos. | [`ejercicios/modelo-epidemia-ac`](ejercicios/modelo-epidemia-ac/): difusión de una enfermedad con un autómata celular probabilístico de tipo SIR. |
| 3 | Simule un robot con tres sensores de distancia que recorre un espacio bidimensional con 4 objetos distribuidos aleatoriamente, sin chocar con ellos. | [`ejercicios/simulacion-robot-sensores`](ejercicios/simulacion-robot-sensores/): robot autónomo con sensores frontal, izquierdo y derecho. |
| 4 | Tome el plano de una ciudad pequeña, localice droguerías, centros de salud y colegios, y dibuje un diagrama de Voronoi por cada concepto. ¿Puede faltar alguno? ¿Hay relación entre los diagramas? | [`ejercicios/analisis-mediante-diagramas-de-voronoi`](ejercicios/analisis-mediante-diagramas-de-voronoi/) para el código y los diagramas; las respuestas a las preguntas, en el documento. |

El capítulo numera como 3 tanto el ejercicio del robot como el de Voronoi; aquí se numeran 3 y 4 para
distinguirlos.

## Descripción de los programas

### Ejercicio 2. Difusión de una enfermedad (`ejercicios/modelo-epidemia-ac`)

Autómata celular probabilístico sobre una cuadrícula de 50 × 50 (2 500 personas). Cada celda está en uno de
tres estados: susceptible, infectada o recuperada. Se usa la vecindad de Moore (8 vecinos) y estas reglas de
transición:

- **Susceptible → Infectado**, con probabilidad `P = 1 − (1 − β)ⁿ`, donde `β` es la probabilidad de contagio
  por contacto y `n` el número de vecinos infectados.
- **Infectado → Recuperado**, con probabilidad fija por paso.
- **Recuperado** permanece recuperado.

Parámetros en `epidemia.py`: `PROB_CONTAGIO = 0.2`, `PROB_RECUPERACION = 0.05`, `INFECTADOS_INICIALES = 5` y
`PASOS = 200`. Con β = 0.2, una persona con tres vecinos infectados se contagia con probabilidad
1 − 0.8³ ≈ 0.49 en ese paso.

La simulación se anima con Matplotlib y muestra la cuadrícula junto con la evolución de las tres
poblaciones. Como las transiciones son aleatorias, cada ejecución da un resultado distinto.

### Ejercicio 3. Robot con tres sensores (`ejercicios/simulacion-robot-sensores`)

Simulación en Pygame de un robot circular que se mueve en un espacio de 1000 × 700 con cuatro obstáculos
colocados al azar, lejos del punto de partida y separados entre sí.

- **Sensores.** Tres rayos, uno frontal y dos laterales a ±45°, con alcance máximo de 180 unidades. Cada
  sensor calcula la distancia al obstáculo más cercano que corta su rayo.
- **Decisión.** Si el sensor frontal detecta algo a menos de 70 unidades, el robot gira hacia el lado con
  más espacio libre. Si el obstáculo está a un lado, gira hacia el lado contrario.
- **Seguridad.** Si aun así hay contacto, el robot retrocede y gira 90°. En los bordes de la pantalla rebota.

La ventana muestra los tres rayos de los sensores y sus lecturas en tiempo real.

### Ejercicio 4. Diagramas de Voronoi (`ejercicios/analisis-mediante-diagramas-de-voronoi`)

A partir de la ubicación de droguerías, centros de salud y colegios de la cabecera de un municipio pequeño
(`data/services.csv`), el script `scripts/voronoi_services.py` genera un diagrama de Voronoi por cada tipo de
servicio y uno con la distribución conjunta. Las figuras quedan en `figures/`.

La conclusión principal, desarrollada en el documento, es que las celdas grandes señalan zonas geométricamente
más alejadas del servicio y son candidatas a estudiar, pero no demuestran por sí solas que falte un
establecimiento: para eso haría falta cruzarlas con población, demanda, capacidad y red vial.

## Estructura

```
2. Automatas celulares/
├── README.md
├── Documento_Automatas_celulares.pdf
└── ejercicios/
    ├── modelo-epidemia-ac/
    │   ├── README.md
    │   ├── epidemia.py
    │   └── requirements.txt
    ├── simulacion-robot-sensores/
    │   ├── README.md
    │   ├── main.py
    │   └── requirements.txt
    └── analisis-mediante-diagramas-de-voronoi/
        ├── README.md
        ├── requirements.txt
        ├── data/services.csv
        ├── scripts/voronoi_services.py
        └── figures/
```

## Ejecución

Cada programa tiene sus propias dependencias. Desde la carpeta del programa, dentro de `ejercicios/`:

```bash
cd ejercicios/modelo-epidemia-ac
pip install -r requirements.txt
python epidemia.py
```

| Programa | Carpeta | Comando | Dependencias |
|---|---|---|---|
| Difusión de una enfermedad | `ejercicios/modelo-epidemia-ac` | `python epidemia.py` | numpy, matplotlib |
| Robot con tres sensores | `ejercicios/simulacion-robot-sensores` | `python main.py` | pygame |
| Diagramas de Voronoi | `ejercicios/analisis-mediante-diagramas-de-voronoi` | `python scripts/voronoi_services.py` | ver su `requirements.txt` |

Los dos primeros abren una ventana con la animación, así que deben ejecutarse en un equipo local y no en
Colab.


## Referencias

- Martínez, J. J. (2026). *Autómatas Celulares*, capítulo 2. Material del curso Inteligencia Artificial y
  Minirobots, Universidad Nacional de Colombia.
- Mitchell, M. (2015). *Introduction to Complexity*. MOOC, Santa Fe Institute.
- Martínez, J. J. (2009). *Notas Vida Artificial*.
- Cortés, C. P. y Cubillos, M. G. (1999). *Desarrollo de Software Adaptativo para el Aprendizaje de Robots
  Móviles, Basado en Autómatas Celulares*. Facultad de Ingeniería, Universidad Nacional, Bogotá.