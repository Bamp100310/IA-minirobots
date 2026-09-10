# Análisis de servicios mediante diagramas de Voronoi
**Lugar de estudio:** Cabecera municipal de Santa Rosa del Sur, Bolívar, Colombia.

## 1. Objetivo

Analizar la distribución espacial de tres tipos de servicios dentro de la **cabecera municipal de Santa Rosa del Sur** mediante diagramas de Voronoi:

* Droguerías/farmacias.
* Centros de atención de salud.
* Instituciones educativas.

El objetivo es estudiar la **proximidad espacial** entre los servicios y detectar sectores que, dentro del área analizada, presentan mayor distancia geométrica al establecimiento más cercano.

> **Alcance:** este ejercicio se limita a establecimientos ubicados en la cabecera municipal. No se incluyen veredas, corregimientos ni establecimientos rurales.

---

## 2. Estructura

```text
santa-rosa-voronoi/

├── data/
│   └── services.csv
│
├── figures/
│   ├── voronoi_farmacias.png
│   ├── voronoi_salud.png
│   ├── voronoi_colegios.png
│   └── distribucion_conjunta.png
│
├── scripts/
│   └── voronoi_services.py
│
├── README.md
└── requirements.txt
```

---

## 3. Datos utilizados

El conjunto de datos contiene **14 establecimientos** distribuidos en tres categorías:

| Categoría                    | Cantidad |
| ---------------------------- | -------: |
| Droguerías/farmacias         |        6 |
| Centros de atención de salud |        5 |
| Instituciones educativas     |        3 |
| **Total**                    |   **14** |

### 3.1 Instituciones educativas

El Plan de Desarrollo Municipal 2024-2027 identifica tres instituciones educativas ubicadas en la zona urbana de Santa Rosa del Sur:

* I.E. Técnica en Informática María Montessori.
* I.E. Técnico Comercial María Inmaculada.
* I.E. Técnica Agropecuaria Alfredo Nobel.

Por lo tanto, para el análisis de cobertura educativa se utilizaron estas tres instituciones como puntos generadores del diagrama de Voronoi.

### 3.2 Fuentes

Las fuentes utilizadas para construir el conjunto de datos fueron:

* **IGAC:** cartografía básica 1:1.000 de Santa Rosa del Sur, elaborada en 2023.
* **Secretaría de Educación de Bolívar:** directorio de establecimientos educativos.
* **Plan de Desarrollo Municipal 2024-2027:** información sobre infraestructura educativa.
* **OpenStreetMap / Mapcarta:** referencias geográficas para establecimientos de salud.
* **Directorios públicos y resultados de Google Business:** referencias para droguerías y algunos servicios de salud.

Fuente cartográfica del IGAC:

