
def calculate_biodiversity(field):
    rating = 0
    value = 1

    for y in range(0, len(field)):
        for x in range(0, len(field[0])):
            if field[y][x] == '#':
                rating += value
            value *= 2

    return rating


def update_field(field):
    new_field = []

    for y in range(0, len(field)):
        new_field.append("")

        for x in range(0, len(field[0])):
            neighbours = 0
            if x > 0 and field[y][x-1] == '#':
                neighbours += 1
            if y > 0 and field[y-1][x] == '#':
                neighbours += 1
            if x < len(field[0])-1 and field[y][x+1] == '#':
                neighbours += 1
            if y < len(field)-1 and field[y+1][x] == '#':
                neighbours += 1

            cell = field[y][x]
            if field[y][x] == '#':
                if neighbours != 1:
                    cell = '.'
            else:
                if neighbours == 1 or neighbours == 2:
                    cell = '#'
            new_field[y] += cell

    return new_field


def main():
    field = [line.strip() for line in open("Day24.txt")]

    rating = calculate_biodiversity(field)
    rating_history = [rating]

    while True:
        field = update_field(field)
        rating = calculate_biodiversity(field)
        if rating in rating_history:
            print(rating)
            break
        else:
            rating_history.append(rating)


main()
