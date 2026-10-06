"""Consulta de repuestos y existencias (ticket 01)."""
import re

FORMATO = re.compile(r"REP-\d{4}")


def _normalizar(codigo):
    "Quita espacios alrededor y exige el formato REP-0000 (supuesto S-03)."
    codigo = str(codigo).strip()
    if not FORMATO.fullmatch(codigo):
        raise ValueError(f"Código '{codigo}' inválido: se espera el formato REP-0000.")
    return codigo


def buscar_repuesto(codigo, catalogo):
    "Datos del repuesto, o None si el código no está en el catálogo (RF-7.4a)."
    codigo = _normalizar(codigo)
    datos = catalogo.get(codigo)
    if datos is None:
        return None
    return {"codigo": codigo, "descripcion": datos["descripcion"], "equipos": list(datos["equipos"])}


def consultar_existencias(codigo, almacen):
    "Unidades disponibles en el almacén; 0 si el repuesto no figura (RF-7.4b)."
    return int(almacen.get(_normalizar(codigo), 0))
