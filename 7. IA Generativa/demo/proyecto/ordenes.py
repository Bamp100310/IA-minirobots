"""Órdenes de trabajo e historial de fallas (ticket 02)."""
import csv
from datetime import date
from pathlib import Path

COLUMNAS = ["fecha", "orden", "equipo", "falla", "estado"]


def generar_orden(equipo, falla, ordenes, fecha=None):
    "Crea una orden abierta con consecutivo único y la agrega a la lista (RF-7.4c, S-03)."
    equipo, falla = str(equipo).strip(), str(falla).strip()
    if not equipo or not falla:
        raise ValueError("La orden necesita el equipo y la descripción de la falla.")
    mayor = max((int(o["id"].split("-")[1]) for o in ordenes), default=0)
    orden = {"id": f"OT-{mayor + 1:04d}", "equipo": equipo, "falla": falla,
             "fecha": fecha or date.today().isoformat(), "estado": "abierta"}
    ordenes.append(orden)
    return orden


def actualizar_historial(orden, ruta_csv):
    "Agrega la orden al historial CSV, creándolo si no existe. Devuelve el total de registros (RF-7.4d)."
    ruta = Path(ruta_csv)
    nuevo = not ruta.exists()
    with open(ruta, "a", encoding="utf-8", newline="") as f:
        escritor = csv.writer(f)
        if nuevo:
            escritor.writerow(COLUMNAS)
        escritor.writerow([orden["fecha"], orden["id"], orden["equipo"], orden["falla"], orden["estado"]])
    with open(ruta, encoding="utf-8", newline="") as f:
        return sum(1 for _ in csv.reader(f)) - 1
