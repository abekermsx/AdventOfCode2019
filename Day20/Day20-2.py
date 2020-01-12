import operator
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

            portal_type = 1
            if x < 3 or y < 3 or x > (width-4) or y > (height-4):
                portal_type = -1

            if 'A' <= area[x, y+1][0] <= 'Z':
                # vertical portal
                portal = area[x, y][0] + area[x, y+1][0]
                if portal not in portals:
                    portals[portal] = []

                if area[x, y-1][0] == '.':
                    area[x, y] = (portal, None)
                    area[x, y+1] = ('#', None)
                    portals[portal].append(((x, y), (x, y-1), portal_type, portal))
                else:
                    area[x, y] = ('#', None)
                    area[x, y+1] = (portal, None)
                    portals[portal].append(((x, y+1), (x, y+2), portal_type, portal))
            elif 'A' <= area[x+1, y][0] <= 'Z':
                # horizontal portal
                portal = area[x, y][0] + area[x+1, y][0]
                if portal not in portals:
                    portals[portal] = []

                if area[x-1, y][0] == '.':
                    area[x, y] = (portal, None)
                    area[x+1, y] = ('#', None)
                    portals[portal].append(((x, y), (x-1, y), portal_type, portal))
                else:
                    area[x, y] = ('#', None)
                    area[x+1, y] = (portal, None)
                    portals[portal].append(((x+1, y), (x+2, y), portal_type, portal))
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


level_down_portals = {}
level_up_portals = {}


def traverse_map(original_area, portal, portals, level, depth, steps):
    global level_down_portals, level_up_portals

    if depth > 128 or level > 32:
        return None

    area = original_area.copy()
    source_portal = portal[3]

    if source_portal not in level_down_portals:
        level_down_portals[source_portal] = []
        level_up_portals[source_portal] = []

    location = portal[0]
    x, y = location[0], location[1]
    area[x, y] = ('#', steps)

    location = portal[1]
    x, y = location[0], location[1]
    area[x, y] = ('#', steps)

    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    positions = [((x, y), 0)]

    start = 0
    end = 1
    while start < end:
        steps += 1

        for i in range(start, end):
            position = positions[i]

            for direction in directions:
                new_location = (position[0][0]+direction[0], position[0][1]+direction[1])
                x, y = new_location

                if area[x, y][0] == '#':
                    continue

                if area[x, y][0] == '.':
                    area[x, y] = ('#', steps)
                    positions.append((new_location, steps))
                    continue

                if area[x, y][0] == 'AA':
                    continue

                if level > 0:
                    if area[x, y][0] == 'ZZ':
                        continue
                else:
                    if area[x, y][0] == 'ZZ':
                        return steps-1

                    portal = portals[area[x, y][0]][0]
                    if portal[0] != new_location:
                        portal = portals[area[x, y][0]][1]
                    if portal[2] == -1:
                        continue

                portal = portals[area[x, y][0]][0]
                if portal[0] == new_location:
                    portal = portals[area[x, y][0]][1]

                if portal[2] == -1:
                    if (portal, level) in level_up_portals[source_portal]:
                        continue
                    else:
                        level_up_portals[source_portal].append((portal, level))
                else:
                    if (portal, level) in level_down_portals[source_portal]:
                        continue
                    else:
                        level_down_portals[source_portal].append((portal, level))

                result = traverse_map(original_area, portal, portals, level - portal[2], depth+1, steps)

                area[x, y] = ('#', steps)

                if portal[2] == -1:
                    level_up_portals[source_portal].remove((portal, level))
                else:
                    level_down_portals[source_portal].remove((portal, level))

                if result is not None:
                    return result

        positions.sort(key=operator.itemgetter(1))

        start = end
        end = len(positions)

    return None


def main():
    area = load_map()
    portals = mark_portals(area)
    print(traverse_map(area, portals['AA'][0], portals, 0, 0, 0))


main()
