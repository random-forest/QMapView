import math
import os

import numpy as np
from numpy import log, tan, cos, arctan, exp
from numpy import pi as PI
from PyQt5.QtCore import QPointF

from src.PointWGS84 import PointWGS84

SAMPLES = 1201
HGTDIR = "data/hgt"

EarthRadius = 6371
Deg2Rad = PI / 180.0
PI2 = PI * 2.0


def get_altitude(lon, lat):
    hgt_file = get_file_name(lon, lat)
    if hgt_file:
        return read_altitude_from_file(hgt_file, lon, lat)
    return -1


def read_altitude_from_file(hgt_file, lon, lat):
    # HGT is 16bit signed integer(i2) - big endian(>)

    with open(hgt_file, 'rb') as hgt_data:
        elevations = np.fromfile(
            hgt_data, np.dtype('>i2'),
            SAMPLES * SAMPLES).reshape((SAMPLES, SAMPLES)
                                       )
        lat_row = int(round((lat - int(lat)) * (SAMPLES - 1), 0))
        lon_row = int(round((lon - int(lon)) * (SAMPLES - 1), 0))

        return elevations[SAMPLES - 1 - lat_row, lon_row].astype(int)


def get_file_name(lon, lat):
    global ew, ns
    if lat >= 0:
        ns = 'N'
    elif lat < 0:
        ns = 'S'

    if lon >= 0:
        ew = 'E'
    elif lon < 0:
        ew = 'W'

    hgt_file = "%(ns)s%(lat)02d%(ew)s%(lon)03d.hgt" % {'lat': abs(lat), 'lon': abs(lon), 'ns': ns, 'ew': ew}
    hgt_file_path = os.path.join(HGTDIR, hgt_file)

    if os.path.isfile(hgt_file_path):
        return hgt_file_path
    else:
        return None


def height_matrix(tl_lat, tl_lon, br_lat, br_lon, step):
    """
      Returns a matrix of tuples with the coordinates of the WGS84 and
      height in meters (lat, lon, height) for a given rectangle.
      tl_lat, tl_lon, br_lat, br_lon - top left and bottom right corners
      of the selection rectangle. step - distance between points in meters
      """

    next_bottom_point_lat, next_bottom_point_lon = move_lat_lon(
        tl_lat, tl_lon, math.radians(90), step
    )
    next_right_point_lat, next_right_point_lon = move_lat_lon(
        tl_lat, tl_lon, math.radians(180), step
    )

    rect_lat_size = br_lat - tl_lat
    rect_lon_size = br_lon - tl_lon

    square_lat_size = next_right_point_lat - tl_lat
    square_lon_size = next_bottom_point_lon - tl_lon

    w_square_count = int(rect_lat_size / square_lat_size)
    h_square_count = int(rect_lon_size / square_lon_size)

    # top row
    lat, lon = tl_lat, tl_lon
    top_row = [(lat, lon)]

    for i in range(w_square_count):
        lat += square_lat_size
        top_row.append((lat, lon))

    top_row.append((br_lat, lon))

    # left col
    lat, lon = tl_lat, tl_lon
    left_col = [(lat, lon)]

    for i in range(h_square_count):
        lon += square_lon_size
        left_col.append((lat, lon))

    left_col.append((lat, br_lon))

    # matrix
    import time

    start_time = time.time()

    matrix = []
    for lat, _ in top_row:
        row_seq = []
        for _, lon in left_col:
            height = get_altitude(lon, lat)
            row_seq.append((lat, lon, height))
        matrix.append(row_seq)

    end_time = time.time()

    print('matrix generation time:', end_time - start_time)

    return matrix


def rotate_point(origin, point, angle):
    """
      Rotate a point counterclockwise by a given angle around a given origin.
      The angle should be given in radians.
      origin, point is QPointF
      """

    dx = point.x() - origin.x()
    dy = point.y() - origin.y()

    return QPointF(
        origin.x() + math.cos(angle) * dx - math.sin(angle) * dy,
        origin.y() + math.sin(angle) * dx + math.cos(angle) * dy
    )


