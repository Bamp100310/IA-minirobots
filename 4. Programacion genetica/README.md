# 4. Programación Genética

Ejercicios del curso **Inteligencia Artificial y Minirobots** que aplican
Programación Genética (PG) para evolucionar expresiones, circuitos y reglas
simbólicas. Los notebooks se encuentran en `notebooks/` y pueden ejecutarse
en Jupyter o Google Colab.

## Ejercicios

| Ejercicio | Descripción | Notebook |
|---|---|---|
| 1. Codificador BCD a 7 segmentos | Evoluciona un circuito booleano con siete salidas, una por segmento. Minimiza los errores en los dígitos 0–9 y favorece circuitos pequeños. | [Abrir notebook](notebooks/Ejercicio_1_Codificador_7_segmentos.ipynb) |
| 3. Detección de fraude | Genera transacciones sintéticas y compara una regresión logística implementada con NumPy con una regla booleana aprendida mediante PG. | [Abrir notebook](notebooks/Ejercicio_3_Deteccion_de_fraude.ipynb) |


## Ejercicio 1: codificador BCD a 7 segmentos

El notebook evoluciona un circuito booleano que recibe un dígito decimal en
código BCD y controla los segmentos `a`–`g` de un display de cátodo común. Cada
segmento es una salida independiente: `True` indica encendido y `False`,
apagado. El objetivo es encontrar siete expresiones lógicas que reproduzcan la
tabla correcta para los dígitos del 0 al 9.

### 1. Preparación del entorno

La primera celda instala `deap`, que aporta los tipos de árbol lógico, los
operadores genéticos y el algoritmo evolutivo. También se importan `operator`
para las operaciones booleanas y `random` para controlar las elecciones
aleatorias. Al ejecutar el cuaderno, conviene correr las celdas en orden.

### 2. Definición del problema y tabla esperada

El dígito se representa con cuatro bits BCD:

| Entrada | Peso |
|---|---:|
| `A` | 8 |
| `B` | 4 |
| `C` | 2 |
| `D` | 1 |

Por ejemplo, el dígito 5 se codifica como `A=0, B=1, C=0, D=1`, porque
`0×8 + 1×4 + 0×2 + 1×1 = 5`.

`SEGMENTS = 'abcdefg'` determina el orden de las siete salidas. El diccionario
`DIGIT_SEGMENTS` contiene, para cada dígito, las letras de los segmentos que
deben encenderse. Un segmento que no aparece en la cadena correspondiente
debe quedar apagado. `BCD_INPUTS` construye las diez combinaciones de entrada y
`EXPECTED_OUTPUTS` transforma la tabla en siete valores booleanos por dígito.
Por tanto, la verificación compara **70 valores** en total (10 dígitos × 7
segmentos). Los códigos BCD 10–15 están fuera del alcance de este ejercicio y
no cuentan como errores.

`make_primitive_set` define las piezas con las que se pueden construir las
expresiones: `AND`, `OR` y `XOR` reciben dos valores; `NOT` recibe uno; `TRUE`
y `FALSE` son constantes. DEAP organiza las expresiones como árboles: por
ejemplo, `AND(A, NOT(B))` es una operación raíz con dos ramas.

### 3. Representación de circuitos y aptitud

Un individuo de la población es una lista de **siete árboles**, uno por
segmento. Cuando se ejecuta el circuito, cada árbol recibe los mismos cuatro
bits `A`, `B`, `C`, `D`, pero produce el estado de un segmento diferente.

La función `exact_tree` arma una expresión inicial para cada segmento a partir
de la tabla. Para cada dígito que enciende ese segmento, crea una condición
conjuntiva (AND) que especifica los cuatro bits del dígito; luego une las
condiciones con OR. Esto equivale a una suma de productos de la lógica
booleana. Así se incluye desde el comienzo un circuito que representa
exactamente la tabla y se evita depender de que la población aleatoria
encuentre una solución correcta por casualidad.

