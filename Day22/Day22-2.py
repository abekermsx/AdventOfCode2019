
# TODO:
# - reduce all shuffling instructions to one formula in the form of (a*x+b) mod m, where x is the number of the card we want to track and m is the length of the deck
# - create an efficient formula for performing the formula above billions of times (power sums?)
# - create the inverse of the formula above to determine which card ends up at a specific location


def shuffle(position, length, instructions):
    for instruction in instructions:
        if instruction == "deal into new stack":
            position = ((position+1) * -1)
        else:
            s = instruction.split(" ")
            v = int(s[-1])
            if s[0] == "deal":
                position = (position*v)
            else:
                position = (position-v)

    return position % length


dealing_instructions = [line.strip() for line in open("Day22.txt")]
print(shuffle(2019, 10007, dealing_instructions))