def move_point(point, bearing, distance):
    lat1 = math.radians(point.lat)
    lon1 = math.radians(point.lon)

    dByR = distance / 1000 / EarthRadius

    lat2 = math.asin(
        math.sin(lat1) * math.cos(dByR) +
        math.cos(lat1) * math.sin(dByR) * math.cos(bearing)
    )
    lon2 = lon1 + math.atan2(
        math.sin(bearing) * math.sin(dByR) * math.cos(lat1),
        math.cos(dByR) - math.sin(lat1) * math.sin(lat2)
    )
    return PointWGS84(math.degrees(lat2), math.degrees(lon2))


def move_lat_lon(lat, lon, bearing, distance):
    lat1 = math.radians(lat)
    lon1 = math.radians(lon)

    dByR = distance / 1000 / EarthRadius

    lat2 = math.asin(
        math.sin(lat1) * math.cos(dByR) +
        math.cos(lat1) * math.sin(dByR) * math.cos(bearing)
    )
    lon2 = lon1 + math.atan2(
        math.sin(bearing) * math.sin(dByR) * math.cos(lat1),
        math.cos(dByR) - math.sin(lat1) * math.sin(lat2)
    )
    return math.degrees(lat2), math.degrees(lon2)


def haversine(wgs84_p1, wgs84_p2):
    lat1, lon1, lat2, lon2 = map(
        np.radians, [wgs84_p1.lat, wgs84_p1.lon, wgs84_p2.lat, wgs84_p2.lon]
    )
    x = (lon2 - lon1) * np.cos(0.5 * (lat2 + lat1))
    y = lat2 - lat1
    km = EarthRadius * np.sqrt(x * x + y * y)
    return km


def posFromLonLat(lon: float, lat: float, zoom: int, tileSize: int):
    """
      Position in scene coordinate of the WGS84 coordinates.
      Convert from WGS84 reference system to scene reference system.
      """
    tx = lon + 180.0
    tx /= 360.0
    ty = (1.0 - log(tan(lat * Deg2Rad) + 1.0 / cos(lat * Deg2Rad)) / PI) / 2.0
    zn = (1 << zoom) * float(tileSize)
    tx *= zn
    ty *= zn

    return tx, ty


def _posFromLonLatArray(lon: float, lat: float, zoom: int, tileSize: int):
    # Optimized implementation of posFromLonLat() function for numpy arrays
    tx = lon + 180.0
    tx /= 360.0

    tmp = lat * Deg2Rad
    ty = cos(tmp)

    np.divide(1.0, ty, out=ty)
    tan(tmp, out=tmp)

    ty += tmp

    log(ty, out=ty)

    ty /= PI

    np.subtract(1.0, ty, out=ty)

    ty /= 2.0
    zn = (1 << zoom) * float(tileSize)
    tx *= zn
    ty *= zn

    return tx, ty


def lonLatFromPos(x: float, y: float, zoom: int, tileSize: int):
    """
      Position in WGS84 coordinate of the scene coordinates.
      Convert from scene reference system to WGS84 reference system.
      """
    tx = x / tileSize
    ty = y / tileSize
    zn = 1 << zoom
    lon = tx / zn * 360.0 - 180.0
    n = PI - PI2 * ty / zn
    lat = arctan(0.5 * (exp(n) - exp(-n))) / Deg2Rad

    return lon, lat


def _lonLatFromPosArray(x: float, y: float, zoom: int, tileSize: int):
    # Optimized implementation of posFromLonLat() function for numpy arrays
    zn = 1 << zoom

    lon = x / tileSize
    lon /= zn
    lon *= 360
    lon -= 180

    lat = y / tileSize
    lat *= -PI2 / zn
    lat += PI
    tmp = lat * -1.0

    exp(lat, out=lat)
    exp(tmp, out=tmp)

    lat -= tmp
    lat *= 0.5

    arctan(lat, out=lat)

    lat /= Deg2Rad

    return lon, lat


def get_elevation_from_rgb(r: int, g: int, b: int) -> float:
    return -10000 + ((r * 256 * 256 + g * 256 + b) * 0.1)
