"""Cruza los criterios de aceptación de un ticket con las pruebas que los citan.

Uso:  python trazabilidad.py <ticket.md> <carpeta_de_pruebas>

Una prueba cubre un criterio cuando su nombre o docstring contiene el identificador (CA-01.1).
Termina con código 1 si algún criterio queda sin prueba.
"""
import ast
import re
import sys
from pathlib import Path


def criterios_del_ticket(ruta):
    texto = Path(ruta).read_text(encoding="utf-8")
    return re.findall(r"^- \[[ x]\] \*\*(CA-[\w.]+)\*\*\s*(.+)$", texto, re.M)


def pruebas_por_criterio(carpeta):
    cubre = {}
    for archivo in sorted(Path(carpeta).rglob("test_*.py")):
        arbol = ast.parse(archivo.read_text(encoding="utf-8"))
        for nodo in ast.walk(arbol):
            if isinstance(nodo, ast.FunctionDef) and nodo.name.startswith("test_"):
                texto = nodo.name + " " + (ast.get_docstring(nodo) or "")
                for ident in re.findall(r"CA-\d+\.\d+", texto):
                    cubre.setdefault(ident, []).append(f"{archivo.name}::{nodo.name}")
    return cubre


def matriz(ruta_ticket, carpeta):
    cubre = pruebas_por_criterio(carpeta)
    return [(ident, frase, cubre.get(ident, [])) for ident, frase in criterios_del_ticket(ruta_ticket)]


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    sys.stdout.reconfigure(encoding="utf-8")
    filas = matriz(sys.argv[1], sys.argv[2])
    faltan = 0
    for ident, frase, pruebas in filas:
        estado = ", ".join(pruebas) if pruebas else "SIN PRUEBA"
        faltan += not pruebas
        print(f"{ident:8} -> {estado}")
    print(f"\n{len(filas) - faltan} de {len(filas)} criterios cubiertos.")
    sys.exit(1 if faltan else 0)