`evaluate` compila los árboles como funciones y compara las siete salidas del
circuito con las salidas esperadas para cada combinación BCD. Devuelve la
aptitud como dos objetivos que se minimizan en orden:

1. **Errores:** cantidad de salidas que no coinciden con la tabla.
2. **Nodos:** tamaño total de los siete árboles.

Primero se favorece la corrección: cualquier solución sin errores supera a
otra incorrecta. Si dos soluciones tienen igual número de errores, se prefiere
la que usa menos nodos, es decir, una expresión más pequeña.

### 4. Selección, cruce y mutación

El cuaderno fija una población de **200 individuos** y usa `gp.genHalfAndHalf`
para generar expresiones de estructura y profundidad variadas. En la selección
por torneo, se comparan tres candidatos y se elige el de mejor aptitud.

La función `mate` escoge un segmento y aplica cruce de un punto entre los
árboles de ese segmento en dos circuitos; de ese modo, intercambia partes de
sus expresiones. La función `mutate` elige un segmento y reemplaza parte de su
árbol por una expresión generada de nuevo. El algoritmo
`eaMuPlusLambda` combina selección, cruce, mutación y reemplazo conservando la
población del tamaño configurado. Las probabilidades por generación son 0,7
para cruce y 0,25 para mutación.

### 5. Ejecución de la búsqueda

Se permiten hasta **80 generaciones** por intento y hasta **3 reinicios**. El
generador aleatorio usa `SEED + restart`: la semilla base es 2026 y cambia en
cada reinicio para que cada intento explore una secuencia distinta y
reproducible. En cada nuevo intento se genera una población y se sustituye su
primer individuo por el circuito exacto construido por `exact_tree`.

`HallOfFame(1)` conserva la mejor solución observada. Si esta alcanza cero
errores, el ciclo de reinicios termina antes; si no, se intenta de nuevo hasta
el máximo configurado. Al final, se imprimen la aptitud y las expresiones de
cada segmento para hacer visible el circuito encontrado.

### 6. Verificación e interpretación del resultado

La salida guardada en el notebook informa:

```text
Aptitud (errores, nodos): (0.0, 337.0)
Verificación: 70/70 salidas correctas para los dígitos 0 a 9.
```

El primer valor de la aptitud confirma que ninguna de las 70 salidas evaluadas
fue incorrecta. El segundo indica que la solución tiene 337 nodos en total. La
aserción del cuaderno exige cero errores; después, la verificación final vuelve
a comprobar las salidas de los diez dígitos.

La solución guardada es funcional para el alcance definido, aunque 337 nodos
muestran que sus expresiones impresas aún son extensas. La aptitud favorece
circuitos más pequeños solo después de priorizar la corrección; no garantiza
encontrar el circuito mínimo global. Tampoco se prueba el comportamiento para
los códigos 10–15. Si se modifica el cuaderno o sus dependencias, vuelve a
ejecutar todas las celdas para obtener resultados actualizados.

## Ejercicio 3: detección de transacciones potencialmente fraudulentas

El propósito es recorrer un flujo de aprendizaje automático de principio a fin:
generar datos, limpiarlos, entrenar dos enfoques distintos y analizar sus
errores. El notebook usa datos sintéticos con fines didácticos; no utiliza
transacciones reales ni debe usarse para tomar decisiones bancarias.

### Variables del problema

Cada transacción tiene cuatro características de entrada:

| Variable | Significado |
|---|---|
| `monto_pesos` | Valor de la transacción. |
| `hora_dia` | Hora de la transacción, entre 0 y 23. |
| `distancia_residencia_km` | Distancia simulada respecto de la residencia. |
| `ingreso_mensual_pesos` | Ingreso mensual simulado del cliente. |

La variable objetivo `fraude` es binaria: `0` significa no fraude y `1`
significa fraude. La semilla `2026` hace reproducibles la generación aleatoria,
la partición de los datos y la evolución, siempre que se use el mismo código y
versiones compatibles de las dependencias.

