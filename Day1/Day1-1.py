
def fuel_requirement(mass):
    return int(mass) // 3 - 2


with open('Day1.txt') as file:
    totalFuel = sum(map(fuel_requirement, file.readlines()))

print(totalFuel)
