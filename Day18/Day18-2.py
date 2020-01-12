import cProfile
import numpy


def get_character_at_position(area, location):
    return area[(location[1], location[0])][0]


def set_character_at_position(area, location, c):
    area[(location[1], location[0])] = (c, area[(location[1], location[0])][1])


def can_move_to_position(area, location):
    return get_character_at_position(area, location) != '#'


def find_paths(area, key_name, keys):
    area = area.copy()

    location = keys[key_name][0]

    x, y = location[0], location[1]

    area[y, x] = ('@', location)

    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    positions = [(x, y)]

    start = 0
    end = 1

    while start < end:
        for position in positions[start:end]:
            for direction in directions:
                new_location = (position[0]+direction[0], position[1]+direction[1])

                x = new_location[0]
                y = new_location[1]

                if area[y, x][1] is not None or not can_move_to_position(area, new_location):
                    continue

                positions.append(new_location)
                area[y, x] = (area[y, x][0], position)

        start = end
        end = len(positions)

    for key in keys.items():
        if key[0] == key_name:
            continue

        position = key[1][0]
        x, y = position[0], position[1]

        if area[y, x][1] is None:
            continue

        path = []
        required_keys = []
        while position != location:
            path.append(position)
            x, y = position[0], position[1]
            position = area[y, x][1]
            c = get_character_at_position(area, position)
            if 'A' <= c <= 'Z':
                required_keys.append(c.lower())

        path.reverse()
        keys[key_name][1].append((key[0], path, required_keys))

    keys[key_name][1].sort(key=lambda v: len(v[1]))


def get_item_locations(area):
    keys = {}

    for position, c in numpy.ndenumerate(area):
        if c[0] == '@' or 'a' <= c[0] <= 'z' or '1' <= c[0] <= '4':
            keys[c[0]] = ((position[1], position[0]), [])

    return keys


best = None
best_steps = []


def find_routes_dfs(state, keys):
    global best, best_steps

    collected_keys = state["collected_keys"]

    if best is not None:
        if len(collected_keys) > 5:
            if state["steps"] + len(keys[state["droids"][0]][1][0][1]) // 2 > best_steps[len(collected_keys)]:
                return

    for i in range(len(state["droids"])):
        for next_key in keys[state["droids"][i]][1]:
            if next_key[0] in collected_keys:
                continue
            if not all(elem in collected_keys for elem in next_key[2]):
                continue

            new_collected_keys = collected_keys + next_key[0]
            new_steps = state["steps"] + len(next_key[1])
            new_best_steps = state["best_steps"] + [new_steps]

            if len(new_collected_keys) == len(keys):
                if best is None or new_steps < best:
                    best = new_steps
                    best_steps = new_best_steps
                    print(best)
                    return
            else:
                new_state = {
                    "droids": state["droids"].copy(),
                    "steps": new_steps,
                    "best_steps": new_best_steps,
                    "collected_keys": new_collected_keys,
                }
                new_state["droids"][i] = next_key[0]
                find_routes_dfs(new_state, keys)

    return


def main():
    # area = [
    #     "#################",
    #     "#i.G..c...e..H.p#",
    #     "########.########",
    #     "#j.A..b...f..D.o#",
    #     "########@########",
    #     "#k.E..a...g..B.n#",
    #     "########.########",
    #     "#l.F..d...h..C.m#",
    #     "#################"
    # ]

    # area = [
    #     "########################",
    #     "#@..............ac.GI.b#",
    #     "###d#e#f################",
    #     "###A#B#C################",
    #     "###g#h#i################",
    #     "########################"
    # ]

    # area = [
    #     "########################",
    #     "#...............b.C.D.f#",
    #     "#.######################",
    #     "#.....@.a.B.c.d.A.e.F.g#",
    #     "########################"
    # ]

    area = [line.strip() for line in open("Day18.txt")]

    xx = 0
    yy = 0

    arr = numpy.empty((len(area), len(area[0])), dtype=tuple)
    for y in range(0, len(area)):
        for x in range(0, len(area[0])):
            arr[y, x] = (area[y][x], None)
            if area[y][x] == '@':
                xx = x
                yy = y

    arr[yy-1, xx] = ('#', None)
    arr[yy, xx] = ('#', None)
    arr[yy+1, xx] = ('#', None)
    arr[yy, xx-1] = ('#', None)
    arr[yy, xx+1] = ('#', None)

    arr[yy-1, xx-1] = ('1', None)
    arr[yy-1, xx+1] = ('2', None)
    arr[yy+1, xx-1] = ('3', None)
    arr[yy+1, xx+1] = ('4', None)

    keys = get_item_locations(arr)

    for key in keys.keys():
        find_paths(arr, key, keys)

    find_routes_dfs({
        "droids": ['1', '2', '3', '4'],
        "steps": 0,
        "best_steps": [0, 0, 0, 0],
        "collected_keys": '1234'
    }, keys)


cProfile.run('main()')
# main()
