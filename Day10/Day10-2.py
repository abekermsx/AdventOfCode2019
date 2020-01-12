from itertools import groupby
from math import gcd, cos, sin, sqrt, atan2


def get_asteroids():
    asteroids = {}

    rows = [line.rstrip() for line in open("Day10.txt")]
    y = 0
    for row in rows:
        for x in range(0, len(row)):
            if row[x] == '#':
                asteroids[(x, y)] = 0

        y += 1

    return asteroids


def vaporise_asteroids(asteroids, station):
    def to_polar(x, y):
        theta = atan2(x, y)
        rho = sqrt(x**2 + y**2)
        return theta, rho

    def to_cartesian(polar):
        theta, rho = polar
        oy, ox = round(rho * cos(theta)), round(rho * sin(theta))
        return sx + ox, sy + oy

    asteroids = (a for a in asteroids if a != station)
    sx, sy = station

    asteroids_polar = sorted((to_polar(ax - sx, ay - sy) for ax, ay in asteroids), reverse=True)
    asteroids_grouped = list((k, list(v)) for k, v in groupby(asteroids_polar, lambda a: a[0]))

    while asteroids_grouped:
        for theta, group in list(asteroids_grouped):
            yield to_cartesian(group[-1])
            if len(group) == 1:
                asteroids_grouped.remove((theta, group))
            else:
                del group[0]


def main():
    asteroids = get_asteroids()
    station = (14, 17)
    zap = vaporise_asteroids(asteroids, station)
    x, y = list(zap)[199]
    return x * 100 + y


print(main())
