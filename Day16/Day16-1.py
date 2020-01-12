
def transform(signal, pattern):
    result = []
    skip = 0

    for step in range(1, len(signal)+1):
        pattern_index = (1 + skip) // step
        repeat = step - (1 + skip) % step

        cumsum = 0

        pattern_v = pattern[pattern_index]
        for value in signal[skip:]:
            cumsum += value * pattern_v
            repeat -= 1
            if repeat == 0:
                repeat = step
                pattern_index += 1
                if pattern_index == len(pattern):
                    pattern_index = 0
                pattern_v = pattern[pattern_index]

        result.append(abs(cumsum) % 10)
        skip += 1

    return result


def main():
    base_pattern = [0, 1, 0, -1]
    signal = [int(v) for v in open("Day16.txt").read()]

    for _ in range(0, 100):
        signal = transform(signal, base_pattern)

    print(signal[0:8])


main()
