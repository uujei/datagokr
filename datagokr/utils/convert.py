from math import *

RE = 6371.00877
GRID = 5
SLAT1 = 30
SLAT2 = 60
OLON = 126
OLAT = 38
XO = 43
YO = 136

DEGRAD = pi / 180
RADDEG = 180 / pi

re = RE / GRID
slat1 = SLAT1 * DEGRAD
slat2 = SLAT2 * DEGRAD
olon = OLON * DEGRAD
olat = OLAT * DEGRAD

sn = tan(pi * 0.25 + slat2 * 0.5) / tan(pi * 0.25 + slat1 * 0.5)
sn = log10(cos(slat1) / cos(slat2)) / log10(sn)
sf = tan(pi * 0.25 + slat1 * 0.5)
sf = pow(sf, sn) * cos(slat1) / sn
ro = tan(pi * 0.25 + olat * 0.5)
ro = re * sf / pow(ro, sn)

# convert longitude, latitude to (x, y)
def lonlat_to_xy(lon: float, lat: float):
    ra = tan(pi * 0.25 + (lat) * DEGRAD * 0.5)
    ra = re * sf / pow(ra, sn)
    theta = lon * DEGRAD - olon
    if theta > pi:
        theta -= 2.0 * pi
    if theta < -pi:
        theta += 2.0 * pi
    theta *= sn
    nx = floor(ra * sin(theta) + XO + 0.5)
    ny = floor(ro - ra * cos(theta) + YO + 0.5)

    return nx, ny


# convert (x, y) to longitude, latitude
def xy_to_lonlat(x, y):
    xn = x - XO - 1
    yn = ro - y + YO + 1
    ra = sqrt(xn * xn + yn * yn)
    if sn < 0:
        ra = -ra
    alat = pow((re * sf / ra), (1 / sn))
    alat = 2 * atan(alat) - pi / 2
    if fabs(xn) <= 0:
        theta = 0
    else:
        if fabs(yn) <= 0:
            theta = pi / 2
            if xn < 0:
                theta = -theta
        else:
            theta = atan2(xn, yn)
    alon = theta / sn + olon
    lat = alat * RADDEG
    lon = alon * RADDEG

    return lon, lat