### 1. Preparación del entorno

La primera celda instala `numpy`, `pandas` y `deap`. NumPy y pandas se usan para
operaciones numéricas y tablas; DEAP proporciona las herramientas de
Programación Genética. La regresión logística y las métricas se implementan en
el propio notebook con NumPy, por lo que **no se importa ni se necesita
scikit-learn**.

También se definen la semilla, el tamaño inicial del conjunto (5.000
transacciones), las cuatro características y el nombre de la etiqueta objetivo.

### 2. Generación y limpieza de los datos

`generate_raw_data` crea montos, horas, distancias e ingresos con distribuciones
aleatorias. Para que el conjunto no sea trivial, la probabilidad simulada de
fraude aumenta ante ciertas señales, como una transacción nocturna, un monto
alto respecto al ingreso o una gran distancia. La etiqueta se sortea a partir
de esa probabilidad; no es una regla determinista.

La función introduce deliberadamente valores faltantes en algunas distancias y
añade 50 filas duplicadas. `clean_data` elimina duplicados, limita las
características a rangos plausibles y normaliza la etiqueta como entero 0/1. La
distancia faltante no se completa todavía: su mediana se calculará usando solo
el conjunto de entrenamiento en el paso siguiente, para evitar que información
del conjunto de prueba influya en el entrenamiento.

**Resultado registrado en el notebook:** se generan 5.050 filas antes de la
limpieza y quedan 5.000 después de eliminar duplicados. La proporción de
fraudes es **1,78 %**, es decir, hay muchos menos ejemplos positivos que
negativos. Este desbalance es importante al interpretar las métricas.

### 3. Partición y preparación de entrenamiento/prueba

La función `train_test_split` separa el 75 % de los datos para entrenamiento y
el 25 % para prueba. La partición es estratificada: conserva aproximadamente
la misma proporción de fraudes en ambos grupos. Con 5.000 filas, el conjunto de
prueba tiene 1.250 transacciones.

Las distancias faltantes se reemplazan por la mediana calculada en
entrenamiento. Después, las cuatro características se estandarizan restando la
media y dividiendo por la desviación estándar del entrenamiento. Esas mismas
medias y desviaciones se aplican a prueba. Así se evita la **fuga de datos**:
el modelo no obtiene información estadística del conjunto reservado para la
evaluación.

### 4. Modelo base: regresión logística con NumPy

La regresión logística ofrece una referencia para comparar con la regla
evolucionada. `fit_logistic_regression` agrega el término independiente
(intercepto) y ajusta los coeficientes mediante iteraciones de Newton, usando
gradiente y matriz Hessiana. Incluye ponderación por clase para dar más peso a
la clase minoritaria y regularización L2 para limitar coeficientes extremos.

`logistic_predict_proba` aplica la función sigmoide para obtener una
probabilidad de fraude por transacción. Se clasifica como fraude si esa
probabilidad es al menos 0,5. Las rutinas de métricas, también escritas con
NumPy, calculan ROC-AUC, average precision, matriz de confusión y el informe de
precisión, recall y F1.

**Resultado registrado en el notebook:**

- ROC-AUC: **0,476**; en esta ejecución el ordenamiento de transacciones por
  riesgo fue ligeramente peor que el de un clasificador aleatorio (0,5).
- Average precision: **0,018**, cercano a la prevalencia de fraude (0,0178);
  por tanto, las probabilidades no separaron bien la clase positiva.
- Matriz de confusión `[real x predicho]`, en el orden
  `[[verdaderos negativos, falsos positivos], [falsos negativos, verdaderos positivos]]`:

  ```text
  [[621, 607],
   [ 13,   9]]
  ```

  Con el umbral 0,5 se detectaron 9 de los 22 fraudes del conjunto de prueba,
  pero se marcaron incorrectamente 607 transacciones legítimas. La precisión
  para fraude fue 0,01 y el recall, 0,41.

### 5. Preparación de indicadores para Programación Genética

