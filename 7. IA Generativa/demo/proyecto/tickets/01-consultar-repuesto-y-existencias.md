# 01: Consultar un repuesto y sus existencias en el almacén

| Campo | Valor |
|---|---|
| **Tipo** | Funcionalidad |
| **Prioridad** | Debe |
| **Estimación** | 3 puntos |
| **Requerimientos** | RF-7.4a, RF-7.4b, RES-02, RES-03 |
| **Bloqueado por** | Ninguno |
| **Estado** | Listo para implementar |

## Contexto

El numeral 4 del ejercicio 7.11 pide un agente de mantenimiento que busque un repuesto por su código y consulte el almacén. Son las dos consultas básicas sobre las que trabajará después el modelo de lenguaje (ticket 03). El curso no define el formato del código ni los datos del catálogo (P-04); el equipo fija el formato REP-0000 (supuesto S-03).

## Objetivo

Dado un código de repuesto, el sistema devuelve su descripción, los equipos compatibles y la cantidad disponible, o explica por qué no puede hacerlo.

## Alcance

**Incluye**
- Búsqueda de un repuesto en el catálogo por su código.
- Consulta de la cantidad disponible en el almacén.
- Rechazo de códigos con formato distinto de REP-0000 (S-03).

**Fuera de alcance**
- Lectura del catálogo desde un archivo o base de datos: el curso no entrega datos de repuestos, así que se recibe como diccionario.
- Conversación en lenguaje natural (ticket 03).

## Interfaz acordada

- `buscar_repuesto(codigo, catalogo)` devuelve un diccionario con `codigo`, `descripcion` y `equipos`, o `None` si el código no está registrado. Lanza `ValueError` si el formato no es REP-0000.
- `consultar_existencias(codigo, almacen)` devuelve un entero con la cantidad disponible (0 si el repuesto no está en el almacén). Lanza `ValueError` si el formato no es REP-0000.

## Criterios de aceptación

- [ ] **CA-01.1** Dado un catálogo con REP-0042 "Motor DC 6 V" compatible con R-01 y R-07, cuando se busca REP-0042, entonces se obtienen esa descripción y esos dos equipos.
- [ ] **CA-01.2** Dado cualquiera de los códigos "42", "REP-42", "rep-0042" y "REP-00420", cuando se busca, entonces se lanza ValueError con un mensaje que menciona el formato REP-0000.
- [ ] **CA-01.3** Dado un código con formato válido que no está en el catálogo (REP-9999), cuando se busca, entonces el resultado es None.
- [ ] **CA-01.4** Dado un almacén con 3 unidades de REP-0042, cuando se consultan sus existencias, entonces el resultado es 3.
- [ ] **CA-01.5** Dado un código válido que no figura en el almacén, cuando se consultan sus existencias, entonces el resultado es 0.

## Casos borde

- Código con espacios alrededor (" REP-0042 "): se aceptan y se ignoran.
- Código en minúsculas: se rechaza, el formato fijado en S-03 es en mayúsculas.

## Dependencias y riesgos

- Riesgo: si P-04 se resuelve con otro formato de código, cambia la validación pero no la interfaz; el catálogo entra como diccionario para aislar su origen.

## Preguntas abiertas

- P-04 no bloquea este ticket: se trabaja con el supuesto S-03.

## Definición de terminado

- [ ] Todos los criterios de aceptación tienen una prueba automatizada que pasa.
- [ ] La suite completa pasa.
- [ ] El trabajo queda explicado (skill `explicar-en-html`).
