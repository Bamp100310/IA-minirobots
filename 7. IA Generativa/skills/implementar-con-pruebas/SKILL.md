---
name: implementar-con-pruebas
description: Implementa un ticket o especificación generando el código y sus pruebas automatizadas con ciclos rojo-verde (TDD) sobre la interfaz acordada, y deja evidencia de cada ciclo y de la trazabilidad criterio-prueba. Úsala cuando el usuario pida implementar, programar o resolver un ticket, generar código para una funcionalidad o escribir sus pruebas.
---

# Implementar con pruebas

Convierte un ticket (salida de `documentar-ticket`) en código que funciona y en pruebas que lo
demuestran. Los criterios de aceptación del ticket son la lista de pruebas.

## Antes de escribir código

1. Leer el ticket completo. Si tiene preguntas abiertas que bloquean, detenerse y preguntar.
2. Identificar las **costuras**: la interfaz pública donde se observará el comportamiento
   (la sección *Interfaz acordada* del ticket). Las pruebas solo tocan esas costuras.
   Si el ticket no la trae, proponerla y confirmarla con el usuario.
3. Revisar el proyecto: estructura, estilo y herramienta de pruebas existentes.
   Si no hay ninguna, usar Python con `pytest` y un `pytest.ini` con `pythonpath = .`.
4. Crear la interfaz con cuerpos `raise NotImplementedError`, para que la prueba en rojo
   falle por la razón correcta y no por un error de importación.

## El ciclo, una rebanada a la vez

Para cada criterio `CA-NN.n`, en orden:

1. **Rojo.** Escribir **una** prueba que exprese el criterio, con el identificador en el
   docstring. Ejecutarla y comprobar que falla por la razón correcta:

   ```bash
   python scripts/ciclo.py --fase rojo --prueba tests/test_x.py::test_y --criterio CA-01.1
   ```

2. **Verde.** Escribir el mínimo código que la hace pasar, y volver a ejecutar:

   ```bash
   python scripts/ciclo.py --fase verde --prueba tests/test_x.py::test_y --criterio CA-01.1
   ```

`ciclo.py` registra cada fase en `bitacora_tdd.json` y avisa si una prueba pasa en rojo
(no prueba nada nuevo) o si falla por importación o sintaxis (falla por la razón equivocada).
No escribir todas las pruebas primero: cada ciclo enseña algo que cambia la siguiente prueba.

## Al terminar

1. Ejecutar la suite completa: `python -m pytest -q`.
2. Refactorizar solo con la suite en verde, y volver a ejecutarla.
3. Comprobar la trazabilidad: todos los criterios del ticket tienen al menos una prueba.

   ```bash
   python scripts/trazabilidad.py tickets/01-<slug>.md tests/
   ```

4. Revisar con [REVISION.md](REVISION.md).
5. Hacer *commit* citando el ticket. Entregar código, pruebas, bitácora y salida de `pytest`,
   que son la evidencia que usará `explicar-en-html`.

## Qué es una buena prueba

- Verifica **comportamiento** a través de la interfaz pública, no detalles internos:
  si se reescribe la implementación sin cambiar el comportamiento, la prueba sigue pasando.
- El valor esperado viene de una **fuente independiente** (el ejemplo del ticket, un cálculo
  hecho a mano), nunca se recalcula como lo hace el código.
- El nombre dice el comportamiento: `test_rechaza_codigo_con_formato_invalido`.
- Es aislada: crea sus propios datos (`tmp_path`, *fixtures*) y no depende del orden.
- Solo se simulan (*mock*) las fronteras externas: red, reloj, bases de datos reales.