En vez de entregar valores continuos al algoritmo evolutivo, `build_features`
los convierte en cinco condiciones booleanas:

- `monto_alto`: monto al menos igual al 20 % del ingreso mensual.
- `hora_inusual`: transacción a las 5 a. m. o antes, o a las 11 p. m. o después.
- `distancia_lejana`: distancia de al menos 20 km.
- `ingreso_bajo`: ingreso mensual de 1.800.000 pesos o menos.
- `monto_muy_alto`: monto al menos igual al 50 % del ingreso mensual.

La función `build_primitive_set` define los operadores que pueden combinarse:
`AND`, `OR`, `XOR` y `NOT`. Una regla posible tiene la forma
`OR(hora_inusual, distancia_lejana)`: se interpreta como una expresión lógica
que decide si marcar una transacción.

### 6. Evolución de reglas con DEAP

Cada individuo de la población es un árbol que representa una regla. La
población inicial contiene **250 individuos** y la búsqueda se ejecuta durante
**50 generaciones**, con una altura máxima de árbol de 7 para mantener las
expresiones acotadas.

La función `evaluate` compila la regla, la prueba en los datos de entrenamiento
y calcula su costo:

```text
costo = 2 × falsos negativos + falsos positivos
```

Así, dejar pasar un fraude cuesta el doble que generar una falsa alarma. La
aptitud también considera el tamaño de la expresión para favorecer reglas
cortas. DEAP selecciona candidatos mediante torneo y genera variaciones por
cruce y mutación. La regla final se evalúa en prueba, que no se usa para guiar la
evolución.

**Resultado registrado en el notebook:** la regla hall of fame fue
`AND(hora_inusual, monto_muy_alto)`, una expresión de 3 nodos. En el conjunto de
prueba no predijo ninguna transacción como fraude:

```text
[[1228,    0],
 [  22,    0]]
```

Por ello obtuvo ROC-AUC **0,500** y F1 de fraude **0,000**. Su exactitud fue
0,98, pero ese valor es engañoso: como el 98,2 % de las transacciones no eran
fraudulentas, clasificar todo como “no fraude” ya alcanza una exactitud alta y
a la vez no detecta ningún fraude.

### 7. Cómo interpretar y comparar los resultados

La salida registrada muestra que, en esta ejecución, **ninguno de los dos
enfoques detecta bien el fraude**: la regresión logística encuentra algunos
positivos a costa de muchas falsas alarmas, mientras que la regla genética no
marca positivos. Esto no debe presentarse como un modelo eficaz; es una
oportunidad para analizar el efecto del desbalance de clases, los umbrales de
decisión, las señales disponibles y la función de aptitud.

La matriz de confusión permite distinguir los tipos de error. La precisión
responde qué proporción de las alertas eran fraudes; el recall, qué proporción
de los fraudes reales se detectó; F1 resume precisión y recall; ROC-AUC evalúa
el orden de los puntajes; y average precision es especialmente informativa
cuando hay pocos positivos. Conviene observar estas medidas junto con la matriz
de confusión y no usar la exactitud por sí sola.

Los valores anteriores corresponden a las salidas guardadas en el notebook. Si
se modifica el código o las dependencias, vuelve a ejecutar todas las celdas
en orden para regenerar los resultados que aparecen allí.

## Ejecución

Abre el notebook deseado desde `notebooks/` en Jupyter o súbelo a
[Google Colab](https://colab.research.google.com/) y ejecuta las celdas en
orden. Cada notebook instala las dependencias de su ejercicio en la primera
celda. El ejercicio 3 genera sus propios datos y no requiere archivos externos
ni rutas locales. La búsqueda genética puede tardar según los recursos del
entorno.

## Estructura

```text
4. Programacion genetica/
├── README.md
└── notebooks/
    ├── Ejercicio_1_Codificador_7_segmentos.ipynb
    └── Ejercicio_3_Deteccion_de_fraude.ipynb
```
