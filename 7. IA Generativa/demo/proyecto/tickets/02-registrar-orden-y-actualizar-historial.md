# 02: Registrar una orden de trabajo y actualizar el historial de fallas

| Campo | Valor |
|---|---|
| **Tipo** | Funcionalidad |
| **Prioridad** | Debe |
| **Estimación** | 3 puntos |
| **Requerimientos** | RF-7.4c, RF-7.4d, RES-02, RES-03 |
| **Bloqueado por** | Ninguno |
| **Estado** | Listo para implementar |

## Contexto

El numeral 4 del ejercicio 7.11 pide que el agente genere una orden de trabajo con la falla y el equipo, y que actualice el historial de fallas. El curso no define el formato de la orden ni del historial (P-04); el equipo fija un consecutivo OT-0000, el estado inicial "abierta" y un historial en CSV (supuesto S-03).

## Objetivo

Al reportar una falla de un equipo, el sistema crea una orden de trabajo abierta con un consecutivo único y la agrega al historial de fallas.

## Alcance

**Incluye**
- Creación de la orden con equipo, falla, fecha, estado "abierta" y consecutivo OT-0000 (S-03).
- Registro de la orden en el historial en formato CSV (S-03).

**Fuera de alcance**
- Prioridad y cierre de órdenes: el numeral 4 no los pide.
- Conversación en lenguaje natural (ticket 03).

## Interfaz acordada

- `generar_orden(equipo, falla, ordenes, fecha=None)` devuelve un diccionario con `id`, `equipo`, `falla`, `fecha` y `estado`, y lo agrega a la lista `ordenes`. Lanza `ValueError` si el equipo o la falla están vacíos.
- `actualizar_historial(orden, ruta_csv)` agrega la orden al archivo CSV (lo crea con encabezado si no existe) y devuelve el número de registros del historial.

## Criterios de aceptación

- [ ] **CA-02.1** Dado que no hay órdenes, cuando se genera una para el equipo R-07 con la falla "rueda izquierda no gira", entonces la orden es OT-0001, queda "abierta" y conserva equipo y falla.
- [ ] **CA-02.2** Dado que existen OT-0001 y OT-0005, cuando se genera una nueva orden, entonces su identificador es OT-0006 y no repite ninguno existente.
- [ ] **CA-02.3** Dada una falla vacía o solo con espacios, cuando se intenta generar la orden, entonces se lanza ValueError y no se agrega ninguna orden.
- [ ] **CA-02.4** Dado que el archivo de historial no existe, cuando se registra una orden, entonces se crea con encabezado y 1 registro.
- [ ] **CA-02.5** Dado un historial con 1 registro, cuando se registra otra orden, entonces quedan 2 registros y el primero no cambia.

## Casos borde

- Identificadores con huecos (OT-0001, OT-0005): el siguiente es el mayor más uno.
- Texto de la falla con comas o tildes: el CSV debe conservarlo intacto.

## Dependencias y riesgos

- Si P-04 fija otro formato de historial, cambia la escritura del archivo pero no la interfaz.

## Preguntas abiertas

- P-04 no bloquea este ticket: se trabaja con el supuesto S-03.

## Definición de terminado

- [ ] Todos los criterios de aceptación tienen una prueba automatizada que pasa.
- [ ] La suite completa pasa.
- [ ] El trabajo queda explicado (skill `explicar-en-html`).
