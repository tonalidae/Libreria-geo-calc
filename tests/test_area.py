"""Pruebas para el módulo de cálculo de áreas geográficas."""

import pytest
from geo_calc.area import polygon_area, spherical_excess


class TestSphericalExcess:
    def test_triangulo_no_cero(self):
        triangle = [(0.0, 0.0), (0.0, 1.0), (1.0, 0.0)]
        excess = spherical_excess(triangle)
        assert excess > 0.0

    def test_menos_de_tres_puntos(self):
        assert spherical_excess([(0.0, 0.0), (1.0, 1.0)]) == 0.0

    def test_un_punto(self):
        assert spherical_excess([(0.0, 0.0)]) == 0.0


class TestPolygonArea:
    def test_cuadrado_ecuatorial(self):
        """Un cuadrado de 1° × 1° cerca del ecuador tiene aprox. 12 308 km²."""
        square = [(0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0)]
        area = polygon_area(square)
        # La resolución de 1 grado en el ecuador es ≈ 111 km × 111 km
        assert 12000 < area < 13000, f"Área inesperada: {area} km²"

    def test_unidad_m2(self):
        square = [(0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0)]
        area_km2 = polygon_area(square, unit="km2")
        area_m2 = polygon_area(square, unit="m2")
        assert area_m2 == pytest.approx(area_km2 * 1e6, rel=1e-9)

    def test_unidad_ha(self):
        square = [(0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0)]
        area_km2 = polygon_area(square, unit="km2")
        area_ha = polygon_area(square, unit="ha")
        assert area_ha == pytest.approx(area_km2 * 100, rel=1e-9)

    def test_unidad_mi2(self):
        square = [(0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0)]
        area_km2 = polygon_area(square, unit="km2")
        area_mi2 = polygon_area(square, unit="mi2")
        assert area_mi2 == pytest.approx(area_km2 * 0.386102, rel=1e-9)

    def test_area_positiva(self):
        polygon = [(4.711, -74.072), (4.711, -74.0), (4.8, -74.0), (4.8, -74.072)]
        area = polygon_area(polygon)
        assert area > 0.0

    def test_pocos_vertices(self):
        with pytest.raises(ValueError, match="al menos 3"):
            polygon_area([(0.0, 0.0), (1.0, 1.0)])

    def test_unidad_invalida(self):
        square = [(0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0)]
        with pytest.raises(ValueError, match="no reconocida"):
            polygon_area(square, unit="acres")
