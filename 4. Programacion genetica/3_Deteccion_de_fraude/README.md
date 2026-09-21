# 3. Detección de fraudes

## Objetivo

Este ejercicio genera un archivo sintético de transacciones y entrena un
modelo que estima si una operación puede ser fraudulenta. Las variables
solicitadas son:

- `monto_pesos`: valor de la transacción.
- `hora_dia`: hora en formato de 0 a 23.
- `distancia_residencia_km`: distancia entre la transacción y la residencia.
- `ingreso_mensual_pesos`: ingreso mensual del cliente.
- `fraude`: etiqueta, donde `1` significa fraude y `0` significa no fraude.

La semilla `2026` hace que los datos y la evaluación sean reproducibles.

El ejercicio tiene dos etapas:

1. Se generan y revisan datos sintéticos.
2. Se entrena un modelo base y una solución mediante Programación Genética.

La regresión logística sirve como referencia numérica. La PG produce una
regla booleana mas facil de leer, por ejemplo: marcar como fraude una
transaccion nocturna cuyo monto sea alto respecto al ingreso mensual.

## Revisión y mejora de los datos

Primero se genera `data/transacciones_raw.csv`, que simula un archivo real con
algunos problemas habituales:

- Se agregan aproximadamente 1 % de filas duplicadas.
- Se agregan aproximadamente 1 % de distancias faltantes.
- Los montos y los ingresos siguen distribuciones sesgadas, más parecidas a
  datos financieros reales que una distribucion uniforme.
- La hora de la transacción tiene mayor frecuencia durante el día.
- La probabilidad de fraude aumenta cuando coinciden una hora inusual, una
  distancia grande y un monto alto respecto del ingreso.

El programa revisa el archivo y genera `data/transacciones_limpias.csv`:

- Elimina duplicados.
- Completa distancias faltantes con la mediana.
- Restringe las variables a rangos plausibles.
- Verifica que la etiqueta de fraude sea binaria.

Estas reglas producen datos didácticos, no representan datos bancarios reales.

### Por qué los cambios hacen los datos más realistas

Un archivo completamente aleatorio no representaría bien el problema: todas
las horas tendrían la misma frecuencia, los montos no dependerían del ingreso
y no existirían errores de captura. En esta implementación:

- Los ingresos y los montos siguen distribuciones sesgadas, porque normalmente
  hay muchas transacciones pequeñas y pocas muy grandes.
- La hora se concentra durante el día y las operaciones nocturnas son menos
  frecuentes.
- El monto se compara con el ingreso mensual, en lugar de usar solo un umbral
  fijo. Una compra de 500.000 pesos no representa el mismo riesgo para todos
  los clientes.
- La distancia, el horario y la relación monto/ingreso influyen en la
  probabilidad de fraude, pero se agrega aleatoriedad para evitar una regla
  perfecta y artificial.
- Se agregan duplicados y valores faltantes para simular un archivo original
  que requiere revisión.

## Modelo

Se utiliza una **regresión logística** implementada con `scikit-learn` como
modelo base.
Antes del modelo, las cuatro variables numéricas se estandarizan. Se utiliza
`class_weight="balanced"` porque en detección de fraude normalmente hay menos
fraudes que transacciones legítimas.

El modelo devuelve una probabilidad. En este ejemplo se marca como fraude si
la probabilidad es mayor o igual que `0.5`. En un sistema real este umbral se
ajustaría según el costo de bloquear una compra legítima frente al costo de
permitir un fraude.

Se reportan:

- **ROC-AUC:** capacidad de ordenar transacciones riesgosas por encima de las
  normales.
- **Average precision:** calidad de las predicciones positivas cuando la clase
  fraude es minoritaria.
- **Precisión, recall y F1:** comportamiento de la clase fraude.
- **Matriz de confusión:** falsos positivos y falsos negativos.

### Cómo leer la matriz de confusión

La matriz se imprime en el orden `[real x predicho]`:

```text
        Predicho
        No fraude  Fraude
Real No fraude    TN       FP
  Fraude       FN       TP
```

`TN` son transacciones normales clasificadas correctamente y `TP` son fraudes
detectados. `FP` representa una alerta sobre una compra legítima, mientras
que `FN` es un fraude que el modelo no detectó. En este problema los `FN`
suelen ser más costosos, por eso se debe observar especialmente el `recall`
de la clase `Fraude`.

