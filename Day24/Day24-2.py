
def count_bugs(fields, level, x, y, dx=0, dy=0):
    if level not in fields:
        return 0

    if dx == 0 and dy == 0:
        return 1 if fields[level][y][x] == '#' else 0

    if x+dx < 0:
        return count_bugs(fields, level - 1, 1, 2)

    if y+dy < 0:
        return count_bugs(fields, level - 1, 2, 1)

    if x+dx == 5:
        return count_bugs(fields, level - 1, 3, 2)

    if y+dy == 5:
        return count_bugs(fields, level - 1, 2, 3)

    if fields[level][y + dy][x + dx] == '?':
        # L
        if x == 1 and y == 2:
            return sum([count_bugs(fields, level + 1, 0, yy) for yy in range(5)])

        # N
        if x == 3 and y == 2:
            return sum([count_bugs(fields, level + 1, 4, yy) for yy in range(5)])

        # H
        if y == 1 and x == 2:
            return sum([count_bugs(fields, level + 1, xx, 0) for xx in range(5)])

        # R
        if y == 3 and x == 2:
            return sum([count_bugs(fields, level + 1, xx, 4) for xx in range(5)])

    return 1 if fields[level][y+dy][x+dx] == '#' else 0


def update_field(fields, level):
    field = fields[level]
    new_field = []

    for y in range(len(field)):
        new_field.append("")

        for x in range(len(field[0])):
            cell = field[y][x]

            if cell == '?':
                new_field[y] += "?"
                continue

            neighbours = count_bugs(fields, level, x, y, 1, 0)
            neighbours += count_bugs(fields, level, x, y, -1, 0)
            neighbours += count_bugs(fields, level, x, y, 0, 1)
            neighbours += count_bugs(fields, level, x, y, 0, -1)

            if cell == '#':
                if neighbours != 1:
                    cell = '.'
            else:
                if neighbours == 1 or neighbours == 2:
                    cell = '#'

            new_field[y] += cell

    return new_field


def count_all_bugs(fields):
    bugs = 0

    for field in fields.values():
        for y in range(5):
            for x in range(5):
                if field[y][x] == '#':
                    bugs += 1

    return bugs


def main():
    field = [line.strip() for line in open("Day24.txt")]
    field[2] = field[2][:2] + '?' + field[2][3:]
    fields = {0: field}

    empty_field = [
        ".....",
        ".....",
        "..?..",
        ".....",
        "....."
    ]

    for _ in range(200):
        new_fields = {}
        for i in range(min(fields.keys())-1, max(fields.keys())+2):

            if i not in fields.keys():
                fields[i] = empty_field.copy()

                new_field = update_field(fields, i)

                if empty_field != new_field:
                    new_fields[i] = new_field
            else:
                new_fields[i] = update_field(fields, i)

        fields = new_fields

    print(count_all_bugs(fields))


main()
