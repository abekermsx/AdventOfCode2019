
def count_digits(image, digit):
    count = 0

    for pixel in image:
        if pixel == digit:
            count += 1

    return count


def get_layers(image, width, height):
    size = width * height

    layers = []
    while len(image) > 0:
        layers.append(image[0:size])
        image = image[size:]

    return layers


def main(image, width, height):
    layers = get_layers(image, width, height)

    results = []
    for layer in layers:
        results.append((count_digits(layer, '0'), count_digits(layer, '1')*count_digits(layer, '2')))

    results.sort(key=lambda tup: tup[0])

    return results[0][1]


data = [line for line in open('Day8.txt')][0]

print(main(data, 25, 6))
