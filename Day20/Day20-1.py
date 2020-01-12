import numpy


def mark_portals(area):
    width, height = area.shape
    portals = {}

    for y in range(0, height):
        for x in range(0, width):
            if area[x, y] is None:
                continue

            if not ('A' <= area[x, y][0] <= 'Z'):
                continue

            if 'A' <= area[x, y+1][0] <= 'Z':
                # vertical portal
                portal = area[x, y][0] + area[x, y+1][0]
                if portal not in portals:
                    portals[portal] = []

                if area[x, y-1][0] == '.':
                    area[x, y] = (portal, None)
                    area[x, y+1] = ('#', None)
                    portals[portal].append(((x, y), (x, y-1)))
                else:
                    area[x, y] = ('#', None)
                    area[x, y+1] = (portal, None)
                    portals[portal].append(((x, y+1), (x, y+2)))
            elif 'A' <= area[x+1, y][0] <= 'Z':
                # horizontal portal
                portal = area[x, y][0] + area[x+1, y][0]
                if portal not in portals:
                    portals[portal] = []

                if area[x-1, y][0] == '.':
                    area[x, y] = (portal, None)
                    area[x+1, y] = ('#', None)
                    portals[portal].append(((x, y), (x-1, y)))
                else:
                    area[x, y] = ('#', None)
                    area[x+1, y] = (portal, None)
                    portals[portal].append(((x+1, y), (x+2, y)))
                pass

    return portals


def load_map():
    lines = [line.rstrip() for line in open("Day20.txt")]
    width = max([len(line) for line in lines])
    height = len(lines)

    area = numpy.empty([width, height], dtype=tuple)

    for y in range(0, height):
        for x in range(0, width):
            area[x, y] = ('#', None)

    for y in range(0, height):
        for x in range(0, len(lines[y])):
            if lines[y][x] != ' ':
                area[x, y] = (lines[y][x], None)

    return area


def traverse_map(area, portal, portals):
    steps = 0

    location = portals[portal][0][0]
    x, y = location[0], location[1]
    area[x, y] = ('#', steps)

    location = portals[portal][0][1]
    x, y = location[0], location[1]
    area[x, y] = ('#', steps)

    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    positions = [(x, y)]

    start = 0
    end = 1

    while start < end:
        steps += 1

        for position in positions[start:end]:
            for direction in directions:
                new_location = (position[0]+direction[0], position[1]+direction[1])
                x, y = new_location
                if area[x, y][0] == 'ZZ':
                    return steps-1

                if area[x, y][0] != '#':
                    if area[x, y][0] == '.':
                        area[x, y] = ('#', steps)
                    else:
                        portal = portals[area[x, y][0]][0]
                        if portal[0] == new_location:
                            portal = portals[area[x, y][0]][1]
                        new_location = portal[1]
                        x, y = new_location
                        area[x, y] = ('#', steps)

                    positions.append(new_location)

        start = end
        end = len(positions)

    return None


def main():
    area = load_map()
    portals = mark_portals(area)
    print(traverse_map(area, 'AA', portals))


main()