[Servicio cartográfico IGAC — Santa Rosa del Sur](https://mapas.igac.gov.co/server/rest/services/carto/carto1000santarosadelsur13688000/MapServer?utm_source=chatgpt.com)

### 3.3 Precisión de las coordenadas

El archivo `services.csv` incluye el campo `precision`, que permite indicar el nivel de precisión de las coordenadas:

* `exacta`: coordenada disponible directamente en una fuente geográfica.
* `aproximada`: coordenada estimada a partir de una dirección o referencia cartográfica.

Esto es relevante porque los diagramas de Voronoi dependen directamente de la posición de cada punto. Por esta razón, las coordenadas aproximadas constituyen una fuente de incertidumbre en el resultado.

---

## 4. Metodología

Cada establecimiento se representa como un punto en un plano y se genera un **diagrama de Voronoi independiente para cada categoría de servicio**.

No se mezclan farmacias, centros de salud y colegios dentro de un mismo diagrama, ya que cada categoría representa un conjunto diferente de servicios.

Para un conjunto de establecimientos con puntos generadores \(p_i\), la celda de Voronoi asociada al punto \(p_i\) se define como:

$$
V_i = \{x : d(x,p_i) \leq d(x,p_j), \forall j \neq i\}
$$

Es decir, una celda contiene todos los puntos del espacio cuyo establecimiento más cercano es el asociado a dicha celda.

La distancia utilizada es la **distancia euclidiana**.

### 4.1 Sistema de coordenadas

Las coordenadas originales del archivo `services.csv` se encuentran en latitud y longitud, correspondientes a **EPSG:4326**.

Antes de realizar los cálculos, estas coordenadas se transforman a:

**EPSG:9377 — MAGNA-SIRGAS / Origen-Nacional**

Esto permite trabajar con coordenadas métricas y realizar los cálculos de distancia en metros, evitando calcular distancias euclidianas directamente sobre grados de latitud y longitud.

La transformación se realiza mediante la librería `pyproj`.

### 4.2 Construcción de las celdas de Voronoi

La implementación actual no depende de una función externa para generar regiones infinitas de Voronoi.

Cada celda comienza siendo toda la **ventana de análisis** y posteriormente se recorta mediante los semiplanos definidos por cada par de establecimientos.

Para dos puntos \(p_i\) y \(p_j\), la condición:

$$
\|x-p_i\|^2 \leq \|x-p_j\|^2
$$

puede expresarse como:

$$
2(p_j-p_i)\cdot x
\leq
\|p_j\|^2-\|p_i\|^2
$$

Esta desigualdad representa el semiplano correspondiente a todos los puntos que están al menos tan cerca de \(p_i\) como de \(p_j\).

El procedimiento utilizado es:

1. Se toma la ventana completa de análisis como la celda inicial.
2. Se compara el establecimiento actual con cada uno de los demás establecimientos de la misma categoría.
3. Se calcula el semiplano correspondiente a cada comparación.
4. La celda se recorta utilizando dicho semiplano.
5. El proceso continúa hasta haber comparado el punto con todos los demás.
6. El polígono resultante corresponde a la celda de Voronoi del establecimiento.

Este procedimiento permite obtener directamente las regiones limitadas al dominio de análisis y evita depender de un radio artificial para cerrar las regiones infinitas.

### 4.3 Cobertura de la ventana de análisis

Al construir cada celda partiendo de la misma ventana de análisis y recortarla mediante las condiciones de Voronoi, las celdas resultantes forman una partición del dominio.

Por lo tanto:

* Las celdas no deberían presentar solapamientos interiores.
* Las celdas no deberían dejar espacios vacíos dentro de la ventana.
* La totalidad de la ventana queda asignada al establecimiento más cercano de la categoría correspondiente.

Los límites entre dos celdas representan aproximadamente los puntos que se encuentran a igual distancia de los dos establecimientos.

### 4.4 Ventana de análisis

El repositorio **no contiene un polígono digital del perímetro urbano oficial** de Santa Rosa del Sur.

Por esta razón, el script utiliza una **ventana rectangular de análisis** alrededor de los establecimientos registrados. Esta ventana permite limitar el cálculo y la visualización al entorno de la cabecera municipal.

> **Importante:** la ventana rectangular utilizada en el ejercicio **no representa el perímetro legal urbano del municipio**.

Su función es definir un dominio espacial para el cálculo de los diagramas. Por esta razón, las celdas que alcanzan los bordes de la ventana deben interpretarse con precaución.

Para una versión geográficamente más rigurosa, la ventana rectangular debería reemplazarse por un polígono digital correspondiente al perímetro urbano oficial.

---

## 5. Interpretación de los diagramas

Los diagramas permiten analizar la distribución espacial de los establecimientos a partir de la distancia geométrica.

### Celdas pequeñas

Una celda pequeña generalmente indica que el establecimiento tiene otros establecimientos de la misma categoría relativamente cerca.

Esto representa una **mayor concentración espacial** del servicio.

### Celdas grandes

Una celda grande indica que el establecimiento se encuentra relativamente más separado de los demás puntos de la misma categoría.

Por lo tanto, puede representar una zona con **menor densidad espacial del servicio** y una mayor distancia geométrica relativa al establecimiento más cercano.

Sin embargo, una celda grande **no demuestra por sí sola que exista una zona desatendida**.

### Celdas en los bordes

Las celdas que alcanzan los límites de la ventana de análisis deben interpretarse con precaución, debido a que parte de su extensión está determinada por el límite artificial utilizado.

Por esta razón:

> **Una celda grande ubicada en el borde de la ventana no constituye automáticamente evidencia de falta de cobertura.**

---

## 6. Resultados

### 6.1 Droguerías/farmacias

El diagrama correspondiente a las droguerías permite observar la distribución espacial de los seis establecimientos registrados.

Las regiones ubicadas alrededor de zonas donde existen varios establecimientos presentan celdas más pequeñas, mientras que los puntos ubicados hacia los extremos de la distribución generan regiones de mayor tamaño.

Esto permite identificar sectores con diferentes niveles de proximidad geométrica a las droguerías.

### 6.2 Centros de atención de salud

El diagrama de servicios de salud contiene cinco establecimientos.

Se observa una distribución espacial en la que algunos servicios se encuentran relativamente próximos entre sí, generando regiones de menor tamaño, mientras que otros puntos presentan una separación mayor respecto a sus vecinos.

El diagrama permite identificar las diferencias de proximidad geométrica entre los distintos sectores de la ventana de análisis.

### 6.3 Instituciones educativas

El análisis educativo utiliza tres instituciones ubicadas en la zona urbana:

* I.E. Técnica en Informática María Montessori.
* I.E. Técnico Comercial María Inmaculada.
* I.E. Técnica Agropecuaria Alfredo Nobel.

Debido a que solamente existen tres puntos generadores, las celdas resultantes son relativamente grandes en comparación con las obtenidas para farmacias y servicios de salud.

Esto permite observar cómo una menor cantidad de establecimientos produce regiones de influencia espacial más extensas.

---

## 7. Comparación entre los tres diagramas

Los tres diagramas utilizan el mismo principio matemático, pero cada uno se calcula de manera independiente utilizando únicamente los establecimientos de su respectiva categoría.

La comparación permite observar diferencias en la distribución espacial:

* Las droguerías cuentan con seis puntos generadores.
* Los servicios de salud cuentan con cinco puntos generadores.
* Las instituciones educativas cuentan con tres puntos generadores.
* Una menor cantidad de establecimientos produce, en general, regiones de Voronoi más extensas.
* La distribución espacial de los establecimientos no es completamente uniforme.
* Los patrones de farmacias y servicios de salud pueden presentar similitudes cuando ambos tipos de servicio se concentran en sectores similares.
* El patrón educativo puede diferir debido al menor número de instituciones consideradas.

Es importante aclarar que la similitud entre dos diagramas no significa que los servicios tengan la misma cobertura. Cada diagrama representa la proximidad únicamente respecto a los establecimientos de su propia categoría.

---

## 8. Consideraciones sobre cobertura

Los diagramas de Voronoi permiten estudiar la **proximidad geométrica**, pero no constituyen por sí mismos una medición completa de cobertura o accesibilidad.

Una zona con una celda grande puede ser un sector que requiere un análisis adicional, pero para determinar si realmente existe un déficit de servicio sería necesario considerar otros factores como:

* Cantidad de población.
* Distribución de la población por sectores.
* Capacidad de los establecimientos.
* Demanda de los servicios.
* Red vial.
* Distancia por las calles.
* Tiempo de desplazamiento.
* Transporte disponible.
* Horarios de atención.
* Servicios específicos ofrecidos.

Por lo tanto, los resultados obtenidos deben entenderse como una **primera aproximación espacial** a la distribución de los servicios.

---

## 9. Limitaciones

El análisis presenta las siguientes limitaciones:

### 9.1 Perímetro urbano

No se dispone dentro del repositorio de un polígono digital del perímetro urbano oficial. En consecuencia, se utiliza una ventana rectangular de análisis.

### 9.2 Distancia euclidiana

El modelo utiliza distancia euclidiana y no distancia sobre la red vial.

Por lo tanto:

```text
Distancia geométrica ≠ accesibilidad real
```

### 9.3 Coordenadas aproximadas

Algunas coordenadas del archivo `services.csv` son aproximadas. Los errores de posición pueden modificar los límites de las celdas de Voronoi.

### 9.4 Distribución de la población

El modelo no incorpora la cantidad ni la distribución espacial de habitantes.

### 9.5 Capacidad de los establecimientos

El tamaño de una celda no indica la capacidad del establecimiento para atender la demanda existente.

### 9.6 Características del servicio

No se consideran diferencias entre los servicios ofrecidos por los establecimientos.

Por ejemplo, dos centros de salud pueden tener áreas de atención diferentes aunque sus posiciones sean similares.

---

## 10. Tecnologías y dependencias

El ejercicio fue implementado en Python utilizando las siguientes librerías:

| Librería     | Función                                      |
| ------------ | -------------------------------------------- |
| `pandas`     | Lectura y manipulación de los datos          |
| `numpy`      | Operaciones numéricas y cálculo vectorial    |
| `matplotlib` | Generación y visualización de los diagramas  |
| `shapely`    | Construcción y manipulación de geometrías    |
| `pyproj`     | Transformación entre sistemas de coordenadas |

Las dependencias se encuentran especificadas en `requirements.txt`.

Actualmente **no se requiere `scipy`**, debido a que la construcción de las celdas de Voronoi se realiza directamente mediante el recorte de semiplanos.

---

## 11. Ejecución

Crear el entorno virtual:

```bash
python -m venv .venv
```

### Windows PowerShell

Activar el entorno virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instalar las dependencias:

```powershell
pip install -r requirements.txt
```

Ejecutar el script:

```powershell
python scripts/voronoi_services.py
```

Las figuras serán generadas automáticamente en la carpeta `figures/`.

---

## 12. Resultados generados

La ejecución del script genera las siguientes imágenes:

1. `figures/voronoi_farmacias.png`
2. `figures/voronoi_salud.png`
3. `figures/voronoi_colegios.png`
4. `figures/distribucion_conjunta.png`

Los tres primeros archivos contienen los diagramas de Voronoi independientes para cada categoría.

El archivo `distribucion_conjunta.png` muestra la ubicación de los tres tipos de servicios dentro de la misma ventana de análisis, permitiendo comparar visualmente su distribución espacial.

---

## 13. Conclusión

El ejercicio permite analizar la distribución espacial de droguerías, centros de atención de salud e instituciones educativas en la cabecera municipal de Santa Rosa del Sur mediante diagramas de Voronoi.

La metodología asigna a cada establecimiento la región cuyos puntos se encuentran más cerca de este que de cualquier otro establecimiento de la misma categoría.

El uso de coordenadas proyectadas en EPSG:9377 permite realizar los cálculos en metros, mientras que la construcción de las celdas mediante recorte de semiplanos permite obtener una partición completa de la ventana de análisis.

Los resultados permiten identificar diferencias en la concentración espacial de los servicios y sectores con mayor o menor proximidad geométrica. No obstante, estos resultados representan únicamente una aproximación espacial y no permiten determinar por sí solos la existencia de déficit de cobertura.

Para mejorar el análisis sería necesario incorporar el perímetro urbano oficial, la red vial, la población, los tiempos de desplazamiento y las características y capacidades de cada establecimiento.
