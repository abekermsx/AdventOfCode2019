from math import gcd


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


def count_visible(asteroids, asteroid):
    visible_count = 0

    for target in asteroids:
        if target == asteroid:
            continue

        location = asteroid

        x_distance = target[0] - asteroid[0]
        y_distance = target[1] - asteroid[1]

        x_movement = x_distance // gcd(x_distance, y_distance)
        y_movement = y_distance // gcd(x_distance, y_distance)

        while True:
            location = (location[0] + x_movement, location[1] + y_movement)

            if location in asteroids:
                if location == target:
                    visible_count += 1
                break

    return visible_count


def main():
    asteroids = get_asteroids()

    for asteroid in asteroids.keys():
        asteroids[asteroid] = count_visible(asteroids, asteroid)

    highest = max(asteroids, key=asteroids.get)

    print(asteroids[highest])


main()
