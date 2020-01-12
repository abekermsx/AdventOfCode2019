
def get_layers(image, width, height):
    size = width * height

    layers = []
    while len(image) > 0:
        layers.append(image[0:size])
        image = image[size:]

    return layers


def merge_layers(layers):
    image = layers.pop(0)

    for layer in layers:
        for i in range(0, len(layer)):
            if image[i] == '2':
                image = image[:i] + layer[i] + image[i+1:]

    return image


def main(image_data, width, height):
    layers = get_layers(image_data, width, height)
    image = merge_layers(layers)

    result = ""
    for row in range(0, height):
        result += image[row * width:(row+1)*width] + "\n"

    return result


data = [line for line in open('Day8.txt')][0]

print(main(data, 25, 6))
