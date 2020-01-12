from math import ceil


def convert(value):
    return int(value[0]), value[1]


class Factory:
    def __init__(self):
        self.stock = {}
        self.manufactured = {}
        self.recipes = {}

    def load_recipes(self, file):
        recipes = [line.strip() for line in open(file)]

        self.stock["ORE"] = 0
        self.manufactured["ORE"] = 0
        self.recipes["ORE"] = [1, []]

        for recipe in recipes:
            amount, product = convert(recipe.split("=>")[1].strip().split(" "))
            ingredients = recipe.split("=>")[0].strip().split(",")

            self.recipes[product] = (amount, [convert(ingredient.strip().split(" ")) for ingredient in ingredients])
            self.stock[product] = 0
            self.manufactured[product] = 0

    def manufacture(self, product, amount):
        if self.stock[product] >= amount:
            self.stock[product] -= amount
            return

        batches = int(ceil((amount-self.stock[product])/self.recipes[product][0]))

        for ingredient in self.recipes[product][1]:
            self.manufacture(ingredient[1], ingredient[0] * batches)

        self.manufactured[product] += batches * self.recipes[product][0]
        self.stock[product] += batches * self.recipes[product][0]

        self.stock[product] -= amount


def main():
    factory = Factory()
    factory.load_recipes("Day14.txt")
    factory.manufacture("FUEL", 1)

    print(factory.manufactured["ORE"])


main()
