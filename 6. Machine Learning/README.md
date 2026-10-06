# 6. Machine Learning

Ejercicios del curso **Inteligencia Artificial y Minirobots** que aplican conceptos de aprendizaje automático supervisado y evalúan su pertinencia frente a métodos analíticos tradicionales. Los scripts de ejecución se encuentran en `scripts/`.

## Ejercicios

| Ejercicio | Descripción | Script |
| --- | --- | --- |
| 1. Multiplicación de Matrices $2\times2$ vs ML | Contrasta la programación determinista con Machine Learning para calcular operaciones matriciales. Evalúa costo computacional y precisión.

 | `scripts/Ejercicio_1_Matrices.py`<br> |
| 2. Support Vector Machine (SVM) | Clasificación de tumores de mama (Wisconsin) comparando el impacto de hiperplanos lineales vs. no lineales (Kernel RBF).

 | `scripts/Ejercicio_2_SVM.py`<br> |
| 3. K-Nearest Neighbors (KNN) | Implementación de aprendizaje perezoso (*Lazy Learning*) para clasificar cultivares de vino, optimizando el hiperparámetro K.

 | `scripts/Ejercicio_3_KNN.py`<br> |
| 4. Árboles de Decisión (Datos Gov) | Modelo de caja blanca aplicado a un entorno real utilizando datos gubernamentales extraídos mediante API (Socrata).

 | `scripts/Ejercicio_4_Arboles_Decision.py`<br> |

---

## Ejercicio 1: Multiplicación de Matrices $2\times2$ vs ML

El script demuestra por qué el aprendizaje automático no debe sustituir el álgebra lineal básica evaluando una operación matemática determinista.

### 1. Variables del problema

* **Entrada:** 8 elementos numéricos de dos matrices $A$ y $B$ de $2\times2$, con valores enteros aleatorios en el rango $[-20, 20]$.


* **Salida (Rótulos):** 4 elementos continuos correspondientes a la matriz $C = A \times B$.


* **Volumen:** Conjunto de datos sintético de 50.000 instancias para entrenamiento y 10 ejemplos para inferencia.



### 2. Análisis de costo y conclusión

* **Método Analítico:** Garantiza un error de 0 y su costo computacional es $\mathcal{O}(1)$, requiriendo solo 8 multiplicaciones y 4 sumas por definición.


* **Enfoque ML (Regresión Múltiple/Red Densa):** Presenta un error residual estadístico (RMSE $>0$). El entrenamiento consume miles de millones de FLOPS (operaciones de punto flotante) para el cálculo de gradientes y actualización de pesos.


* **Veredicto:** ML aproxima funciones probabilísticas e inserta ruido innecesario en un cálculo exacto.



## Ejercicio 2: Support Vector Machine (SVM)

Clasificación de cáncer utilizando el principio de maximización del margen óptimo.

### 1. Preparación de datos y métricas

* **Dataset:** *Breast Cancer Wisconsin*, compuesto por 30 características geométricas celulares.


* **Objetivo:** Clasificar el tumor como benigno o maligno buscando maximizar la métrica de Sensibilidad. El enfoque principal es reducir la tasa de falsos negativos críticos en diagnósticos médicos.



### 2. Estrategia de Kernels

* Se evalúa un Kernel Lineal frente a un Kernel RBF (Radial Basis Function).


* El objetivo del *Kernel Trick* es mapear características a un espacio de mayor dimensión ($\mathbb{R}^{n}\rightarrow\mathbb{R}^{m}$) para trazar fronteras de decisión curvas donde los datos no son linealmente separables.



## Ejercicio 3: K-Nearest Neighbors (KNN)

Implementación orientada a *Lazy Learning*, donde todo el procesamiento pesado ocurre durante la fase de inferencia calculando similitudes geométricas.

### 1. Preparación del modelo

* **Dataset:** *Wine Dataset*, con 13 propiedades fisicoquímicas para predecir 3 tipos de cultivares.


* **Pre-procesamiento crítico:** Dado que las métricas de distancia (Euclidiana, Manhattan) son sensibles a la magnitud, es obligatorio estandarizar los datos (ej. utilizando `StandardScaler`).



### 2. Balance Sesgo-Varianza

* El modelo decide la clase calculando la moda de los $K$ vecinos más cercanos.


* Se utiliza validación cruzada (curva de validación) para hallar el hiperparámetro $K$ óptimo. Un valor de $K=1$ sobreajusta capturando ruido, mientras que un $K$ muy grande generaliza en exceso (subajuste).



## Ejercicio 4: Árboles de Decisión (Datos Gubernamentales)

Construcción de un modelo de "caja blanca" interpretable utilizando datos abiertos del gobierno colombiano.

### 1. Extracción y limpieza

* **Fuente:** Histórico de accidentes de tránsito o hurto extraído del portal Datos Abiertos Colombia mediante la API de Socrata.


* **Características:** Comuna, rango de horas, día de la semana y tipo de vía.


* **Procesamiento:** Las variables categóricas se transforman mediante One-Hot Encoding.



### 2. Entrenamiento y reglas lógicas

* El modelo divide recursivamente los nodos maximizando la pureza (usando Índice Gini o Entropía).


* Para evitar el sobreajuste, se implementa una técnica de pre-poda limitando la profundidad del árbol (`max_depth=4`).


* Esta restricción de profundidad permite graficar el árbol resultante y extraer reglas lógicas claras en formato "if-then-else" (ej. condiciones específicas que aumentan la probabilidad de heridos en un incidente).



---

## Ejecución

Los modelos están implementados en Python. Para ejecutarlos localmente o en Google Colab:

1. Instala las dependencias listadas en `requirements.txt` (`scikit-learn`, `pandas`, `numpy`, etc.).


2. Ejecuta los scripts ubicados en la carpeta `scripts/`.


3. El ejercicio 4 requiere conexión a internet para consumir la API pública.



## Estructura

```text
6. Machine Learning/
├── README.md
├── requirements.txt
├── Informe_Ejercicios.pdf
└── scripts/
    ├── Ejercicio_1_Matrices.py
    ├── Ejercicio_2_SVM.py
    ├── Ejercicio_3_KNN.py
    └── Ejercicio_4_Arboles_Decision.py

```
