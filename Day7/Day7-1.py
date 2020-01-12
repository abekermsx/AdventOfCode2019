import itertools


class Computer:
    def __init__(self, data):
        self.memory = data
        self.pc = 0
        self.input = []
        self.output = []

    def get_value(self, position, mode):
        if mode == 0:
            return self.memory[self.memory[position]]
        else:
            return self.memory[position]

    def set_input(self, data):
        self.input = data

    def get_output(self):
        return self.output

    def run(self):
        while True:
            opcode = self.memory[self.pc] % 100

            if opcode == 99:
                break

            mode1 = (self.memory[self.pc]//100) % 10
            value1 = self.get_value(self.pc + 1, mode1)

            if opcode == 3:
                self.memory[self.memory[self.pc+1]] = self.input.pop(0)
                self.pc += 2
            elif opcode == 4:
                self.output.append(value1)
                self.pc += 2
            else:
                mode2 = (self.memory[self.pc]//1000)
                value2 = self.get_value(self.pc + 2, mode2)

                if opcode == 1:
                    store_position = self.memory[self.pc + 3]
                    self.memory[store_position] = value1 + value2
                    self.pc += 4
                elif opcode == 2:
                    store_position = self.memory[self.pc + 3]
                    self.memory[store_position] = value1 * value2
                    self.pc += 4
                elif opcode == 5:
                    if value1 != 0:
                        self.pc = value2
                    else:
                        self.pc += 3
                elif opcode == 6:
                    if value1 == 0:
                        self.pc = value2
                    else:
                        self.pc += 3
                elif opcode == 7:
                    store_position = self.memory[self.pc + 3]
                    if value1 < value2:
                        self.memory[store_position] = 1
                    else:
                        self.memory[store_position] = 0
                    self.pc += 4
                elif opcode == 8:
                    store_position = self.memory[self.pc + 3]
                    if value1 == value2:
                        self.memory[store_position] = 1
                    else:
                        self.memory[store_position] = 0
                    self.pc += 4


def get_result(phases):
    last_output = 0
    for phase in phases:
        computer = Computer(list(map(int, [line.rstrip().split(',') for line in open('Day7.txt')][0])))
        computer.set_input([phase, last_output])
        computer.run()
        last_output = computer.get_output()[0]

    return last_output


def main():
    max_signal = 0
    possible_phases = list(itertools.permutations([0, 1, 2, 3, 4]))

    for phases in possible_phases:
        max_signal = max(max_signal, get_result(phases))

    print(max_signal)


main()
