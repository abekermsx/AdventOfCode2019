import itertools
from enum import Enum


class ProcessorState(Enum):
    IDLE = 0
    RUNNING = 1
    AWAITING = 2
    STOPPED = 3


class Computer:
    def __init__(self, data):
        self.memory = data
        self.pc = 0
        self.input = []
        self.output = []
        self.state = ProcessorState.IDLE

    def get_value(self, position, mode):
        if mode == 0:
            return self.memory[self.memory[position]]
        else:
            return self.memory[position]

    def add_input(self, data):
        self.input.append(data)

    def has_output(self):
        return len(self.output) > 0

    def get_output(self):
        return self.output.pop(0)

    def run(self):
        self.state = ProcessorState.RUNNING

        while True:
            opcode = self.memory[self.pc] % 100
            if opcode == 99:
                self.state = ProcessorState.STOPPED
                break

            mode1 = (self.memory[self.pc]//100) % 10
            value1 = self.get_value(self.pc + 1, mode1)

            if opcode == 3:
                if len(self.input) == 0:
                    self.state = ProcessorState.AWAITING
                    break

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
    amplifiers = []

    for phase in phases:
        computer = Computer(list(map(int, [line.rstrip().split(',') for line in open('Day7.txt')][0])))
        computer.add_input(phase)
        computer.run()
        amplifiers.append(computer)

    amplifiers[0].add_input(0)
    amplifiers[0].run()

    while amplifiers[4].state != ProcessorState.STOPPED:
        for i in range(0, 5):
            if amplifiers[i].state == ProcessorState.STOPPED:
                continue

            source_amplifier = 4 if i == 0 else i - 1
            if amplifiers[source_amplifier].has_output():
                amplifiers[i].add_input(amplifiers[source_amplifier].get_output())
                amplifiers[i].run()

    return amplifiers[4].get_output()


def main():
    max_signal = 0
    possible_phases = list(itertools.permutations([5, 6, 7, 8, 9]))

    for phases in possible_phases:
        max_signal = max(max_signal, get_result(phases))

    print(max_signal)


main()
