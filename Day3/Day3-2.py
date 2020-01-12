
class WireMap:
    def __init__(self):
        self.wire_map = {}
        self.x = 0
        self.y = 0
        self.step_counter = 0

    def move(self, steps, x_dir, y_dir):
        while steps > 0:
            self.x += x_dir
            self.y += y_dir
            self.step_counter += 1
            self.wire_map[(self.x, self.y)] = self.step_counter
            steps -= 1

    def move_up(self, steps):
        return self.move(steps, 0, -1)

    def move_down(self, steps):
        return self.move(steps, 0, 1)

    def move_left(self, steps):
        return self.move(steps, -1, 0)

    def move_right(self, steps):
        return self.move(steps, 1, 0)

    def mark_wires(self, movements):
        for command in movements:
            direction = command[0]
            s = int(command[1:])

            if direction == "R":
                self.move_right(s)
            elif direction == "L":
                self.move_left(s)
            elif direction == "U":
                self.move_up(s)
            else:
                self.move_down(s)


maps = [line.strip().split(",") for line in open("Day3.txt")]

map1 = WireMap()
map1.mark_wires(maps[0])

map2 = WireMap()
map2.mark_wires(maps[1])

keys1 = set(map1.wire_map.keys())
keys2 = set(map2.wire_map.keys())
keys_intersection = keys1 & keys2

result = []
for key in keys_intersection:
    result.append(map1.wire_map[key] + map2.wire_map[key])

print(min(result))
