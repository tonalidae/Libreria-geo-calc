"""
Módulo de cálculo de rumbos y azimuts geográficos.

Funciones para determinar la dirección de viaje entre puntos
y calcular puntos intermedios en la superficie terrestre.
"""

import math
from typing import Tuple

EARTH_RADIUS_KM = 6371.0


def initial_bearing(lat1: float, lon1: float,
                    lat2: float, lon2: float) -> float:
    """
    Calcula el rumbo inicial (azimut) desde el punto 1 al punto 2.

    El rumbo se mide en grados desde el norte verdadero en sentido
    horario (0° = Norte, 90° = Este, 180° = Sur, 270° = Oeste).

    Parámetros
    ----------
    lat1 : float
        Latitud del punto de origen en grados decimales.
    lon1 : float
        Longitud del punto de origen en grados decimales.
    lat2 : float
        Latitud del punto de destino en grados decimales.
    lon2 : float
        Longitud del punto de destino en grados decimales.

    Retorna
    -------
    float
        Rumbo inicial en grados (0–360).

    Ejemplos
    --------
    >>> initial_bearing(4.7110, -74.0721, 3.8667, -77.0333)
    249.67...
    """
    lat1_r = math.radians(lat1)
    lat2_r = math.radians(lat2)
    dlon = math.radians(lon2 - lon1)

    x = math.sin(dlon) * math.cos(lat2_r)
    y = (math.cos(lat1_r) * math.sin(lat2_r)
         - math.sin(lat1_r) * math.cos(lat2_r) * math.cos(dlon))
    bearing = math.degrees(math.atan2(x, y))
    return (bearing + 360) % 360


def final_bearing(lat1: float, lon1: float,
                  lat2: float, lon2: float) -> float:
    """
    Calcula el rumbo final al llegar al punto 2 desde el punto 1.

    Parámetros
    ----------
    lat1 : float
        Latitud del punto de origen en grados decimales.
    lon1 : float
        Longitud del punto de origen en grados decimales.
    lat2 : float
        Latitud del punto de destino en grados decimales.
    lon2 : float
        Longitud del punto de destino en grados decimales.

    Retorna
    -------
    float
        Rumbo final en grados (0–360).
    """
    return (initial_bearing(lat2, lon2, lat1, lon1) + 180) % 360


def midpoint(lat1: float, lon1: float,
             lat2: float, lon2: float) -> Tuple[float, float]:
    """
    Calcula el punto medio en la línea geodésica entre dos puntos.

    Parámetros
    ----------
    lat1 : float
        Latitud del primer punto en grados decimales.
    lon1 : float
        Longitud del primer punto en grados decimales.
    lat2 : float
        Latitud del segundo punto en grados decimales.
    lon2 : float
        Longitud del segundo punto en grados decimales.

    Retorna
    -------
    tuple[float, float]
        (latitud, longitud) del punto medio en grados decimales.

    Ejemplos
    --------
    >>> midpoint(0.0, 0.0, 0.0, 10.0)
    (0.0, 5.0)
    """
    lat1_r = math.radians(lat1)
    lat2_r = math.radians(lat2)
    lon1_r = math.radians(lon1)
    dlon = math.radians(lon2 - lon1)

    Bx = math.cos(lat2_r) * math.cos(dlon)
    By = math.cos(lat2_r) * math.sin(dlon)
    lat_m = math.atan2(
        math.sin(lat1_r) + math.sin(lat2_r),
        math.sqrt((math.cos(lat1_r) + Bx) ** 2 + By ** 2)
    )
    lon_m = lon1_r + math.atan2(By, math.cos(lat1_r) + Bx)
    return (math.degrees(lat_m), (math.degrees(lon_m) + 540) % 360 - 180)


def destination_point(lat: float, lon: float,
                      bearing: float, distance_km: float) -> Tuple[float, float]:
    """
    Calcula las coordenadas de un punto destino dado un punto de origen,
    un rumbo y una distancia.

    Parámetros
    ----------
    lat : float
        Latitud del punto de origen en grados decimales.
    lon : float
        Longitud del punto de origen en grados decimales.
    bearing : float
        Rumbo en grados (0 = Norte, 90 = Este).
    distance_km : float
        Distancia en kilómetros.

    Retorna
    -------
    tuple[float, float]
        (latitud, longitud) del punto destino en grados decimales.

    Ejemplos
    --------
    >>> destination_point(0.0, 0.0, 90.0, 111.195)
    (0.0, 1.0...)
    """
    delta = distance_km / EARTH_RADIUS_KM
    theta = math.radians(bearing)
    lat_r = math.radians(lat)
    lon_r = math.radians(lon)

    lat2 = math.asin(
        math.sin(lat_r) * math.cos(delta)
        + math.cos(lat_r) * math.sin(delta) * math.cos(theta)
    )
    lon2 = lon_r + math.atan2(
        math.sin(theta) * math.sin(delta) * math.cos(lat_r),
        math.cos(delta) - math.sin(lat_r) * math.sin(lat2)
    )
    return (math.degrees(lat2), (math.degrees(lon2) + 540) % 360 - 180)
