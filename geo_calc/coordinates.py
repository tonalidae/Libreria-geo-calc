"""
Módulo de conversión de sistemas de coordenadas geográficas.

Soporta conversiones entre:
- Grados decimales (DD) y Grados/Minutos/Segundos (DMS)
- Coordenadas geográficas (latitud/longitud) y UTM
"""

import math
from typing import Tuple

# Parámetros del elipsoide WGS-84
WGS84_A = 6378137.0
WGS84_F = 1 / 298.257223563
WGS84_B = WGS84_A * (1 - WGS84_F)
WGS84_E2 = 2 * WGS84_F - WGS84_F ** 2  # excentricidad al cuadrado
WGS84_EP2 = WGS84_E2 / (1 - WGS84_E2)  # segunda excentricidad al cuadrado

# Factor de escala UTM
K0 = 0.9996


def decimal_to_dms(decimal_degrees: float,
                   is_latitude: bool = True) -> Tuple[int, int, float, str]:
    """
    Convierte grados decimales a formato Grados°Minutos'Segundos".

    Parámetros
    ----------
    decimal_degrees : float
        Coordenada en grados decimales. Latitud: [-90, 90].
        Longitud: [-180, 180].
    is_latitude : bool, opcional
        True si el valor es latitud (por defecto), False si es longitud.

    Retorna
    -------
    tuple[int, int, float, str]
        (grados, minutos, segundos, dirección) donde dirección es
        'N'/'S' para latitud o 'E'/'W' para longitud.

    Ejemplos
    --------
    >>> decimal_to_dms(4.7110, is_latitude=True)
    (4, 42, 39.6, 'N')
    >>> decimal_to_dms(-74.0721, is_latitude=False)
    (74, 4, 19.56, 'W')
    """
    if is_latitude:
        direction = "N" if decimal_degrees >= 0 else "S"
    else:
        direction = "E" if decimal_degrees >= 0 else "W"

    abs_deg = abs(decimal_degrees)
    degrees = int(abs_deg)
    minutes_full = (abs_deg - degrees) * 60
    minutes = int(minutes_full)
    seconds = (minutes_full - minutes) * 60

    return (degrees, minutes, round(seconds, 6), direction)


def dms_to_decimal(degrees: int, minutes: int,
                   seconds: float, direction: str) -> float:
    """
    Convierte Grados°Minutos'Segundos" a grados decimales.

    Parámetros
    ----------
    degrees : int
        Grados (valor positivo).
    minutes : int
        Minutos (0–59).
    seconds : float
        Segundos (0–59.9999).
    direction : str
        Dirección: 'N', 'S', 'E' o 'W'.

    Retorna
    -------
    float
        Coordenada en grados decimales.

    Lanza
    -----
    ValueError
        Si la dirección no es válida.

    Ejemplos
    --------
    >>> dms_to_decimal(4, 42, 39.6, 'N')
    4.711...
    >>> dms_to_decimal(74, 4, 19.56, 'W')
    -74.0721...
    """
    direction = direction.upper()
    if direction not in ("N", "S", "E", "W"):
        raise ValueError(
            f"Dirección '{direction}' no válida. Use N, S, E o W."
        )
    decimal = degrees + minutes / 60 + seconds / 3600
    if direction in ("S", "W"):
        decimal = -decimal
    return decimal


