---
name: documentar-ticket
description: Redacta un ticket de trabajo completo (contexto, objetivo, alcance, interfaz acordada, criterios de aceptación verificables, dependencias, riesgos, estimación y definición de terminado) a partir de requerimientos, una conversación o una idea suelta. Úsala cuando el usuario pida crear, escribir o documentar un ticket, issue, historia de usuario o tarea, o cuando haya que describir el trabajo antes de implementarlo.
---

# Documentar ticket

Un ticket está bien escrito cuando otra persona, o un agente que no vio esta conversación,
puede hacer el trabajo **sin preguntar nada**. Esta skill recibe la salida de
`capturar-requerimientos` (o el contexto disponible) y entrega tickets listos para
`implementar-con-pruebas`.

## Proceso

1. **Reunir el contexto.** Leer `requerimientos.md` si existe, la conversación y el código
   del proyecto. Usar el vocabulario del dominio que ya usa el proyecto.

2. **Cortar en rebanadas verticales.** Cada ticket entrega un comportamiento completo que se
   puede demostrar solo (entrada → lógica → salida → pruebas), no una capa aislada.
   Si no cabe en una sesión de trabajo (más de 8 puntos), se parte. Cada ticket declara
   qué otros tickets lo **bloquean**.

3. **Redactar con [PLANTILLA_TICKET.md](PLANTILLA_TICKET.md)**, sin dejar secciones vacías
   (si algo no aplica, escribir "No aplica" y por qué).

4. **Escribir los criterios de aceptación** en formato *Dado / Cuando / Entonces*, con datos
   concretos y observables desde la interfaz pública. Cada criterio lleva un identificador
   `CA-<ticket>.<n>` y cada requerimiento del alcance queda cubierto por al menos un criterio.
   Estos criterios son la lista de pruebas que escribirá `implementar-con-pruebas`.

5. **Acordar la interfaz pública** (las *costuras* donde se probará): nombres de funciones,
   entradas, salidas y errores. Es lo único de diseño que entra en el ticket.

6. **Validar** el ticket y corregir hasta que no haya errores:

   ```bash
   python scripts/validar_ticket.py tickets/01-<slug>.md
   ```

7. **Confirmar con el usuario** el corte, el alcance y las dependencias. Luego guardar un archivo
   por ticket en `tickets/NN-<slug>.md` (numerados en orden de dependencias) o publicarlos en el
   gestor del proyecto (por ejemplo `gh issue create --body-file tickets/01-<slug>.md`).

## Reglas

- El ticket describe el **qué** y el **por qué**; el **cómo** queda para quien implementa.
  No incluir rutas de archivos ni código, salvo la firma de la interfaz acordada.
- *Fuera de alcance* siempre está escrito: es lo que evita discusiones después.
- Las preguntas abiertas de los requerimientos que afectan al ticket se copian al ticket;
  un ticket con una pregunta que bloquea el trabajo no está listo.
- Estimación en puntos de Fibonacci (1, 2, 3, 5, 8).
