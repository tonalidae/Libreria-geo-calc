"""
Módulo de cálculo de distancias geográficas.

Implementa fórmulas para calcular distancias entre puntos
en la superficie terrestre.
"""

import math

# Radio de la Tierra en kilómetros (modelo esférico)
EARTH_RADIUS_KM = 6371.0

# Parámetros del elipsoide WGS-84
WGS84_A = 6378137.0          # semieje mayor en metros
WGS84_F = 1 / 298.257223563  # achatamiento
WGS84_B = WGS84_A * (1 - WGS84_F)  # semieje menor en metros


def haversine(lat1: float, lon1: float, lat2: float, lon2: float,
              unit: str = "km") -> float:
    """
    Calcula la distancia entre dos puntos geográficos usando la fórmula
    de Haversine (modelo esférico).

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
    unit : str, opcional
        Unidad de la distancia resultante: 'km' (kilómetros, por defecto),
        'm' (metros), 'mi' (millas), 'nm' (millas náuticas).

    Retorna
    -------
    float
        Distancia entre los dos puntos en la unidad indicada.

    Ejemplos
    --------
    >>> haversine(4.7110, -74.0721, 3.8667, -77.0333)
    360.15...

    Referencias
    -----------
    Sinnott, R.W. (1984). "Virtues of the Haversine".
    Sky and Telescope, 68(2), 159.
    """
    lat1_r = math.radians(lat1)
    lat2_r = math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (math.sin(dlat / 2) ** 2
         + math.cos(lat1_r) * math.cos(lat2_r) * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance_km = EARTH_RADIUS_KM * c

    conversions = {
        "km": 1.0,
        "m": 1000.0,
        "mi": 0.621371,
        "nm": 0.539957,
    }
    if unit not in conversions:
        raise ValueError(
            f"Unidad '{unit}' no reconocida. Use: {list(conversions.keys())}"
        )
    return distance_km * conversions[unit]


def vincenty(lat1: float, lon1: float, lat2: float, lon2: float,
             unit: str = "km", max_iter: int = 200,
             tol: float = 1e-12) -> float:
    """
    Calcula la distancia geodésica entre dos puntos usando la fórmula
    de Vincenty (elipsoide WGS-84).

    Es más precisa que Haversine para distancias cortas y largas.

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
    unit : str, opcional
        Unidad de la distancia resultante: 'km' (por defecto), 'm', 'mi', 'nm'.
    max_iter : int, opcional
        Número máximo de iteraciones (por defecto 200).
    tol : float, opcional
        Tolerancia de convergencia (por defecto 1e-12).

    Retorna
    -------
    float
        Distancia geodésica en la unidad indicada.

    Lanza
    -----
    ValueError
        Si la fórmula no converge (puntos casi antipodales).

    Referencias
    -----------
    Vincenty, T. (1975). "Direct and Inverse Solutions of Geodesics on the
    Ellipsoid with application of nested equations".
    Survey Review, 23(176), 88–93.
    """
    a = WGS84_A
    f = WGS84_F
    b = WGS84_B

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    L = math.radians(lon2 - lon1)

    U1 = math.atan((1 - f) * math.tan(phi1))
    U2 = math.atan((1 - f) * math.tan(phi2))
    sin_U1, cos_U1 = math.sin(U1), math.cos(U1)
    sin_U2, cos_U2 = math.sin(U2), math.cos(U2)

    lam = L
    for _ in range(max_iter):
        sin_lam = math.sin(lam)
        cos_lam = math.cos(lam)
        sin_sigma = math.sqrt(
            (cos_U2 * sin_lam) ** 2
            + (cos_U1 * sin_U2 - sin_U1 * cos_U2 * cos_lam) ** 2
        )
        if sin_sigma == 0:
            return 0.0  # puntos coincidentes
        cos_sigma = sin_U1 * sin_U2 + cos_U1 * cos_U2 * cos_lam
        sigma = math.atan2(sin_sigma, cos_sigma)
        sin_alpha = cos_U1 * cos_U2 * sin_lam / sin_sigma
        cos2_alpha = 1 - sin_alpha ** 2
        if cos2_alpha == 0:
            cos_2sigma_m = 0.0
        else:
            cos_2sigma_m = cos_sigma - 2 * sin_U1 * sin_U2 / cos2_alpha
        C = f / 16 * cos2_alpha * (4 + f * (4 - 3 * cos2_alpha))
        lam_prev = lam
        lam = L + (1 - C) * f * sin_alpha * (
            sigma + C * sin_sigma * (
                cos_2sigma_m + C * cos_sigma * (-1 + 2 * cos_2sigma_m ** 2)
            )
        )
        if abs(lam - lam_prev) < tol:
            break
    else:
        raise ValueError(
            "La fórmula de Vincenty no convergió. "
            "Los puntos podrían ser casi antipodales."
        )

    u2 = cos2_alpha * (a ** 2 - b ** 2) / b ** 2
    A_vin = 1 + u2 / 16384 * (4096 + u2 * (-768 + u2 * (320 - 175 * u2)))
    B_vin = u2 / 1024 * (256 + u2 * (-128 + u2 * (74 - 47 * u2)))
    delta_sigma = B_vin * sin_sigma * (
        cos_2sigma_m + B_vin / 4 * (
            cos_sigma * (-1 + 2 * cos_2sigma_m ** 2)
            - B_vin / 6 * cos_2sigma_m * (-3 + 4 * sin_sigma ** 2)
            * (-3 + 4 * cos_2sigma_m ** 2)
        )
    )
    distance_m = b * A_vin * (sigma - delta_sigma)
    distance_km = distance_m / 1000.0

    conversions = {
        "km": 1.0,
        "m": 1000.0,
        "mi": 0.621371,
        "nm": 0.539957,
    }
    if unit not in conversions:
        raise ValueError(
            f"Unidad '{unit}' no reconocida. Use: {list(conversions.keys())}"
        )
    return distance_km * conversions[unit]
