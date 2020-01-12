
def computer(items):
    position = 0

    while True:
        opcode = items[position] % 100

        if opcode == 99:
            break
        elif opcode == 3:
            items[items[position + 1]] = int(input("Enter number:"))
            position += 2
        elif opcode == 4:
            print(items[items[position + 1]])
            position += 2
        else:
            mode1 = (items[position]//100) % 10
            mode2 = (items[position]//1000)

            if mode1 == 0:
                value1 = items[items[position + 1]]
            else:
                value1 = items[position + 1]

            if mode2 == 0:
                value2 = items[items[position + 2]]
            else:
                value2 = items[position + 2]

            store_position = items[position + 3]

            if opcode == 1:
                items[store_position] = value1 + value2
            elif opcode == 2:
                items[store_position] = value1 * value2

            position += 4


program = list(map(int, [line.rstrip().split(',') for line in open('Day5.txt')][0]))

computer(program)
