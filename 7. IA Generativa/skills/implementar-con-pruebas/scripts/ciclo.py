"""Ejecuta una prueba en la fase rojo o verde del ciclo TDD y la registra en la bitácora.

Uso:  python ciclo.py --fase rojo|verde --prueba <archivo::prueba> [--criterio CA-01.1]
                      [--bitacora bitacora_tdd.json]

Se ejecuta desde la raíz del proyecto. Código de salida 0 si la fase salió como se esperaba:
en rojo la prueba debe fallar por una aserción o un NotImplementedError; en verde debe pasar.
"""
import argparse
import json
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

RAZON_EQUIVOCADA = r"\b(ImportError|ModuleNotFoundError|SyntaxError|IndentationError|NameError|fixture '.+' not found)\b"


def ejecutar(prueba):
    inicio = time.perf_counter()
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", prueba],
                       capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr, time.perf_counter() - inicio


def evaluar(fase, codigo, salida):
    """Devuelve (resultado, cumple, mensaje)."""
    if codigo == 5 or "no tests ran" in salida or "not found" in salida and "ERROR" in salida:
        return "no encontrada", False, "pytest no encontró la prueba indicada."
    paso = codigo == 0
    if fase == "rojo":
        if paso:
            return "pasa", False, "La prueba pasa sin código nuevo: no está probando nada nuevo."
        error = re.search(RAZON_EQUIVOCADA, salida)
        if error:
            return "falla", False, f"Falla por la razón equivocada ({error.group(1)}); cree primero la interfaz."
        return "falla", True, "Falla por la razón correcta."
    if paso:
        return "pasa", True, "La prueba pasa."
    return "falla", False, "La prueba todavía falla."


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--fase", choices=["rojo", "verde"], required=True)
    ap.add_argument("--prueba", required=True)
    ap.add_argument("--criterio", default="")
    ap.add_argument("--bitacora", default="bitacora_tdd.json")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    codigo, salida, segundos = ejecutar(args.prueba)
    resultado, cumple, mensaje = evaluar(args.fase, codigo, salida)
    ultima = [l for l in salida.strip().splitlines() if l.strip()][-1:] or [""]

    ruta = Path(args.bitacora)
    bitacora = json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else []
    bitacora.append({"momento": datetime.now().isoformat(timespec="seconds"), "fase": args.fase,
                     "criterio": args.criterio, "prueba": args.prueba, "resultado": resultado,
                     "esperado": "falla" if args.fase == "rojo" else "pasa", "cumple": cumple,
                     "mensaje": mensaje, "pytest": ultima[0], "segundos": round(segundos, 2)})
    ruta.write_text(json.dumps(bitacora, ensure_ascii=False, indent=2), encoding="utf-8")

    marca = "OK " if cumple else "!! "
    print(f"{marca}[{args.fase.upper():5}] {args.criterio:8} {args.prueba}: {resultado}. {mensaje}")
    if not cumple:
        print(salida[-1500:])
    sys.exit(0 if cumple else 1)


if __name__ == "__main__":
    main()
