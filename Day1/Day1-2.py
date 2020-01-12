
def fuel_required_for_mass(mass):
    return mass // 3 - 2


def fuel_required(mass):
    fuel = max(fuel_required_for_mass(mass), 0)

    if fuel > 0:
        fuel += fuel_required(fuel)

    return fuel


with open('Day1.txt') as file:
    print(sum(fuel_required(int(m)) for m in file.readlines()))