## Versión con Programación Genética

También se puede resolver el ejercicio mediante PG. El archivo
`deteccion_fraude_pg.py` usa **DEAP** para evolucionar una regla booleana de
clasificacion.

### Terminales

Las terminales no son los valores numéricos sin procesar, sino indicadores
interpretables derivados de las cuatro variables del enunciado:

```text
monto_alto       = monto / ingreso >= 0.20
hora_inusual     = hora <= 5 o hora >= 23
distancia_lejana = distancia >= 20 km
ingreso_bajo     = ingreso <= 1.800.000 pesos
monto_muy_alto   = monto / ingreso >= 0.50
```

Estas variables convierten los datos numéricos en condiciones booleanas. Por
ejemplo, si una transacción tiene un monto de 900.000 pesos y el ingreso
mensual es de 2.000.000, entonces `monto_alto` es verdadero porque
`900.000 / 2.000.000 = 0.45`.

### Funciones

El conjunto de funciones es:

```text
F = { AND(x, y), OR(x, y), XOR(x, y), NOT(x) }
```

Cada individuo es un árbol booleano. Por ejemplo, una regla posible es:

```text
OR(AND(monto_muy_alto, hora_inusual), distancia_lejana)
```

La regla anterior marca una operación como fraude cuando se cumple al menos
una de estas condiciones: el monto es muy alto y la operación ocurre en una
hora inusual, o la transacción está muy lejos de la residencia. Su ventaja es
que puede presentarse directamente como una politica de alerta.

### Aptitud

La aptitud penaliza más un fraude no detectado que una alerta incorrecta:

```text
error = 2 * falsos_negativos + falsos_positivos
aptitud = (error, numero_de_nodos)
```

El segundo componente favorece reglas cortas e interpretables. Para ejecutar
esta versión, primero genere el archivo limpio y luego ejecute:

```powershell
python deteccion_fraude.py
python deteccion_fraude_pg.py
```

### Qué hace cada programa

`deteccion_fraude.py`:

- Genera `transacciones_raw.csv`.
- Elimina duplicados y corrige datos faltantes o fuera de rango.
- Guarda `transacciones_limpias.csv`.
- Entrena la regresión logística.
- Imprime métricas y dos ejemplos con probabilidad de fraude.

`deteccion_fraude_pg.py`:

- Lee `transacciones_limpias.csv`.
- Construye los cinco indicadores booleanos usados como terminales.
- Genera una población de reglas.
- Aplica selección, cruce y mutación con DEAP.
- Evalúa las reglas sobre los datos de entrenamiento.
- Imprime la mejor regla encontrada y sus métricas sobre el conjunto de prueba.

La división entre entrenamiento y prueba evita evaluar el modelo solamente
con los ejemplos que ya utilizó para aprender. Aun así, como los datos son
sintéticos y fueron creados con reglas conocidas, los resultados no deben
interpretarse como evidencia de rendimiento bancario real.

## Ejecución

Desde esta carpeta, se recomienda crear un entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python deteccion_fraude.py
```

Si PowerShell no permite activar el entorno, ejecute directamente:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe deteccion_fraude.py
```

## Estructura

```text
4. Programacion genetica/
└── 3_Deteccion_de_fraude/
    ├── README.md
    ├── requirements.txt
    ├── deteccion_fraude.py
    ├── deteccion_fraude_pg.py
    └── data/
        ├── transacciones_raw.csv
        └── transacciones_limpias.csv
```

Los archivos dentro de `data/` se crean al ejecutar el programa y no es
necesario escribirlos manualmente.

## Interpretación

El modelo no demuestra que una transacción sea fraudulenta: estima un riesgo a
partir de cuatro variables sintéticas. Para una aplicación real se requerirían
más variables, datos históricos validados, tratamiento del desbalance, una
separación temporal entre entrenamiento y prueba y una revisión humana de los
casos marcados.

## Conclusiones esperadas

El resultado más importante no es obtener una exactitud perfecta, sino mostrar
el proceso completo: crear datos, revisar su calidad, entrenar un modelo,
medir sus errores y analizar las alertas. La regresión logística normalmente
ofrece una probabilidad continua, mientras que la PG entrega una expresión
booleana. Por ello, ambos modelos pueden tener métricas parecidas, pero la
regla de PG suele ser más sencilla de explicar a una persona encargada de
revisar transacciones.
