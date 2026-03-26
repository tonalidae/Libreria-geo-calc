# Libreria-geo-calc

Librería Python para cálculos geográficos y geodésicos. Proporciona funciones
para calcular distancias, rumbos, conversión de coordenadas y áreas en la
superficie terrestre.

## Instalación

```bash
pip install .
```

Para instalar con dependencias de desarrollo (pytest):

```bash
pip install ".[dev]"
```

## Módulos

### `geo_calc.distance` — Distancias geográficas

#### `haversine(lat1, lon1, lat2, lon2, unit='km')`

Calcula la distancia entre dos puntos usando la **fórmula de Haversine**
(modelo esférico). Rápida y suficientemente precisa para la mayoría de usos.

```python
from geo_calc import haversine

# Distancia Bogotá ↔ Medellín
dist = haversine(4.7110, -74.0721, 6.2442, -75.5812)
print(f"{dist:.2f} km")  # ~238.67 km

# En metros
dist_m = haversine(4.7110, -74.0721, 6.2442, -75.5812, unit="m")
```

Unidades disponibles: `'km'`, `'m'`, `'mi'` (millas), `'nm'` (millas náuticas).

#### `vincenty(lat1, lon1, lat2, lon2, unit='km')`

Calcula la distancia geodésica usando la **fórmula de Vincenty** sobre el
elipsoide WGS-84. Más precisa que Haversine, especialmente para distancias
cortas.

```python
from geo_calc import vincenty

dist = vincenty(4.7110, -74.0721, 6.2442, -75.5812)
print(f"{dist:.2f} km")  # ~238.14 km
```

---

### `geo_calc.bearing` — Rumbos y azimuts

#### `initial_bearing(lat1, lon1, lat2, lon2)`

Rumbo inicial desde el punto 1 al punto 2 (0° = Norte, sentido horario).

```python
from geo_calc import initial_bearing

rumbo = initial_bearing(4.7110, -74.0721, 6.2442, -75.5812)
print(f"{rumbo:.2f}°")  # noroeste ≈ 320°
```

#### `final_bearing(lat1, lon1, lat2, lon2)`

Rumbo al llegar al punto de destino.

#### `midpoint(lat1, lon1, lat2, lon2)`

Punto medio en la geodésica entre dos puntos.

```python
from geo_calc import midpoint

lat, lon = midpoint(4.7110, -74.0721, 6.2442, -75.5812)
print(f"({lat:.4f}, {lon:.4f})")
```

#### `destination_point(lat, lon, bearing, distance_km)`

Coordenadas del punto destino dado origen, rumbo y distancia.

```python
from geo_calc.bearing import destination_point

lat, lon = destination_point(4.7110, -74.0721, 0.0, 100.0)  # 100 km al norte
```

---

### `geo_calc.coordinates` — Conversión de coordenadas

#### `decimal_to_dms(decimal_degrees, is_latitude=True)`

Convierte grados decimales a Grados°Minutos'Segundos".

```python
from geo_calc import decimal_to_dms

deg, min_, sec, dir_ = decimal_to_dms(4.7110, is_latitude=True)
print(f"{deg}°{min_}'{sec:.2f}\"{dir_}")  # 4°42'39.60"N

deg, min_, sec, dir_ = decimal_to_dms(-74.0721, is_latitude=False)
print(f"{deg}°{min_}'{sec:.2f}\"{dir_}")  # 74°4'19.56"W
```

#### `dms_to_decimal(degrees, minutes, seconds, direction)`

Convierte DMS a grados decimales.

```python
from geo_calc import dms_to_decimal

lat = dms_to_decimal(4, 42, 39.6, 'N')   # 4.711
lon = dms_to_decimal(74, 4, 19.56, 'W')  # -74.0721
```

#### `dd_to_utm(lat, lon)`

Convierte coordenadas geográficas a **UTM WGS-84**.

```python
from geo_calc import dd_to_utm

easting, northing, zone, letter = dd_to_utm(4.7110, -74.0721)
print(f"Zona {zone}{letter}: {easting:.0f}E, {northing:.0f}N")
# Zona 18N: 614986E, 520606N
```

#### `utm_to_dd(easting, northing, zone_number, zone_letter)`

Convierte coordenadas UTM a grados decimales.

```python
from geo_calc import utm_to_dd

lat, lon = utm_to_dd(614986.0, 520606.0, 18, 'N')
print(f"({lat:.4f}, {lon:.4f})")  # (4.7110, -74.0721)
```

---

### `geo_calc.area` — Áreas geográficas

#### `polygon_area(polygon, unit='km2')`

Calcula el área de un polígono geográfico (lista de tuplas `(lat, lon)`)
usando la fórmula del exceso esférico de Girard.

```python
from geo_calc import polygon_area

# Polígono alrededor de Bogotá
poligono = [
    (4.5, -74.3),
    (4.5, -73.8),
    (5.0, -73.8),
    (5.0, -74.3),
]
area = polygon_area(poligono)
print(f"{area:.0f} km²")
```

Unidades disponibles: `'km2'`, `'m2'`, `'ha'` (hectáreas), `'mi2'`.

---

## Pruebas

```bash
python -m pytest tests/ -v
```

## Referencia de sistemas de coordenadas

| Sistema | Descripción |
|---------|-------------|
| DD | Grados decimales (ej: 4.711, -74.072) |
| DMS | Grados°Minutos'Segundos" + dirección |
| UTM | Universal Transverse Mercator, elipsoide WGS-84 |

## Licencia

MIT
