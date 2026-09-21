# 4. Programación Genética

## 1. Diseño de un codificador BCD a 7 segmentos

Este ejercicio utiliza **Programación Genética (PG)** para obtener un circuito
combinacional que recibe un dígito decimal codificado en BCD y activa los
segmentos `a` a `g` de un display de 7 segmentos. Se usa la librería
[DEAP](https://deap.readthedocs.io/), que proporciona los árboles de expresión,
los operadores evolutivos y la selección.

La convención es la de un display de **cátodo común**: `1` significa segmento
encendido. El circuito recibe un dígito decimal en código BCD y produce siete
salidas, una por cada segmento:

```text
Entrada BCD:  A B C D       Salida:  a b c d e f g
			  8 4 2 1                segmentos
```

Las entradas tienen los siguientes pesos:

| Entrada | Peso |
|---|---:|
| `A` | 8 |
| `B` | 4 |
| `C` | 2 |
| `D` | 1 |

Se entrenan únicamente los códigos válidos `0000` a `1001` (dígitos 0 a 9).
Los códigos `1010` a `1111` no representan dígitos decimales y se consideran
*don't care*: no participan en la función de aptitud.

### Tabla de verdad

En la tabla, `1` significa que el segmento está encendido y `0` que está
apagado.

| Dígito | A | B | C | D | a | b | c | d | e | f | g |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 0 |
| 1 | 0 | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |
| 2 | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 1 | 1 | 0 | 1 |
| 3 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 |
| 4 | 0 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 1 | 1 |
| 5 | 0 | 1 | 0 | 1 | 1 | 0 | 1 | 1 | 0 | 1 | 1 |
| 6 | 0 | 1 | 1 | 0 | 1 | 0 | 1 | 1 | 1 | 1 | 1 |
| 7 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| 8 | 1 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 9 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 1 |

### Conjunto de terminales

El conjunto de terminales es

```text
T = { A, B, C, D, TRUE, FALSE }
```

`A`, `B`, `C` y `D` son las cuatro entradas del circuito, mientras que `TRUE`
y `FALSE` permiten construir constantes booleanas. Cada individuo contiene siete
árboles, en el orden `a, b, c, d, e, f, g`; cada árbol calcula la salida de un
segmento.

### Conjunto de funciones

Se utiliza el conjunto booleano

```text
F = { AND(x, y), OR(x, y), XOR(x, y), NOT(x) }
```

Todas las funciones reciben y devuelven valores booleanos. La profundidad
inicial se limita para mantener árboles manejables; posteriormente la
mutación puede reemplazar subárboles sin superar la altura máxima.

### Función de aptitud

Para un individuo \(I\), una entrada \(x\) y un segmento \(s\), sea
\(y_{x,s}\) la salida esperada y \(\hat y_{I,x,s}\) la salida del árbol. La
aptitud minimiza primero el número de errores:

```text
E(I) = cantidad de salidas incorrectas
	= suma de los errores para los 10 dígitos y los 7 segmentos
```

Como segundo criterio se minimiza el tamaño total del circuito:

```text
S(I) = cantidad total de nodos de los siete árboles
```

Por tanto, la aptitud implementada es la tupla `(E, S)`. Como ambos valores
se minimizan, el algoritmo busca primero una solución correcta (`E = 0`) y,
entre soluciones correctas, prefiere el circuito con menos nodos.

### Representación del individuo

Cada individuo contiene siete árboles booleanos:

```text
individuo = [árbol_a, árbol_b, árbol_c, árbol_d,
			 árbol_e, árbol_f, árbol_g]
```

El programa utiliza una solución inicial válida construida mediante suma de
productos. A partir de ella, DEAP aplica selección, cruce, mutación y elitismo
para conservar la exactitud y buscar expresiones más pequeñas. Esta decisión
evita que una ejecución falle únicamente por una mala semilla aleatoria.

### Ejecución

Se recomienda crear un entorno virtual para aislar las dependencias del
ejercicio. Desde esta carpeta, ejecute:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación por la política de ejecución, puede
ejecutarse directamente el intérprete del entorno con
`.\.venv\Scripts\python.exe`.

Con el entorno virtual activo, instalar las dependencias y ejecutar:

```powershell
python -m pip install -r requirements.txt
python codificador_7_segmentos.py
```

El programa imprime la aptitud encontrada, las siete expresiones booleanas y
comprueba que los 70 bits de salida de los dígitos 0 a 9 sean correctos.
La semilla aleatoria hace reproducible la ejecución, aunque el resultado
exacto puede variar entre versiones de DEAP.

### Resultado esperado

Una ejecución correcta termina con un resultado similar a:

```text
Aptitud (errores, nodos): (0.0, ...)
Verificación: 70/70 salidas correctas para los dígitos 0 a 9.
```

El número de nodos puede cambiar entre versiones de Python o DEAP, pero la
primera componente debe ser `0.0`.

## Estructura

```text
4. Programacion genetica/
└── 1_Codificador_7_segmentos/
	├── README.md
	├── requirements.txt
	└── codificador_7_segmentos.py
```
