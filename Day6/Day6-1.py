
def main():
    data = [line.rstrip().split(')') for line in open('Day6.txt')]
    orbiters = dict((moon, planet) for planet, moon in data)

    connections = 0
    for orbiter in orbiters:
        o = orbiter
        while o is not None:
            o = orbiters.get(o)
            if o is not None:
                connections += 1

    print(connections)


main()
