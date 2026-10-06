"""Valida que un ticket cumpla la plantilla de la skill documentar-ticket.

Uso:  python validar_ticket.py <ticket.md> [<ticket2.md> ...]

Termina con código 0 si no hay errores. Las advertencias no bloquean.
"""
import re
import sys
from pathlib import Path

SECCIONES = ["Contexto", "Objetivo", "Alcance", "Interfaz acordada", "Criterios de aceptación",
             "Casos borde", "Dependencias y riesgos", "Preguntas abiertas", "Definición de terminado"]
CAMPOS = ["Tipo", "Prioridad", "Estimación", "Requerimientos", "Bloqueado por", "Estado"]
FIBONACCI = {"1", "2", "3", "5", "8"}


def secciones(texto):
    partes = re.split(r"^## +(.+?)\s*$", texto, flags=re.M)
    return {partes[i].strip(): partes[i + 1].strip() for i in range(1, len(partes), 2)}


def validar(texto):
    errores, avisos = [], []
    if not re.search(r"^# +\S", texto, re.M):
        errores.append("Falta el título (línea '# NN: ...').")
    cuerpo = secciones(texto)
    for s in SECCIONES:
        if s not in cuerpo:
            errores.append(f"Falta la sección '## {s}'.")
        elif not cuerpo[s]:
            errores.append(f"La sección '{s}' está vacía (escriba 'No aplica' y por qué).")
    campos = dict(re.findall(r"^\|\s*\*\*(.+?)\*\*\s*\|\s*(.*?)\s*\|\s*$", texto, re.M))
    for c in CAMPOS:
        if not campos.get(c):
            errores.append(f"Falta el campo '{c}' en la tabla de metadatos.")
    estimacion = re.findall(r"\d+", campos.get("Estimación", ""))
    if estimacion and estimacion[0] not in FIBONACCI:
        errores.append(f"Estimación {estimacion[0]}: use 1, 2, 3, 5 u 8 (si es mayor, parta el ticket).")
    if campos.get("Requerimientos") and not re.search(r"\b(RF|RNF|RES)-\d+", campos["Requerimientos"]):
        avisos.append("El ticket no cita identificadores de requerimientos (RF-, RNF-, RES-).")

    alcance = cuerpo.get("Alcance", "")
    if "Fuera de alcance" not in alcance:
        errores.append("El alcance no declara 'Fuera de alcance'.")

    criterios = re.findall(r"^- \[ \] \*\*(CA-[\w.]+)\*\*\s*(.+)$", cuerpo.get("Criterios de aceptación", ""), re.M)
    if not criterios:
        errores.append("No hay criterios con el formato '- [ ] **CA-NN.n** Dado ..., cuando ..., entonces ...'.")
    for ident, frase in criterios:
        f = frase.lower()
        if not (re.search(r"\bdad[oa]s?\b", f) and "cuando" in f and "entonces" in f):
            errores.append(f"{ident} no sigue el formato Dado / Cuando / Entonces.")
        if re.search(r"\b(r[áa]pido|f[áa]cil|amigable|adecuad\w*|correctamente|bien)\b", f):
            avisos.append(f"{ident} usa un término no verificable; cámbielo por un dato medible.")
    ids = [i for i, _ in criterios]
    if len(ids) != len(set(ids)):
        errores.append("Hay identificadores de criterio repetidos.")

    restos = re.findall(r"<[^<>\n]{2,60}>", texto)
    if restos:
        errores.append(f"Quedan marcadores de la plantilla sin llenar: {restos[:3]}")
    return errores, avisos, ids


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    sys.stdout.reconfigure(encoding="utf-8")
    total = 0
    for ruta in sys.argv[1:]:
        errores, avisos, ids = validar(Path(ruta).read_text(encoding="utf-8"))
        estado = "VÁLIDO" if not errores else "CON ERRORES"
        print(f"{Path(ruta).name}: {estado}  ({len(ids)} criterios de aceptación)")
        for e in errores:
            print(f"  ERROR  {e}")
        for a in avisos:
            print(f"  AVISO  {a}")
        total += len(errores)
    sys.exit(1 if total else 0)
