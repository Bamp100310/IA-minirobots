import csv

import pytest

from ordenes import actualizar_historial, generar_orden

FECHA = "2026-10-02"


def test_primera_orden_es_ot_0001_y_queda_abierta():
    """CA-02.1"""
    ordenes = []
    orden = generar_orden("R-07", "rueda izquierda no gira", ordenes, fecha=FECHA)
    assert orden == {"id": "OT-0001", "equipo": "R-07", "falla": "rueda izquierda no gira",
                     "fecha": FECHA, "estado": "abierta"}
    assert ordenes == [orden]


def test_consecutivo_sigue_al_mayor_existente():
    """CA-02.2"""
    ordenes = [{"id": "OT-0001"}, {"id": "OT-0005"}]
    orden = generar_orden("R-03", "sensor sin lectura", ordenes, fecha=FECHA)
    assert orden["id"] == "OT-0006"
    assert len({o["id"] for o in ordenes}) == 3


@pytest.mark.parametrize("falla", ["", "   "])
def test_falla_vacia_se_rechaza_sin_crear_orden(falla):
    """CA-02.3"""
    ordenes = []
    with pytest.raises(ValueError):
        generar_orden("R-07", falla, ordenes, fecha=FECHA)
    assert ordenes == []


def test_historial_inexistente_se_crea_con_encabezado(tmp_path):
    """CA-02.4"""
    ruta = tmp_path / "historial.csv"
    orden = generar_orden("R-07", "rueda izquierda no gira", [], fecha=FECHA)
    assert actualizar_historial(orden, ruta) == 1
    with open(ruta, encoding="utf-8", newline="") as f:
        filas = list(csv.reader(f))
    assert filas[0] == ["fecha", "orden", "equipo", "falla", "estado"]
    assert filas[1] == [FECHA, "OT-0001", "R-07", "rueda izquierda no gira", "abierta"]


def test_segundo_registro_conserva_el_primero(tmp_path):
    """CA-02.5"""
    ruta = tmp_path / "historial.csv"
    ordenes = []
    actualizar_historial(generar_orden("R-07", "rueda izquierda no gira", ordenes, fecha=FECHA), ruta)
    primera = ruta.read_text(encoding="utf-8")
    total = actualizar_historial(generar_orden("R-02", "batería, no carga", ordenes, fecha=FECHA), ruta)
    assert total == 2
    assert ruta.read_text(encoding="utf-8").startswith(primera)