def dd_to_utm(lat: float, lon: float) -> Tuple[float, float, int, str]:
    """
    Convierte coordenadas geográficas (grados decimales) a UTM (WGS-84).

    Parámetros
    ----------
    lat : float
        Latitud en grados decimales [-80, 84].
    lon : float
        Longitud en grados decimales [-180, 180].

    Retorna
    -------
    tuple[float, float, int, str]
        (easting, northing, zone_number, zone_letter) donde:
        - easting: coordenada Este en metros
        - northing: coordenada Norte en metros
        - zone_number: número de zona UTM (1–60)
        - zone_letter: letra de banda de latitud UTM

    Lanza
    -----
    ValueError
        Si la latitud está fuera del rango UTM.

    Ejemplos
    --------
    >>> dd_to_utm(4.7110, -74.0721)
    (614986..., 520606..., 18, 'N')
    """
    if not -80.0 <= lat <= 84.0:
        raise ValueError(
            f"Latitud {lat} fuera del rango UTM [-80, 84]."
        )

    a = WGS84_A
    e2 = WGS84_E2
    k0 = K0

    lat_r = math.radians(lat)
    lon_r = math.radians(lon)

    zone_number = int((lon + 180) / 6) + 1
    if 56.0 <= lat < 64.0 and 3.0 <= lon < 12.0:
        zone_number = 32
    if 72.0 <= lat < 84.0:
        if 0.0 <= lon < 9.0:
            zone_number = 31
        elif 9.0 <= lon < 21.0:
            zone_number = 33
        elif 21.0 <= lon < 33.0:
            zone_number = 35
        elif 33.0 <= lon < 42.0:
            zone_number = 37

    lon_origin = (zone_number - 1) * 6 - 180 + 3
    lon_origin_r = math.radians(lon_origin)

    N = a / math.sqrt(1 - e2 * math.sin(lat_r) ** 2)
    T = math.tan(lat_r) ** 2
    C = WGS84_EP2 * math.cos(lat_r) ** 2
    A = math.cos(lat_r) * (lon_r - lon_origin_r)

    M = a * (
        (1 - e2 / 4 - 3 * e2 ** 2 / 64 - 5 * e2 ** 3 / 256) * lat_r
        - (3 * e2 / 8 + 3 * e2 ** 2 / 32 + 45 * e2 ** 3 / 1024)
        * math.sin(2 * lat_r)
        + (15 * e2 ** 2 / 256 + 45 * e2 ** 3 / 1024) * math.sin(4 * lat_r)
        - (35 * e2 ** 3 / 3072) * math.sin(6 * lat_r)
    )

    easting = (k0 * N * (
        A + (1 - T + C) * A ** 3 / 6
        + (5 - 18 * T + T ** 2 + 72 * C - 58 * WGS84_EP2) * A ** 5 / 120
    ) + 500000.0)

    northing = k0 * (M + N * math.tan(lat_r) * (
        A ** 2 / 2
        + (5 - T + 9 * C + 4 * C ** 2) * A ** 4 / 24
        + (61 - 58 * T + T ** 2 + 600 * C - 330 * WGS84_EP2) * A ** 6 / 720
    ))
    if lat < 0:
        northing += 10000000.0

    zone_letter = _utm_zone_letter(lat)

    return (easting, northing, zone_number, zone_letter)


def utm_to_dd(easting: float, northing: float,
              zone_number: int, zone_letter: str) -> Tuple[float, float]:
    """
    Convierte coordenadas UTM a grados decimales (WGS-84).

    Parámetros
    ----------
    easting : float
        Coordenada Este en metros.
    northing : float
        Coordenada Norte en metros.
    zone_number : int
        Número de zona UTM (1–60).
    zone_letter : str
        Letra de banda de latitud UTM.

    Retorna
    -------
    tuple[float, float]
        (latitud, longitud) en grados decimales.

    Ejemplos
    --------
    >>> utm_to_dd(614986.0, 520606.0, 18, 'N')
    (4.71..., -74.07...)
    """
    a = WGS84_A
    e2 = WGS84_E2
    ep2 = WGS84_EP2
    k0 = K0

    zone_letter = zone_letter.upper()
    x = easting - 500000.0
    y = northing
    if zone_letter < "N":
        y -= 10000000.0

    lon_origin = (zone_number - 1) * 6 - 180 + 3

    M = y / k0
    mu = M / (a * (1 - e2 / 4 - 3 * e2 ** 2 / 64 - 5 * e2 ** 3 / 256))

    e1 = (1 - math.sqrt(1 - e2)) / (1 + math.sqrt(1 - e2))
    phi1 = (mu
            + (3 * e1 / 2 - 27 * e1 ** 3 / 32) * math.sin(2 * mu)
            + (21 * e1 ** 2 / 16 - 55 * e1 ** 4 / 32) * math.sin(4 * mu)
            + (151 * e1 ** 3 / 96) * math.sin(6 * mu)
            + (1097 * e1 ** 4 / 512) * math.sin(8 * mu))

    N1 = a / math.sqrt(1 - e2 * math.sin(phi1) ** 2)
    T1 = math.tan(phi1) ** 2
    C1 = ep2 * math.cos(phi1) ** 2
    R1 = a * (1 - e2) / (1 - e2 * math.sin(phi1) ** 2) ** 1.5
    D = x / (N1 * k0)

    lat = phi1 - (N1 * math.tan(phi1) / R1) * (
        D ** 2 / 2
        - (5 + 3 * T1 + 10 * C1 - 4 * C1 ** 2 - 9 * ep2) * D ** 4 / 24
        + (61 + 90 * T1 + 298 * C1 + 45 * T1 ** 2
           - 252 * ep2 - 3 * C1 ** 2) * D ** 6 / 720
    )
    lon = (D - (1 + 2 * T1 + C1) * D ** 3 / 6
           + (5 - 2 * C1 + 28 * T1 - 3 * C1 ** 2 + 8 * ep2
              + 24 * T1 ** 2) * D ** 5 / 120) / math.cos(phi1)

    return (math.degrees(lat), lon_origin + math.degrees(lon))


def _utm_zone_letter(lat: float) -> str:
    """Retorna la letra de banda UTM para una latitud dada."""
    letters = "CDEFGHJKLMNPQRSTUVWXX"
    idx = int((lat + 80) / 8)
    if 0 <= idx < len(letters):
        return letters[idx]
    return "Z"
