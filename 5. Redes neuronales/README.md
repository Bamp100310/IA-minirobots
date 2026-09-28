# 5. Redes Neuronales Artificiales

Desarrollo de los cinco ejercicios propuestos en la sección 5.9 del capítulo
*Introducción a las Redes Neuronales Artificiales* (José J. Martínez P.), curso de Inteligencia Artificial y Minirobots.

Los programas se entregan como notebooks de Jupyter, ejecutados y con sus resultados incluidos. El documento [`Documento_Redes_Neuronales.pdf`](Documento_Redes_Neuronales.pdf) describe las partes y los resultados de cada programa, el uso de herramientas de IA generativa, y contiene los enlaces para abrir cada notebook en Google Colab.

## Ejercicios desarrollados

| Ejercicio | Notebook | Herramienta | Verificación | Resultado principal |
|---|---|---|---|---|
| 1. Modelo de un experimento con una red de **dos capas ocultas** | [Ejercicio 1](notebooks/Ejercicio_1_Experimento_Red_Dos_Capas_Ocultas.ipynb) | NumPy (retropropagación de la sección 5.5 para una red 2‑4‑4‑1) | Gradiente numérico; entrenamiento idéntico en Keras con los mismos pesos iniciales; comparación con el modelo físico de Michaelis-Menten | Error de predicción de 11.1 cuentas/min², igual al del modelo físico y cercano al error experimental (10.0); predicciones para concentraciones no medidas |
| 2. Fashion MNIST con una red de **dos capas ocultas** | [Ejercicio 2](notebooks/Ejercicio_2_Fashion_MNIST_Dos_Capas_Ocultas.ipynb) | TensorFlow / Keras | Propagación a mano por las dos capas ocultas: 10 000 predicciones idénticas; comparación con 0 y 1 capa oculta con tres semillas | **88.7 %** de exactitud y 88.7 % de precisión promedio en prueba |
| 3. Fashion MNIST: funciones e instrucciones explicadas | [Ejercicio 3](notebooks/Ejercicio_3_Fashion_MNIST_Funciones_Instrucciones.ipynb) | TensorFlow / Keras | Cada función principal repetida con NumPy (`Flatten`, `Dense`, pérdida, un paso de gradiente con `GradientTape`, `predict`) | Modelo del capítulo con 87.4 % de exactitud en prueba |
| 4. Modelo con un dataset de Kaggle y ejemplos de internet | [Ejercicio 4](notebooks/Ejercicio_4_Kaggle_Pokemon_Legendarios.ipynb) | kagglehub, Keras (red 6‑16‑8‑1 con dos capas ocultas), scikit-learn | Validación cruzada contra una regla base y 23 ejemplos nuevos tomados de internet | Auditoría de datos (formas alternativas y rótulos) y análisis de lo que aprendió la red |
| 5. Punto libre: convolución, pooling y CNN | [Ejercicio 5](notebooks/Ejercicio_5_Convolucion_Pooling_CNN.ipynb) | NumPy, SciPy, Keras | Ejemplos numéricos de la sección 5.8 y figura 5.24 reproducidos; `Conv2D` igual a la convolución hecha a mano | CNN con 91.1 % frente a 88.0 % de la red densa de dos capas ocultas |

## Las redes de dos capas ocultas

| Ejercicio | Arquitectura | Capa oculta 1 | Capa oculta 2 | Salida |
|---|---|---|---|---|
| 1 | 2‑4‑4‑1 | 4 neuronas, sigmoide | 4 neuronas, sigmoide | 1 neurona, lineal (regresión) |
| 2 | 784‑256‑128‑10 | 256 neuronas, ReLU (+ Dropout) | 128 neuronas, ReLU (+ Dropout) | 10 neuronas, softmax |
| 4 | 6‑16‑8‑1 | 16 neuronas, ReLU | 8 neuronas, ReLU | 1 neurona, sigmoide |

En los tres casos el número de capas ocultas se verifica en el notebook (capas con pesos del modelo) y la propagación se repite capa por capa.

## Estructura

```
5. Redes neuronales/
├── README.md
├── requirements.txt
├── Documento_Redes_Neuronales.pdf
├── notebooks/
│   ├── Ejercicio_1_Experimento_Red_Dos_Capas_Ocultas.ipynb
│   ├── Ejercicio_2_Fashion_MNIST_Dos_Capas_Ocultas.ipynb
│   ├── Ejercicio_3_Fashion_MNIST_Funciones_Instrucciones.ipynb
│   ├── Ejercicio_4_Kaggle_Pokemon_Legendarios.ipynb
│   └── Ejercicio_5_Convolucion_Pooling_CNN.ipynb
└── img/                      figuras generadas por los notebooks
```

## Ejecución

### Google COLAB

Ingresar a colab.research.google.com y abrir el notebook mediante *Archivo → Abrir notebook → GitHub*,
indicando la dirección del repositorio, o usar directamente los enlaces del documento. Ejecutar con
*Entorno de ejecución → Ejecutar todas*. TensorFlow, scikit-learn, kagglehub y las demás librerías vienen
preinstaladas. Para los ejercicios 2, 3 y 5 se recomienda activar la GPU (*Entorno de ejecución → Cambiar tipo
de entorno*).

### Jupyter local

```bash
pip install -r requirements.txt
jupyter notebook notebooks/
```

Tiempos aproximados en CPU: Ejercicio 1, 2 min; Ejercicio 2, 20 min (comparación de arquitecturas con tres semillas); Ejercicio 3, 4 min; Ejercicio 4, 5 min; Ejercicio 5, 5 min.

### Datos

- Ejercicio 1: la tabla del experimento de Treloar (1974), conjunto `Puromycin` de R, está escrita dentro del notebook; no requiere descarga.
- Ejercicios 2, 3 y 5: Fashion MNIST se descarga automáticamente con `tf.keras.datasets.fashion_mnist.load_data()`.
- Ejercicio 4: el conjunto `abcsds/pokemon` se descarga de Kaggle con `kagglehub`. Si la descarga no es posible,
  el notebook usa una copia idéntica alojada en GitHub e indica en su salida cuál fuente utilizó.
- Ejercicio 5: la imagen *ascent* se obtiene con `scipy.datasets` (requiere `pooch`).

## Referencias

- Martínez, J. J. (2026). *Introducción a las redes neuronales artificiales*, capítulo 5. Material del curso.
- Moroney, L. (2020). *AI and Machine Learning for Coders*. O'Reilly.
- Ng, A. *Machine Learning*. Coursera.
- He, K., Zhang, X., Ren, S. y Sun, J. (2016). Deep Residual Learning for Image Recognition. *CVPR*.
- Treloar, M. A. (1974). *Effects of Puromycin on Galactosyltransferase in Golgi Membranes*. Tesis de maestría, Universidad de Toronto.
- Bates, D. M. y Watts, D. G. (1988). *Nonlinear Regression Analysis and Its Applications*. Wiley.
- Xiao, H., Rasul, K. y Vollgraf, R. (2017). Fashion-MNIST: a Novel Image Dataset for Benchmarking Machine
  Learning Algorithms. arXiv:1708.07747.
- Rumelhart, D., Hinton, G. y Williams, R. (1986). Learning representations by back-propagating errors.
  *Nature*, 323, 533-536.
- Barradas, A. (abcsds). *Pokemon with stats* [conjunto de datos]. Kaggle.
