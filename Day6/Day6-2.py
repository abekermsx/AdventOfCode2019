
def find_path(start, end, links, counter):
    items = [item for item in links if item[0] == start]

    for item in items:
        links.remove(item)
        links.remove((item[1], item[0]))
        if item[1] == end:
            print(counter-1)
        else:
            find_path(item[1], end, links, counter + 1)


def main():
    links = []
    data = [line.rstrip().split(')') for line in open('Day6.txt')]

    for planet, moon in data:
        links.append((planet, moon))
        links.append((moon, planet))

    find_path("YOU", "SAN", links, 0)


main()
