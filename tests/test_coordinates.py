"""Pruebas para el módulo de conversión de coordenadas."""

import pytest
from geo_calc.coordinates import (
    decimal_to_dms,
    dms_to_decimal,
    dd_to_utm,
    utm_to_dd,
)


class TestDecimalToDMS:
    def test_latitud_positiva(self):
        deg, min_, sec, direction = decimal_to_dms(4.7110, is_latitude=True)
        assert deg == 4
        assert min_ == 42
        assert sec == pytest.approx(39.6, abs=0.001)
        assert direction == "N"

    def test_latitud_negativa(self):
        deg, min_, sec, direction = decimal_to_dms(-4.7110, is_latitude=True)
        assert direction == "S"
        assert deg == 4

    def test_longitud_positiva(self):
        deg, min_, sec, direction = decimal_to_dms(10.5, is_latitude=False)
        assert direction == "E"
        assert deg == 10
        assert min_ == 30

    def test_longitud_negativa(self):
        deg, min_, sec, direction = decimal_to_dms(-74.0721, is_latitude=False)
        assert direction == "W"
        assert deg == 74
        assert min_ == 4
        assert sec == pytest.approx(19.56, abs=0.01)

    def test_cero(self):
        deg, min_, sec, direction = decimal_to_dms(0.0, is_latitude=True)
        assert deg == 0
        assert min_ == 0
        assert sec == pytest.approx(0.0)
        assert direction == "N"


class TestDMSToDecimal:
    def test_norte(self):
        result = dms_to_decimal(4, 42, 39.6, "N")
        assert result == pytest.approx(4.7110, abs=0.0001)

    def test_sur(self):
        result = dms_to_decimal(4, 42, 39.6, "S")
        assert result == pytest.approx(-4.7110, abs=0.0001)

    def test_este(self):
        result = dms_to_decimal(74, 4, 19.56, "E")
        assert result == pytest.approx(74.0721, abs=0.0001)

    def test_oeste(self):
        result = dms_to_decimal(74, 4, 19.56, "W")
        assert result == pytest.approx(-74.0721, abs=0.0001)

    def test_direction_minuscula(self):
        result = dms_to_decimal(4, 42, 39.6, "n")
        assert result == pytest.approx(4.7110, abs=0.0001)

    def test_direction_invalida(self):
        with pytest.raises(ValueError, match="no válida"):
            dms_to_decimal(4, 42, 39.6, "X")

    def test_redondeo_inverso(self):
        """Convertir decimal → DMS → decimal debe ser consistente."""
        original = 3.8667
        deg, min_, sec, direction = decimal_to_dms(original, is_latitude=True)
        result = dms_to_decimal(deg, min_, sec, direction)
        assert result == pytest.approx(original, abs=1e-5)


class TestDDtoUTM:
    def test_bogota(self):
        easting, northing, zone, letter = dd_to_utm(4.7110, -74.0721)
        assert zone == 18
        assert letter == "N"
        assert 500000 < easting < 800000
        assert 400000 < northing < 700000

    def test_hemisferio_sur(self):
        easting, northing, zone, letter = dd_to_utm(-3.4516, -76.5320)
        # Northing en hemisferio sur debe ser > 9 millones
        assert northing > 9_000_000

    def test_latitud_invalida(self):
        with pytest.raises(ValueError, match="fuera del rango UTM"):
            dd_to_utm(85.0, 0.0)

    def test_latitud_invalida_sur(self):
        with pytest.raises(ValueError, match="fuera del rango UTM"):
            dd_to_utm(-81.0, 0.0)


class TestUTMtoDD:
    def test_bogota_ida_vuelta(self):
        lat_orig, lon_orig = 4.7110, -74.0721
        easting, northing, zone, letter = dd_to_utm(lat_orig, lon_orig)
        lat, lon = utm_to_dd(easting, northing, zone, letter)
        assert lat == pytest.approx(lat_orig, abs=1e-4)
        assert lon == pytest.approx(lon_orig, abs=1e-4)

    def test_medellin_ida_vuelta(self):
        lat_orig, lon_orig = 6.2442, -75.5812
        easting, northing, zone, letter = dd_to_utm(lat_orig, lon_orig)
        lat, lon = utm_to_dd(easting, northing, zone, letter)
        assert lat == pytest.approx(lat_orig, abs=1e-4)
        assert lon == pytest.approx(lon_orig, abs=1e-4)
