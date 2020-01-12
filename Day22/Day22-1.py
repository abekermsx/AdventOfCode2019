
def create_deck(size):
    return [i for i in range(0, size)]


def deal_into_new_stack(deck):
    deck = deck.copy()
    deck.reverse()
    return deck


def cut_n_cards(deck, n):
    return deck[n:] + deck[0:n]


def deal_with_increment_n(deck, n):
    new_deck = deck.copy()
    i = 0
    for card in deck:
        new_deck[i] = card
        i += n
        i %= len(deck)

    return new_deck


def shuffle(deck, instructions):
    deck = deck.copy()

    for instruction in instructions:
        if instruction == "deal into new stack":
            deck = deal_into_new_stack(deck)
        else:
            s = instruction.split(" ")
            if s[0] == "deal":
                deck = deal_with_increment_n(deck, int(s[-1]))
            else:
                deck = cut_n_cards(deck, int(s[-1]))

    return deck


def main(size, instructions, repeat=1):
    deck = create_deck(size)

    for i in range(0, repeat):
        deck = shuffle(deck, instructions)

    return deck


dealing_instructions = [line.strip() for line in open("Day22.txt")]
result = main(10007, dealing_instructions)
print(result.index(2019))
