"""
Módulo de cálculo de áreas geográficas.

Funciones para calcular el área de polígonos geográficos
en la superficie terrestre.
"""

import math
from typing import List, Tuple

EARTH_RADIUS_KM = 6371.0

Coord = Tuple[float, float]


def spherical_excess(polygon: List[Coord]) -> float:
    """
    Calcula el exceso esférico de un polígono en la esfera unitaria.

    Parámetros
    ----------
    polygon : list[tuple[float, float]]
        Lista de tuplas (latitud, longitud) en grados decimales que
        definen el polígono. No es necesario repetir el primer vértice
        al final.

    Retorna
    -------
    float
        Exceso esférico en radianes.
    """
    n = len(polygon)
    if n < 3:
        return 0.0

    total = 0.0
    for i in range(n):
        lat1, lon1 = polygon[i]
        lat2, lon2 = polygon[(i + 1) % n]
        dlon = math.radians(lon2 - lon1)
        lat1_r = math.radians(lat1)
        lat2_r = math.radians(lat2)
        total += dlon * (1 + math.sin(lat1_r) + math.sin(lat2_r)) / 2

    return abs(total)


def polygon_area(polygon: List[Coord], unit: str = "km2") -> float:
    """
    Calcula el área de un polígono geográfico en la superficie terrestre
    usando la fórmula de Girard (exceso esférico).

    Parámetros
    ----------
    polygon : list[tuple[float, float]]
        Lista de tuplas (latitud, longitud) en grados decimales que
        definen el polígono. No es necesario cerrar el polígono
        repitiendo el primer vértice.
    unit : str, opcional
        Unidad del área resultante: 'km2' (km², por defecto),
        'm2' (m²), 'ha' (hectáreas), 'mi2' (millas²).

    Retorna
    -------
    float
        Área del polígono en la unidad indicada.

    Lanza
    -----
    ValueError
        Si el polígono tiene menos de 3 vértices o la unidad no es válida.

    Ejemplos
    --------
    >>> # Cuadrado aproximado de 1° x 1° cerca del ecuador
    >>> sq = [(0, 0), (0, 1), (1, 1), (1, 0)]
    >>> polygon_area(sq)
    12308...

    Notas
    -----
    Este método asume que los bordes del polígono son arcos de gran círculo.
    Para polígonos pequeños la precisión es alta; para polígonos muy grandes
    (continentales) se recomienda usar proyecciones cartográficas dedicadas.
    """
    if len(polygon) < 3:
        raise ValueError("El polígono debe tener al menos 3 vértices.")

    conversions = {
        "km2": 1.0,
        "m2": 1e6,
        "ha": 100.0,
        "mi2": 0.386102,
    }
    if unit not in conversions:
        raise ValueError(
            f"Unidad '{unit}' no reconocida. Use: {list(conversions.keys())}"
        )

    excess = spherical_excess(polygon)
    area_km2 = excess * EARTH_RADIUS_KM ** 2
    return area_km2 * conversions[unit]
