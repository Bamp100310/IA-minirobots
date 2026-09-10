# Modelo de difusión de una enfermedad mediante Autómatas Celulares Probabilísticos

## Descripción

Se implementa un modelo de difusión de una enfermedad utilizando un **Autómata Celular Probabilístico (ACP)**.

La población se representa mediante una cuadrícula bidimensional, donde cada celda representa una persona. Cada persona puede encontrarse en uno de tres estados:

* **S - Susceptible:** persona que no tiene la enfermedad y puede infectarse.
* **I - Infectado:** persona que tiene la enfermedad y puede contagiar a sus vecinos.
* **R - Recuperado:** persona que tuvo la enfermedad y se recuperó.

La simulación permite observar cómo una enfermedad puede propagarse espacialmente a través de una población durante diferentes pasos de tiempo.

---

## Objetivo

El objetivo es estudiar cómo las probabilidades de contagio y recuperación afectan la difusión de una enfermedad mediante un modelo basado en Autómatas Celulares.

El modelo permite visualizar:

1. La propagación de la enfermedad.
2. La cantidad de personas susceptibles.
3. La cantidad de personas infectadas.
4. La cantidad de personas recuperadas.
5. La evolución de estos estados a través del tiempo.

---

## Modelo utilizado

El espacio está representado por una cuadrícula de:

```text
50 × 50
```

Por lo tanto, se simulan:

```text
2500 personas
```

Cada celda tiene uno de los siguientes estados:

```text
0 = Susceptible
1 = Infectado
2 = Recuperado
```

---

## Vecindad

Para determinar si una persona puede contagiarse se utiliza una **vecindad de Moore**.

Esto significa que una persona puede interactuar con las ocho celdas que la rodean:

```text
┌───┬───┬───┐
│   │   │   │
├───┼───┼───┤
│   │ P │   │
├───┼───┼───┤
│   │   │   │
└───┴───┴───┘
```

La celda central representa a la persona actual y las ocho celdas restantes representan sus vecinos.

---

## Reglas de transición

### 1. Susceptible → Infectado

Una persona susceptible puede infectarse si tiene uno o más vecinos infectados.

La probabilidad de infección se calcula mediante:

```text
P(infección) = 1 - (1 - β)^n
```

Donde:

* `β` representa la probabilidad de contagio por contacto.
* `n` representa la cantidad de vecinos infectados.

En el programa:

```python
PROB_CONTAGIO = 0.25
```

Esto significa que cada contacto con una persona infectada tiene una probabilidad base del 25 % de producir contagio.

Por ejemplo, si una persona tiene tres vecinos infectados:

```text
P = 1 - (1 - 0.25)^3
P ≈ 0.578
```

Por lo tanto, tendría aproximadamente un 57.8 % de probabilidad de infectarse durante ese paso.

---

### 2. Infectado → Recuperado

Una persona infectada tiene una determinada probabilidad de recuperarse en cada paso:

```python
PROB_RECUPERACION = 0.05
```

Por lo tanto, existe un 5 % de probabilidad de recuperación durante cada paso de tiempo.

---

### 3. Recuperado → Recuperado

Una persona recuperada permanece en ese estado durante el resto de la simulación.

---

## Parámetros principales

Los principales parámetros pueden modificarse directamente en `epidemia.py`:

```python
TAMANO_GRID = 50

PROB_CONTAGIO = 0.25

PROB_RECUPERACION = 0.05

INFECTADOS_INICIALES = 5

PASOS = 200
```

### Tamaño de la población

```python
TAMANO_GRID = 50
```

Representa una cuadrícula de 50 × 50 personas.

### Probabilidad de contagio

```python
PROB_CONTAGIO = 0.25
```

Controla la probabilidad de contagio por contacto.

### Probabilidad de recuperación

```python
PROB_RECUPERACION = 0.05
```

Controla la probabilidad de que una persona infectada se recupere durante un paso.

### Infectados iniciales

```python
INFECTADOS_INICIALES = 5
```

Indica cuántas personas comienzan infectadas.

### Número de pasos

```python
PASOS = 200
```

Define cuánto tiempo se ejecutará la simulación.

---

## Instalación

Se recomienda utilizar Python 3.

Primero se deben instalar las dependencias:

```bash
pip install -r requirements.txt
```

También se pueden instalar directamente:

```bash
pip install numpy matplotlib
```

---

## Ejecución

Para ejecutar el programa:

```bash
python epidemia.py
```

En algunos sistemas puede ser necesario utilizar:

```bash
python3 epidemia.py
```

Al ejecutar el programa aparecerá una ventana con dos visualizaciones:

1. La cuadrícula que representa la población.
2. Una gráfica con la evolución de susceptibles, infectados y recuperados.

---

## Visualización

Durante la simulación se puede observar cómo los individuos infectados transmiten la enfermedad a las personas susceptibles cercanas.

Al mismo tiempo, algunas personas infectadas pasan al estado recuperado.

La simulación utiliza valores aleatorios para determinar si ocurre cada transición, por lo que diferentes ejecuciones pueden producir resultados diferentes.

---

## Tecnologías utilizadas

* Python
* NumPy
* Matplotlib
* Autómatas Celulares Probabilísticos
* Modelo epidemiológico SIR

---

## Estructura del proyecto

```text
modelo-epidemia-ac/
│
├── epidemia.py
├── README.md
└── requirements.txt
```

---

## Conceptos de Inteligencia Artificial utilizados

Esta simulación permite estudiar los siguientes conceptos:

* Autómatas celulares.
* Sistemas dinámicos.
* Modelos probabilísticos.
* Simulación computacional.
* Estados y transiciones.
* Vecindades.
* Procesos estocásticos.
* Difusión espacial.
* Modelamiento de sistemas.

---

## Limitaciones del modelo

Es una simulación académica y no pretende representar exactamente una enfermedad real.

El modelo supone que:

* Todas las personas tienen el mismo comportamiento.
* Todas las personas tienen la misma probabilidad de contagio.
* Las personas no se desplazan entre celdas.
* Los recuperados no vuelven a infectarse.
* No se consideran vacunación, aislamiento ni mortalidad.
* La población permanece constante.

Estas simplificaciones permiten estudiar de manera sencilla el comportamiento de un Autómata Celular Probabilístico.
