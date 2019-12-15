from math import atan2, gcd, pi
from collections import defaultdict


def asteroid_coords(field):
    asteroids = []
    for y in range(len(field)):
        for x in range(len(field[y])):
            if field[y][x] == '#':
                asteroids.append((x, y))
    return asteroids


def dist(coord):
    x, y = coord
    return -((x ** 2) + (y ** 2)) ** 0.5


def angle(slope):
    y, x = slope
    # shift by pi / 2
    return ((atan2(y, x) + (pi / 2)) % (2 * pi))


def flat_zip(lsts):
    # zip multiple differently sized lists
    zipped = []
    j = max(map(len, lsts))
    for i in range(j):
        for lst in lsts:
            if i < len(lst):
                zipped.append(lst[i])
    return zipped


def num_visible(station, asteroids):
    visible = set()
    x, y = station
    for ax, ay in asteroids:
        dx = ax - x
        dy = ay - y
        d = gcd(dx, dy)
        if d != 0:
            slope = (dy // d, dx // d)
            visible.add((slope))
    return len(visible)


def sort_asteroids(station, asteroids):
    slopes = defaultdict(list)
    x, y = station
    for ax, ay in asteroids:
        dx = ax - x
        dy = ay - y
        d = gcd(dx, dy)
        if d != 0:
            slope = (dy // d, dx // d)
            slopes[slope].append((ax, ay))
            slopes[slope].sort(key=dist)
    sorted_slopes = sorted(slopes.keys(), key=angle)
    sorted_asteroids = [slopes[k] for k in sorted_slopes]
    return flat_zip(sorted_asteroids)


with open("input.txt") as f:
    field = [list(line.rstrip("\n")) for line in f]
    asteroids = asteroid_coords(field)

    # part 1
    max_asteroids, max_station = max(
        [(num_visible(station, asteroids), station) for station in asteroids])
    print(max_asteroids)

    # part 2
    sorted_asteroids = sort_asteroids(max_station, asteroids)
    ax, ay = sorted_asteroids[200 - 1]
    print(ax * 100 + ay)
