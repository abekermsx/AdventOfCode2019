
def update_velocity(velocity, moon, neighbour, axis):
    result = list(velocity)
    result[axis] += max(min(neighbour[axis]-moon[axis], 1), -1)
    return tuple(result)


def apply_gravity(moons):
    result = {}

    for moon in moons:
        velocity = moons[moon]

        for neighbour in moons:
            if moon == neighbour:
                continue

            velocity = update_velocity(velocity, moon, neighbour, 0)
            velocity = update_velocity(velocity, moon, neighbour, 1)
            velocity = update_velocity(velocity, moon, neighbour, 2)

        result[moon] = velocity

    return result


def apply_velocity(moons):
    result = {}

    for moon in moons:
        location = list(moon)
        location[0] += moons[moon][0]
        location[1] += moons[moon][1]
        location[2] += moons[moon][2]
        result[tuple(location)] = moons[moon]

    return result


def main():
    moons = {(-9, -1, -1): (0, 0, 0), (2, 9, 5): (0, 0, 0), (10, 18, -12): (0, 0, 0), (-6, 15, -7): (0, 0, 0)}

    for _ in range(0, 1000):
        moons = apply_gravity(moons)
        moons = apply_velocity(moons)

    return sum([sum(abs(m) for m in list(moon)) * sum(abs(v) for v in list(moons[moon])) for moon in moons])


print(main())
