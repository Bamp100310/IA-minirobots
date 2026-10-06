# 04: Responder preguntas sobre los documentos del curso, citando la fuente

| Campo | Valor |
|---|---|
| **Tipo** | Funcionalidad |
| **Prioridad** | Debe |
| **Estimación** | 5 puntos |
| **Requerimientos** | RF-7.3, RES-7.O, RES-02, RES-03 |
| **Bloqueado por** | Ninguno |
| **Estado** | Listo para implementar |

## Contexto

El numeral 3 del ejercicio 7.11 pide un chatbot construido con base en los documentos entregados para el curso, que son los mismos siete PDF de los que salieron estos requerimientos. La sección 7.7 del capítulo describe el esquema RAG: cargar los documentos, convertirlos en texto, partirlos, indexarlos y recuperar los fragmentos relevantes antes de generar la respuesta.

## Objetivo

Un estudiante hace una pregunta sobre el curso y recibe una respuesta basada en los documentos, con el documento y la página de donde sale.

## Alcance

**Incluye**
- Indexación de los PDF de una carpeta, por página.
- Recuperación de los fragmentos más relevantes y respuesta con un modelo local (RES-7.O, P-05).
- Citas de documento y página en cada respuesta.

**Fuera de alcance**
- Interfaz web; el chatbot se usa desde el notebook.
- Documentos distintos de PDF.

## Interfaz acordada

- `indexar(carpeta)` devuelve un índice con los fragmentos de todos los PDF de la carpeta y su documento y página de origen.
- `responder(pregunta, indice)` devuelve el texto de la respuesta y la lista de citas (documento, página) en que se basa.

## Criterios de aceptación

- [ ] **CA-04.1** Dado el índice de los siete documentos, cuando se pregunta cuántos ejercicios del capítulo 3 hay que desarrollar, entonces la respuesta dice tres y cita 3_Algoritmos_Gen_ticos_26_2.pdf, página 25.
- [ ] **CA-04.2** Dado el índice, cuando se pregunta qué es un autómata celular, entonces la respuesta cita al menos una página de 2._Aut__matas_Celulares_26_2.pdf.
- [ ] **CA-04.3** Dada una pregunta sin relación con el curso, cuando se responde, entonces el chatbot dice que no está en los documentos y no devuelve citas.
- [ ] **CA-04.4** Dado un PDF nuevo en la carpeta, cuando se vuelve a indexar, entonces sus páginas aparecen como citas posibles.

## Casos borde

- Texto extraído con espacios de más ("C uando", "requerim ientos"): la búsqueda no debe depender de palabras exactas.
- Preguntas que mezclan dos capítulos: la respuesta cita ambos.

## Dependencias y riesgos

- Reutiliza la extracción de texto de la skill capturar-requerimientos.
- Los modelos pequeños pueden responder sin usar el contexto; los criterios verifican las citas, no la redacción.

## Preguntas abiertas

- P-05: si la sugerencia de Ollama no aplica al numeral 3, el modelo se cambia sin tocar la interfaz; no bloquea.

## Definición de terminado

- [ ] Todos los criterios de aceptación tienen una prueba automatizada que pasa.
- [ ] La suite completa pasa.
- [ ] El trabajo queda explicado (skill `explicar-en-html`).
