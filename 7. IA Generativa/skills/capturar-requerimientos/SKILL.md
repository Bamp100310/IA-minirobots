---
name: capturar-requerimientos
description: Lee documentos provistos por el usuario (PDF, DOCX, TXT o Markdown, como enunciados, solicitudes, actas, pliegos o manuales) y extrae una lista trazable de requerimientos funcionales, no funcionales y restricciones, con la fuente exacta de cada uno y las preguntas abiertas. Úsala cuando el usuario adjunte o mencione documentos y pida requerimientos, alcance, necesidades o "qué hay que hacer".
---

# Capturar requerimientos

Convierte uno o varios documentos en una lista de requerimientos **verificables y trazables**.
Es la primera skill del flujo: su salida es la entrada de `documentar-ticket`.

| | |
|---|---|
| **Entradas** | Documentos `.pdf`, `.docx`, `.txt` o `.md` |
| **Salidas** | `requerimientos.md` (con [PLANTILLA_REQUERIMIENTOS.md](PLANTILLA_REQUERIMIENTOS.md)) y `candidatos.json` |

## Proceso

1. **Extraer el texto completo**, sin resumirlo, conservando página y línea:

   ```bash
   python scripts/extraer_texto.py <documento> > texto.txt
   ```

2. **Detectar candidatos** de forma mecánica. El script propone como candidatos las frases con
   expresiones de obligación (*debe, se requiere, se sugiere, podría, shall, must*), los ítems de las
   secciones de requerimientos (*Ejercicios, Problemas, Requerimientos, Actividades, Entregables*),
   los ítems que empiezan con un verbo en infinitivo o imperativo (*Crear, Tome, Desarrolle*) y las
   reglas de selección (*escoja uno; desarrolle tres de los seis*). A cada uno le asigna tipo,
   prioridad y **confianza**: alta dentro de una sección de requerimientos, media en una lista
   introducida por una frase que termina en «:», baja en la prosa:

   ```bash
   python scripts/detectar_requerimientos.py texto.txt --fuente <documento> --json candidatos.json
   ```

   Con varios documentos se ejecuta una vez por documento. Se revisan primero los de confianza
   alta y media; los de baja se leen por encima para no perder obligaciones escritas en la prosa.

3. **Revisar cada candidato.** El script solo propone; el criterio lo pone el agente:
   - Descartar lo que no es requerimiento (contexto, ejemplos, historia).
   - Partir los compuestos: una oración que pide dos cosas son dos requerimientos.
   - Reescribir cada uno como *"El sistema debe <verbo> <objeto> [condición]"*.
   - Clasificar: **RF** funcional, **RNF** no funcional (desempeño, seguridad, usabilidad,
     disponibilidad), **RES** restricción (tecnología, plazo o norma impuesta).
   - Prioridad MoSCoW según el lenguaje del documento: *debe / se requiere* → **Debe**;
     *debería / se sugiere* → **Debería**; *podría / opcionalmente* → **Podría**.
     Si el documento da a escoger (*desarrolle tres de los seis*), esas opciones son **Elegible** y la
     regla se registra aparte como restricción.
   - Escribir un **criterio de verificación** observable para cada requerimiento.

4. **Buscar lo implícito y lo ambiguo**: datos que nadie define, unidades, volúmenes, quién usa
   el sistema, formatos de archivo. No inventar la respuesta: registrarla como **pregunta abierta**.

5. **Entregar** `requerimientos.md` con la plantilla y mostrar al usuario las preguntas abiertas.

## Reglas

- Toda fila lleva su **fuente** (documento y página o línea) y la **cita textual** del original.
  Lo que no tiene fuente es un supuesto y va a la sección *Supuestos*.
- Si dos documentos se contradicen, se registran ambos y la contradicción va a preguntas abiertas.
- Los identificadores son estables (`RF-01`, `RNF-01`, `RES-01`): otras skills los citan.
- En esta etapa no se proponen soluciones técnicas.
