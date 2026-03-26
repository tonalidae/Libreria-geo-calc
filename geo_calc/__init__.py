"""
geo_calc - Librería de cálculos geográficos
=============================================

Una librería Python para cálculos geográficos que incluye:
- Distancias entre coordenadas geográficas
- Cálculo de rumbos y azimuts
- Conversión de sistemas de coordenadas
- Cálculo de áreas geográficas
"""

from .distance import haversine, vincenty
from .bearing import initial_bearing, final_bearing, midpoint, destination_point
from .coordinates import (
    decimal_to_dms,
    dms_to_decimal,
    dd_to_utm,
    utm_to_dd,
)
from .area import polygon_area, spherical_excess

__version__ = "1.0.0"
__author__ = "celys"

__all__ = [
    "haversine",
    "vincenty",
    "initial_bearing",
    "final_bearing",
    "midpoint",
    "destination_point",
    "decimal_to_dms",
    "dms_to_decimal",
    "dd_to_utm",
    "utm_to_dd",
    "polygon_area",
    "spherical_excess",
]
