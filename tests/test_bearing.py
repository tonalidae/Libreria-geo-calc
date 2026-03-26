"""Pruebas para el módulo de cálculo de rumbos."""

import math
import pytest
from geo_calc.bearing import (
    initial_bearing,
    final_bearing,
    midpoint,
    destination_point,
)

BOGOTA = (4.7110, -74.0721)
MEDELLIN = (6.2442, -75.5812)


class TestInitialBearing:
    def test_norte_puro(self):
        bearing = initial_bearing(0.0, 0.0, 1.0, 0.0)
        assert bearing == pytest.approx(0.0, abs=0.01)

    def test_este_puro(self):
        bearing = initial_bearing(0.0, 0.0, 0.0, 1.0)
        assert bearing == pytest.approx(90.0, abs=0.01)

    def test_sur_puro(self):
        bearing = initial_bearing(1.0, 0.0, 0.0, 0.0)
        assert bearing == pytest.approx(180.0, abs=0.01)

    def test_oeste_puro(self):
        bearing = initial_bearing(0.0, 1.0, 0.0, 0.0)
        assert bearing == pytest.approx(270.0, abs=0.01)

    def test_rango_valido(self):
        b = initial_bearing(*BOGOTA, *MEDELLIN)
        assert 0.0 <= b < 360.0

    def test_bogota_medellin(self):
        b = initial_bearing(*BOGOTA, *MEDELLIN)
        # Medellín está al noroeste de Bogotá (entre 270° y 360°)
        assert 270 < b < 360


class TestFinalBearing:
    def test_opuesto_al_inverso(self):
        fb = final_bearing(*BOGOTA, *MEDELLIN)
        ib_inv = initial_bearing(*MEDELLIN, *BOGOTA)
        assert fb == pytest.approx((ib_inv + 180) % 360, abs=1e-6)

    def test_rango_valido(self):
        fb = final_bearing(*BOGOTA, *MEDELLIN)
        assert 0.0 <= fb < 360.0


class TestMidpoint:
    def test_mismo_punto(self):
        lat, lon = midpoint(4.0, -74.0, 4.0, -74.0)
        assert lat == pytest.approx(4.0, abs=1e-6)
        assert lon == pytest.approx(-74.0, abs=1e-6)

    def test_ecuador_horizontal(self):
        lat, lon = midpoint(0.0, 0.0, 0.0, 10.0)
        assert lat == pytest.approx(0.0, abs=1e-6)
        assert lon == pytest.approx(5.0, abs=1e-4)

    def test_meridiano_vertical(self):
        lat, lon = midpoint(0.0, 0.0, 10.0, 0.0)
        assert lat == pytest.approx(5.0, abs=1e-4)
        assert lon == pytest.approx(0.0, abs=1e-6)

    def test_simetria(self):
        lat1, lon1 = midpoint(*BOGOTA, *MEDELLIN)
        lat2, lon2 = midpoint(*MEDELLIN, *BOGOTA)
        assert lat1 == pytest.approx(lat2, abs=1e-6)
        assert lon1 == pytest.approx(lon2, abs=1e-6)


class TestDestinationPoint:
    def test_norte_1_grado(self):
        """100 km al norte desde el ecuador."""
        lat, lon = destination_point(0.0, 0.0, 0.0, 100.0)
        assert lat > 0.0
        assert lon == pytest.approx(0.0, abs=0.01)

    def test_este_1_grado(self):
        """Avanzar al este en el ecuador debe mantener latitud 0."""
        lat, lon = destination_point(0.0, 0.0, 90.0, 100.0)
        assert lat == pytest.approx(0.0, abs=0.01)
        assert lon > 0.0

    def test_distancia_cero(self):
        lat, lon = destination_point(4.711, -74.072, 45.0, 0.0)
        assert lat == pytest.approx(4.711, abs=1e-4)
        assert lon == pytest.approx(-74.072, abs=1e-4)
