---
name: explicar-en-html
description: Genera un documento HTML autocontenido que explica en detalle el trabajo realizado (problema, decisiones, funcionamiento, código clave, pruebas con sus resultados reales, limitaciones y cómo reproducirlo), listo para abrir en el navegador o imprimir. Úsala cuando el usuario pida explicar, documentar o presentar lo que se hizo, o un informe técnico en HTML del trabajo terminado.
---

# Explicar en HTML

Produce una explicación que entiende alguien que **no estuvo** mientras se hacía el trabajo.
Es la última skill del flujo: toma el ticket, el código y la evidencia de
`implementar-con-pruebas` y los convierte en un solo archivo `.html`.

## Proceso

1. **Reunir evidencia, no recuerdos.** Ticket, archivos cambiados, salida real de `pytest`,
   bitácora TDD, mediciones. Toda cifra del documento sale de una ejecución o de un archivo.

2. **Escribir el contenido** en `contenido.json` según [ESQUEMA.md](ESQUEMA.md), con las
   secciones obligatorias:

   | id | Sección | Qué responde |
   |---|---|---|
   | `resumen` | Resumen | Qué se hizo y cuál fue el resultado, en 3 a 5 líneas |
   | `problema` | Problema y contexto | Por qué hacía falta |
   | `decisiones` | Decisiones de diseño | Qué se decidió, qué alternativa se descartó y por qué |
   | `funcionamiento` | Cómo funciona | El recorrido de los datos, paso a paso |
   | `codigo` | Código clave | Fragmentos cortos y comentados, no archivos completos |
   | `pruebas` | Pruebas y resultados | Tabla criterio → prueba → resultado real |
   | `limitaciones` | Limitaciones y trabajo futuro | Lo que no hace y lo que quedó pendiente |
   | `reproducir` | Cómo reproducir | Comandos exactos |

3. **Generar el HTML** con la plantilla de [assets/plantilla.html](assets/plantilla.html):

   ```bash
   python scripts/generar_html.py contenido.json explicacion.html
   ```

   El script escapa el código, arma el índice, verifica las secciones obligatorias y reporta
   advertencias. Corregir hasta que no haya ninguna.

4. **Revisar el resultado** abriéndolo en el navegador (o tomando una captura) antes de
   entregarlo: que se lea bien en tema claro y oscuro, y al imprimir.

## Reglas de redacción

- Definir cada término técnico la primera vez que aparece.
- Explicar el **por qué** de cada decisión, no solo el qué.
- Preferir tablas y listas cortas a párrafos largos; un fragmento de código no pasa de 25 líneas.
- Decir con claridad lo que **no** se hizo o no funcionó.
- El archivo es autocontenido: sin CDN, sin fuentes ni scripts externos; funciona sin conexión.
