# 03: Conversar con el agente usando las funciones como herramientas

| Campo | Valor |
|---|---|
| **Tipo** | Funcionalidad |
| **Prioridad** | Debería |
| **Estimación** | 5 puntos |
| **Requerimientos** | RF-7.4, RES-7.O, RES-02, RES-03 |
| **Bloqueado por** | 01, 02 |
| **Estado** | Listo para implementar |

## Contexto

Con las consultas (ticket 01) y el registro de órdenes (ticket 02) disponibles, falta lo que hace de esto un agente: que el técnico pida las cosas en lenguaje natural y el modelo decida qué función llamar. El capítulo sugiere Ollama en el numeral 2 (RES-7.O); se adopta también aquí para que el agente funcione sin internet (P-05).

## Objetivo

El técnico describe la situación en una frase y el agente decide qué funciones llamar y responde con el resultado.

## Alcance

**Incluye**
- Registro de las cuatro funciones como herramientas del modelo.
- Ciclo de conversación: mensaje, llamadas a herramientas, respuesta.

**Fuera de alcance**
- Interfaz gráfica; la conversación es por consola.

## Interfaz acordada

- `atender(mensaje, estado)` devuelve el texto de la respuesta y la lista de herramientas llamadas, en orden.

## Criterios de aceptación

- [ ] **CA-03.1** Dado el mensaje "¿hay unidades del REP-0042?", cuando el agente lo atiende, entonces llama a consultar_existencias con REP-0042 y la respuesta contiene la cantidad.
- [ ] **CA-03.2** Dado el mensaje "el R-07 no gira la rueda izquierda", cuando el agente lo atiende, entonces llama a generar_orden y luego a actualizar_historial, y la respuesta contiene el identificador de la orden.
- [ ] **CA-03.3** Dado que no hay conexión a internet, cuando el agente atiende un mensaje, entonces responde usando el modelo local.

## Casos borde

- Mensajes con un código mal escrito: el agente transmite el error de formato al técnico.

## Dependencias y riesgos

- Los modelos pequeños de Ollama pueden elegir mal la herramienta; las pruebas deben fijar la semilla y la temperatura en 0.

## Preguntas abiertas

- P-05: si la sugerencia de Ollama no aplica al numeral 4, el modelo se cambia sin tocar la interfaz; no bloquea.

## Definición de terminado

- [ ] Todos los criterios de aceptación tienen una prueba automatizada que pasa.
- [ ] La suite completa pasa.
- [ ] El trabajo queda explicado (skill `explicar-en-html`).
