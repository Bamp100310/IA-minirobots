# 5. Redes Neuronales Artificiales

Desarrollo de los cuatro ejercicios propuestos en la sección 5.9 del capítulo
*Introducción a las Redes Neuronales Artificiales* (José J. Martínez P.), curso de Inteligencia Artificial y Minirobots.

Los programas se entregan como notebooks de Jupyter, ejecutados y con sus resultados incluidos. El documento
`Documento_Redes_Neuronales.pdf` (y su versión editable `.docx`) describe las partes y los resultados de cada
programa, el uso de herramientas de IA generativa, y contiene los enlaces para abrir cada notebook en Google Colab.

## Ejercicios desarrollados

| Ejercicio | Notebook | Herramienta | Verificación | Resultado principal |
|---|---|---|---|---|
| 1. Redes con dos capas ocultas para NAND y XOR | [Ejercicio 1](notebooks/Ejercicio_1_Compuertas_NAND_XOR.ipynb) | NumPy (programa Clase_NNA3 generalizado) | Reproducción exacta del Ejemplo 1 del capítulo y prueba de gradiente numérico | Ambas compuertas aprendidas; 79 de 80 entrenamientos exitosos con 20 semillas |
| 2. Clasificación de prendas con Fashion MNIST | [Ejercicio 2](notebooks/Ejercicio_2_Fashion_MNIST.ipynb) | TensorFlow / Keras | Propagación repetida a mano con los pesos extraídos: 10 000 predicciones idénticas | 88.3 % de exactitud en prueba |
| 3. Modelo con un dataset de Kaggle y ejemplos de internet | [Ejercicio 3](notebooks/Ejercicio_3_Kaggle_Pokemon_Legendarios.ipynb) | kagglehub, Keras, scikit-learn | Validación cruzada contra una regla base y 23 ejemplos nuevos tomados de internet | Auditoría de datos (formas alternativas y rótulos), análisis de lo que aprendió la red |
| 4. Punto libre: convolución, pooling y CNN | [Ejercicio 4](notebooks/Ejercicio_4_Convolucion_Pooling_CNN.ipynb) | NumPy, SciPy, Keras | Ejemplos numéricos de la sección 5.8 y figura 5.24 reproducidos; `Conv2D` igual a la convolución hecha a mano | CNN con 91.1 % frente a 88.0 % de la red densa |

## Observaciones sobre el material del capítulo

El Ejercicio 1 reproduce primero el procedimiento de la sección 5.3, donde el capítulo construye las
compuertas escogiendo los pesos a mano (AND, OR y NOT de una neurona; la NAND de dos capas de la figura
5.10 con sus once columnas; la NOR; la red de dos salidas de la figura 5.11; y la XOR armada con esas
mismas piezas), y después entrena las dos redes que pide el enunciado.

Al reproducir el programa del Ejemplo 1 (sección 5.6) se encontró que la función `dSig` calcula
`sig(s)*sig(s)` en lugar de `sig(s)*(1 - sig(s))`, que es la derivada que el propio capítulo establece en
las secciones 5.2.2 y 5.5. Con la derivada corregida el Ejemplo 1 reduce su error final 110 veces, y la
diferencia es decisiva en la XOR: con la versión del programa no se aprende en ninguna de 40 corridas.

## Estructura

```
5. Redes neuronales/
├── README.md
├── requirements.txt
├── Documento_Redes_Neuronales.pdf
├── Documento_Redes_Neuronales.docx
├── notebooks/
│   ├── Ejercicio_1_Compuertas_NAND_XOR.ipynb
│   ├── Ejercicio_2_Fashion_MNIST.ipynb
│   ├── Ejercicio_3_Kaggle_Pokemon_Legendarios.ipynb
│   └── Ejercicio_4_Convolucion_Pooling_CNN.ipynb
└── img/                      figuras generadas por los notebooks
```

## Ejecución

### Google COLAB

Ingresar a colab.research.google.com y abrir el notebook mediante *Archivo → Abrir notebook → GitHub*,
indicando la dirección del repositorio, o usar directamente los enlaces del documento. Ejecutar con
*Entorno de ejecución → Ejecutar todas*. TensorFlow, scikit-learn, kagglehub y las demás librerías vienen
preinstaladas. Para los ejercicios 2 y 4 se recomienda activar la GPU (*Entorno de ejecución → Cambiar tipo
de entorno*), aunque también funcionan en CPU.

### Jupyter local

```bash
pip install -r requirements.txt
jupyter notebook notebooks/
```

### Datos

- Ejercicios 2 y 4: Fashion MNIST se descarga automáticamente con `tf.keras.datasets.fashion_mnist.load_data()`.
- Ejercicio 3: el conjunto `abcsds/pokemon` se descarga de Kaggle con `kagglehub`. Si la descarga no es posible,
  el notebook usa una copia idéntica alojada en GitHub e indica en su salida cuál fuente utilizó.
- Ejercicio 4: la imagen *ascent* se obtiene con `scipy.datasets` (requiere `pooch`).


## Referencias

- Martínez, J. J. (2026). *Introducción a las redes neuronales artificiales*, capítulo 5. Material del curso.
- Moroney, L. (2020). *AI and Machine Learning for Coders*. O'Reilly.
- Ng, A. *Machine Learning*. Coursera.
- He, K., Zhang, X., Ren, S. y Sun, J. (2016). Deep Residual Learning for Image Recognition. *CVPR*.
- Xiao, H., Rasul, K. y Vollgraf, R. (2017). Fashion-MNIST: a Novel Image Dataset for Benchmarking Machine
  Learning Algorithms. arXiv:1708.07747.
- Minsky, M. y Papert, S. (1969). *Perceptrons*. MIT Press.
- Rumelhart, D., Hinton, G. y Williams, R. (1986). Learning representations by back-propagating errors.
  *Nature*, 323, 533-536.
- Barradas, A. (abcsds). *Pokemon with stats* [conjunto de datos]. Kaggle.
