"""Pruebas para el módulo de cálculo de distancias."""

import math
import pytest
from geo_calc.distance import haversine, vincenty


# Pares de coordenadas de referencia (ciudades colombianas y mundiales)
# Bogotá (4.7110° N, 74.0721° O)
# Medellín (6.2442° N, 75.5812° O)
# Quibdó (5.6919° N, 76.6583° O)
# Cali (3.4516° N, 76.5320° O)
# Bogotá ↔ Medellín: ≈ 213 km (línea recta)

BOGOTA = (4.7110, -74.0721)
MEDELLIN = (6.2442, -75.5812)
CALI = (3.4516, -76.5320)


class TestHaversine:
    def test_bogota_medellin_km(self):
        dist = haversine(*BOGOTA, *MEDELLIN)
        assert 230 < dist < 250, f"Distancia inesperada: {dist} km"

    def test_puntos_identicos(self):
        assert haversine(0.0, 0.0, 0.0, 0.0) == pytest.approx(0.0)

    def test_unidad_metros(self):
        dist_km = haversine(*BOGOTA, *MEDELLIN, unit="km")
        dist_m = haversine(*BOGOTA, *MEDELLIN, unit="m")
        assert dist_m == pytest.approx(dist_km * 1000, rel=1e-9)

    def test_unidad_millas(self):
        dist_km = haversine(*BOGOTA, *MEDELLIN, unit="km")
        dist_mi = haversine(*BOGOTA, *MEDELLIN, unit="mi")
        assert dist_mi == pytest.approx(dist_km * 0.621371, rel=1e-6)

    def test_unidad_millas_nauticas(self):
        dist_km = haversine(*BOGOTA, *MEDELLIN, unit="km")
        dist_nm = haversine(*BOGOTA, *MEDELLIN, unit="nm")
        assert dist_nm == pytest.approx(dist_km * 0.539957, rel=1e-6)

    def test_unidad_invalida(self):
        with pytest.raises(ValueError, match="no reconocida"):
            haversine(*BOGOTA, *MEDELLIN, unit="parsec")

    def test_simetria(self):
        d1 = haversine(*BOGOTA, *MEDELLIN)
        d2 = haversine(*MEDELLIN, *BOGOTA)
        assert d1 == pytest.approx(d2, rel=1e-9)

    def test_cruce_ecuador(self):
        norte = (1.0, 0.0)
        sur = (-1.0, 0.0)
        dist = haversine(*norte, *sur)
        expected = 2 * math.radians(1.0) * 6371.0
        assert dist == pytest.approx(expected, rel=1e-3)

    def test_cruce_antimeridiano(self):
        # (0°, 179°) y (0°, -179°) están a 2° de separación cruzando el
        # antimeridiano; el camino más corto es 2°.
        p1 = (0.0, 179.0)
        p2 = (0.0, -179.0)
        dist = haversine(*p1, *p2)
        assert dist == pytest.approx(2 * math.radians(1.0) * 6371.0, rel=1e-3)


class TestVincenty:
    def test_bogota_medellin_km(self):
        dist = vincenty(*BOGOTA, *MEDELLIN)
        assert 230 < dist < 250, f"Distancia inesperada: {dist} km"

    def test_puntos_identicos(self):
        assert vincenty(0.0, 0.0, 0.0, 0.0) == pytest.approx(0.0)

    def test_consistencia_haversine(self):
        """Vincenty y Haversine deben coincidir dentro del ~0.3%."""
        d_h = haversine(*BOGOTA, *CALI)
        d_v = vincenty(*BOGOTA, *CALI)
        assert abs(d_h - d_v) / d_v < 0.003

    def test_unidad_metros(self):
        dist_km = vincenty(*BOGOTA, *MEDELLIN, unit="km")
        dist_m = vincenty(*BOGOTA, *MEDELLIN, unit="m")
        assert dist_m == pytest.approx(dist_km * 1000, rel=1e-9)

    def test_simetria(self):
        d1 = vincenty(*BOGOTA, *MEDELLIN)
        d2 = vincenty(*MEDELLIN, *BOGOTA)
        assert d1 == pytest.approx(d2, rel=1e-6)

    def test_unidad_invalida(self):
        with pytest.raises(ValueError, match="no reconocida"):
            vincenty(*BOGOTA, *MEDELLIN, unit="AU")
