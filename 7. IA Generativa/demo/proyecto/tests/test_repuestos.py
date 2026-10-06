import pytest

from repuestos import buscar_repuesto, consultar_existencias

CATALOGO = {
    "REP-0042": {"descripcion": "Motor DC 6 V", "equipos": ["R-01", "R-07"]},
    "REP-0100": {"descripcion": "Sensor ultrasónico HC-SR04", "equipos": ["R-03"]},
}
ALMACEN = {"REP-0042": 3, "REP-0100": 12}


def test_busqueda_devuelve_descripcion_y_equipos():
    """CA-01.1"""
    repuesto = buscar_repuesto("REP-0042", CATALOGO)
    assert repuesto["descripcion"] == "Motor DC 6 V"
    assert repuesto["equipos"] == ["R-01", "R-07"]


@pytest.mark.parametrize("codigo", ["42", "REP-42", "rep-0042", "REP-00420"])
def test_rechaza_codigo_con_formato_invalido(codigo):
    """CA-01.2"""
    with pytest.raises(ValueError, match="REP-0000"):
        buscar_repuesto(codigo, CATALOGO)


def test_codigo_valido_no_registrado_devuelve_none():
    """CA-01.3"""
    assert buscar_repuesto("REP-9999", CATALOGO) is None


def test_existencias_de_repuesto_en_almacen():
    """CA-01.4"""
    assert consultar_existencias("REP-0042", ALMACEN) == 3


def test_existencias_de_repuesto_ausente_es_cero():
    """CA-01.5"""
    assert consultar_existencias("REP-0777", ALMACEN) == 0
