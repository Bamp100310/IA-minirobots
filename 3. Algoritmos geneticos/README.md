# 3. Algoritmos Genéticos

Desarrollo de tres de los seis ejercicios propuestos en la sección 3.10 del capítulo
*Algoritmos Genéticos* (José J. Martínez P.), curso de Inteligencia Artificial.

Los tres programas se entregan como notebooks de Jupyter, ejecutados y con sus resultados
incluidos. El archivo `Documento_Algoritmos_Geneticos.pdf` describe las partes y los resultados
de cada programa y cuenta con hipervinculos para ver y ejecutarlo en Google Colab.

## Ejercicios desarrollados

| Ejercicio | Notebook | Tipo de gen | Verificación | Resultado |
|---|---|---|---|---|
| 1. Maximizar `f(x) = x·sen(10πx)+1` en [0,1] | [Ejercicio 1](notebooks/Ejercicio_1_Maximizar_funcion.ipynb) | Binario, 22 bits | Búsqueda exhaustiva sobre 2 000 001 puntos y refinamiento numérico | Óptimo global en 30 de 30 corridas, error de 2.1×10⁻⁷ |
| 3. Despacho óptimo de energía eléctrica | [Ejercicio 3](notebooks/Ejercicio_3_Despacho_de_energia.ipynb) | Real, 16 y 20 genes | Programación lineal y enumeración de 784 000 despachos enteros | Óptimo exacto en 10 de 10 corridas |
| 6. Dieta de costo mínimo (multi-objetivo) | [Ejercicio 6](notebooks/Ejercicio_6_Dieta_multiobjetivo.ipynb) | Entero, 10 genes | Frente de Pareto exacto por enumeración de 9 765 625 dietas | 98.4 % del frente exacto recuperado |

La selección de estos tres ejercicios responde a que cubren tres tipos distintos de codificación
del cromosoma y tres secciones diferentes del capítulo (el algoritmo genético simple, el
tratamiento de restricciones y los algoritmos multi-objetivo), y a que en los tres casos existe
una solución exacta calculable por otro método, lo que permite verificar la respuesta obtenida.

## Estructura

```
3. Algoritmos geneticos/
├── README.md
├── requirements.txt
├── Documento_Algoritmos_Geneticos.pdf
├── notebooks/
│   ├── Ejercicio_1_Maximizar_funcion.ipynb
│   ├── Ejercicio_3_Despacho_de_energia.ipynb
│   └── Ejercicio_6_Dieta_multiobjetivo.ipynb
└── img/
```

## Ejecución

### Google COLAB

Ingresar a colab.research.google.com y abrir el notebook mediante *Archivo → Abrir notebook →
GitHub*, indicando la dirección del repositorio, o subiendo el archivo directamente. Ejecutar
con *Entorno de ejecución → Ejecutar todas*. No se requiere instalar nada: NumPy, SciPy, pandas
y Matplotlib vienen preinstalados

Otra forma es ingresando mediante los hipervinculos del documento `Documento_Algoritmos_Geneticos.pdf`.

### Jupyter local

```bash
pip install -r requirements.txt
jupyter notebook notebooks/
```

Los tres notebooks utilizan semillas aleatorias fijas (`numpy.random.default_rng`), de manera que
los resultados son reproducibles: al volver a ejecutarlos se obtienen exactamente las mismas
cifras que aparecen en el documento.

## Referencias

- Martínez, J. J. (2026). *Algoritmos genéticos*, capítulo 3. Material del curso.
- Holland, J. (1995). *Adaptation in Natural and Artificial Systems* (2.ª ed.). MIT Press.
- Goldberg, D. (1989). *Genetic Algorithms in Search, Optimization and Machine Learning*.
  Addison-Wesley.
- Deb, K., Pratap, A., Agarwal, S. y Meyarivan, T. (2002). A fast and elitist multiobjective
  genetic algorithm: NSGA-II. *IEEE Transactions on Evolutionary Computation*, 6(2), 182-197.
- Mitchell, M. (1999). *An Introduction to Genetic Algorithms*. MIT Press.
