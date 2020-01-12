from enum import Enum
from copy import deepcopy


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


def get_view(computer):
    lines = []
    line = ""

    while computer.has_output():
        c = computer.get_output()
        if c == 10:
            lines.append(line)
            line = ""
        else:
            line += chr(c)

    return lines[:-2]


def get_droid_location(view):
    for y, line in enumerate(view):
        for x, c in enumerate(line):
            if c == '^':
                return x, y

    return None


directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

# movements that should be tested when facing specific direction
movements = [
    [3, 4],  # up
    [4, 3],  # down
    [2, 1],  # left
    [1, 2],  # right
]


def get_element_at_location(view, location):
    if location[0] < 0 or location[0] >= len(view[0]):
        return None

    if location[1] < 0 or location[1] >= len(view):
        return None

    return view[location[1]][location[0]]


def can_turn_in_direction(view, location, direction, turn):
    turn = 0 if turn == 'L' else 1
    movement = movements[direction-1][turn]
    location = (location[0] + directions[movement-1][0], location[1] + directions[movement-1][1])

    if location[0] < 0 or location[0] == len(view[0]):
        return False

    if location[1] < 0 or location[1] == len(view):
        return False

    return view[location[1]][location[0]] == '#'


def get_new_direction(view, location, direction):
    if can_turn_in_direction(view, location, direction, 'L'):
        return 'L'

    if can_turn_in_direction(view, location, direction, 'R'):
        return 'R'

    return 'X'


# assumes droid only turns left/right when hitting a wall
def get_path(view):
    location = get_droid_location(view)
    path = []
    direction = 1

    while True:
        turn = get_new_direction(view, location, direction)

        if turn == 'X':
            break

        direction = movements[direction-1][turn == 'R']

        steps = 0
        while True:
            new_location = (location[0] + directions[direction-1][0], location[1] + directions[direction-1][1])
            if get_element_at_location(view, new_location) == '#':
                location = new_location
                steps += 1
            else:
                break

        path.append((turn, steps))

    return path


def build_function(path):
    return ",".join([move[0] + "," + str(move[1]) for move in path])


def optimize_instructions(input_state):
    if input_state["position"] == len(input_state["path"]):
        state = deepcopy(input_state)
        state["completed"] = True
        return state

    # use existing function
    if len(input_state["main"]) < 19:
        for i, f in enumerate(input_state["functions"]):
            if f == input_state["path"][input_state["position"]:input_state["position"]+len(f)]:
                state = deepcopy(input_state)
                state["main"].append(i+1)
                state["position"] += len(f)
                new_state = optimize_instructions(state)
                if new_state["completed"]:
                    return new_state

    # add to current function
    if input_state["current_function"] is not None and input_state["main"].count(input_state["current_function"] + 1) == 1:
        state = deepcopy(input_state)
        new_function = state["functions"][state["current_function"]]
        new_function.append(state["path"][state["position"]])
        if len(build_function(new_function)) <= 20:
            state["functions"][state["current_function"]] = new_function
            state["position"] += 1
            new_state = optimize_instructions(state)
            if new_state["completed"]:
                return new_state

    # create new function
    if len(input_state["functions"]) < 3 and len(input_state["main"]) < 10:
        state = deepcopy(input_state)
        state["functions"].append([state["path"][state["position"]]])
        state["main"].append(len(state["functions"]))
        state["position"] += 1
        state["current_function"] = len(state["functions"])-1
        new_state = optimize_instructions(state)
        if new_state["completed"]:
            return new_state

    return input_state


def main():
    computer = Computer(list(map(int, [line.rstrip().split(',') for line in open('Day17.txt')][0])))
    computer.memory[0] = 2
    computer.run()
    
    view = get_view(computer)

    path = get_path(view)

    state = {
        "path": path,
        "position": 0,
        "main": [],
        "functions": [],
        "current_function": None,
        "completed": False
    }

    state = optimize_instructions(state)

    for c in ",".join([chr(65+c-1) for c in state["main"]]):
        computer.add_input(ord(c))
    computer.add_input(10)

    for f in state["functions"]:
        for c in build_function(f):
            computer.add_input(ord(c))
        computer.add_input(10)

    computer.add_input('n')
    computer.add_input(10)
    computer.run()

    while computer.has_output():
        v = computer.get_output()
        if not computer.has_output():
            print(v)


main()
