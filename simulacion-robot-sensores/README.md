# Simulación de Robot Autónomo con Tres Sensores

## Descripción

Se implementa la simulación de un robot autónomo que se desplaza en un espacio bidimensional (2D) y evita cuatro obstáculos distribuidos aleatoriamente.

La simulación fue desarrollada en Python utilizando la biblioteca Pygame.

## Características

- Espacio bidimensional de 1000 x 700 unidades.
- Robot móvil con orientación.
- Tres sensores de distancia:
  - Frontal.
  - Izquierda.
  - Derecha.
- Distancia máxima de detección configurable.
- Cuatro obstáculos generados aleatoriamente.
- Movimiento autónomo.
- Detección de obstáculos.
- Evasión automática.
- Visualización en tiempo real.
- Cálculo de la distancia hasta el obstáculo más cercano.

## Instalación

Se recomienda utilizar un entorno virtual.

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py

