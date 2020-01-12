
def transform(signal):
    result = []
    cumsum = 0

    for i in range(len(signal)-1, -1, -1):
        cumsum += signal[i]
        result.append(cumsum % 10)

    return list(reversed(result))


def main():
    text = open("Day16.txt").read()
    data = [int(v) for v in text]
    skip = int(text[0:7])

    signal = []
    for _ in range(0, 10000):
        signal += data

    signal = signal[skip:]
    for _ in range(0, 100):
        signal = transform(signal)

    print(signal[0:8])


main()
