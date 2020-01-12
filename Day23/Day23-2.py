from enum import Enum


class ProcessorState(Enum):
    IDLE = 0
    RUNNING = 1
    AWAITING = 2


class Mode(Enum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


class Opcode(Enum):
    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    ADJUST_RELATIVE_BASE = 9
    STOP = 99


class Computer:
    def __init__(self, data):
        self.state = ProcessorState.IDLE
        self.memory = data
        self.input = []
        self.output = []
        self.pc = 0
        self.relative_base = 0

    def adjust_memory(self, address):
        if len(self.memory) > address:
            return

        self.memory.extend([0 for _ in range(0, address-len(self.memory)+1)])

        return

    def get_address(self, position, mode=Mode.IMMEDIATE):
        if mode == Mode.POSITION:
            address = self.read_memory(position)
        elif mode == Mode.IMMEDIATE:
            address = position
        else:  # mode == Mode.RELATIVE
            address = self.relative_base + self.read_memory(position)

        return address

    def read_memory(self, address):
        self.adjust_memory(address)
        return self.memory[address]

    def get_parameter(self, position, mode=Mode.IMMEDIATE):
        address = self.get_address(position, mode)
        return self.read_memory(address)

    def write_memory(self, position, value, mode=Mode.IMMEDIATE):
        address = self.get_address(position, mode)
        self.adjust_memory(address)
        self.memory[address] = value

    def add_input(self, data):
        self.input.append(data)

    def has_output(self):
        return len(self.output) > 0

    def get_output(self):
        return self.output.pop(0)

    def run(self):
        self.state = ProcessorState.RUNNING

        while True:
            byte = self.read_memory(self.pc)

            opcode = Opcode(byte % 100)
            if opcode == Opcode.STOP:
                self.state = ProcessorState.IDLE
                break

            mode1 = Mode((byte // 100) % 10)
            mode2 = Mode((byte // 1000) % 10)
            mode3 = Mode((byte // 10000) % 10)

            parameter1 = self.get_parameter(self.pc + 1, mode1)
            parameter2 = self.get_parameter(self.pc + 2, mode2)
            parameter3 = self.get_address(self.pc + 3, mode3)

            if opcode == Opcode.INPUT:
                if len(self.input) == 0:
                    self.state = ProcessorState.AWAITING
                    break

                self.write_memory(self.pc + 1, self.input.pop(0), mode1)
                self.pc += 2
            elif opcode == Opcode.OUTPUT:
                self.output.append(parameter1)
                self.pc += 2
            elif opcode == Opcode.ADD:
                self.write_memory(parameter3, parameter1 + parameter2)
                self.pc += 4
            elif opcode == Opcode.MULTIPLY:
                self.write_memory(parameter3, parameter1 * parameter2)
                self.pc += 4
            elif opcode == Opcode.JUMP_IF_TRUE:
                self.pc = parameter2 if parameter1 != 0 else self.pc + 3
            elif opcode == Opcode.JUMP_IF_FALSE:
                self.pc = parameter2 if parameter1 == 0 else self.pc + 3
            elif opcode == Opcode.LESS_THAN:
                self.write_memory(parameter3, 1 if parameter1 < parameter2 else 0)
                self.pc += 4
            elif opcode == Opcode.EQUALS:
                self.write_memory(parameter3, 1 if parameter1 == parameter2 else 0)
                self.pc += 4
            elif opcode == Opcode.ADJUST_RELATIVE_BASE:
                self.relative_base += self.get_parameter(self.pc + 1, mode1)
                self.pc += 2


def main():
    network = []
    incoming = []
    program = list(map(int, [line.rstrip().split(',') for line in open('Day23.txt')][0]))

    for i in range(0, 50):
        network.append(Computer(program.copy()))
        incoming.append([])
        network[i].add_input(i)
        network[i].run()

    has_nat = False
    nat_x, nat_y = 0, 0
    nat_last_y = None

    while True:
        for i in range(0, 50):
            if len(incoming[i]) > 0:
                network[i].add_input(incoming[i].pop(0))
                network[i].add_input(incoming[i].pop(0))
                network[i].run()
            else:
                network[i].add_input(-1)
                network[i].run()
            if network[i].has_output():
                address = network[i].get_output()
                x = network[i].get_output()
                y = network[i].get_output()

                if address == 255:
                    nat_x = x
                    nat_y = y
                    has_nat = True
                else:
                    incoming[address].append(x)
                    incoming[address].append(y)

            if has_nat:
                if all([len(i) == 0 for i in incoming]):
                    if nat_y == nat_last_y:
                        print(y)
                        return

                    network[0].add_input(nat_x)
                    network[0].add_input(nat_y)
                    network[0].run()
                    has_nat = False
                    nat_last_y = nat_y


main()
