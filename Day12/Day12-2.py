from math import gcd
from functools import reduce


def lcm(denominators):
    return reduce(lambda a, b: a*b // gcd(a, b), denominators)


def update_velocity(velocity, moon, neighbour):
    return velocity + max(min(neighbour[0]-moon[0], 1), -1)


def apply_gravity(moons):
    result = []

    for moon in moons:
        velocity = moon[1]

        for neighbour in moons:
            if moon == neighbour:
                continue

            velocity = update_velocity(velocity, moon, neighbour)

        result.append((moon[0], velocity))

    return result


def apply_velocity(moons):
    result = []

    for moon in moons:
        result.append((moon[0]+moon[1], moon[1]))

    return result


def get_steps(moons):
    original = moons.copy()
    steps = 0
    while True:
        moons = apply_gravity(moons)
        moons = apply_velocity(moons)
        steps += 1
        if moons == original:
            break

    return steps


def main():
    moons = {(-9, -1, -1): (0, 0, 0), (2, 9, 5): (0, 0, 0), (10, 18, -12): (0, 0, 0), (-6, 15, -7): (0, 0, 0)}

    steps_x = get_steps([(k[0], 0) for k in moons.keys()])
    steps_y = get_steps([(k[1], 0) for k in moons.keys()])
    steps_z = get_steps([(k[2], 0) for k in moons.keys()])

    return steps_x, steps_y, steps_z


print(lcm(list(main())))
