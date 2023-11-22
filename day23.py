import os, re
from random import shuffle

LINE_REGEX = re.compile("pos=< *(-*)(\d+), *(-*)(\d+), *(-*)(\d+)>, r=(-*)(\d+)")

class Box:
    def __init__(self, x_range: tuple[int, int], y_range: tuple[int, int], z_range: tuple[int, int]):
        self.x_range = x_range
        self.y_range = y_range
        self.z_range = z_range

    def is_valid(self):
        return self.x_range[0] <= self.x_range[1] and self.y_range[0] <= self.y_range[1] and self.z_range[0] <= self.z_range[1]

    def __repr__(self):
        return f"{self.x_range}, {self.y_range}, {self.z_range}"

class Nanobot:
    def __init__(self, x: int, y: int, z: int, r: int):
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.box = Box((x-r, x+r), (y-r, y+r), (z-r, z+r))

    def point_in_range(self, p: tuple[int, int, int]):
        return (abs(self.x - p[0]) + abs(self.y - p[1]) + abs(self.z - p[2])) <= self.r

    def nanobot_in_range(self, n: "Nanobot"):
        return self.point_in_range((n.x, n.y, n.z))

    def box_in_range(self, b: Box):
        # find closest point of box
        x_point = b.x_range[0] if self.x <= b.x_range[0] else b.x_range[1] if self.x >= b.x_range[1] else self.x
        y_point = b.y_range[0] if self.y <= b.y_range[0] else b.y_range[1] if self.y >= b.y_range[1] else self.y
        z_point = b.z_range[0] if self.z <= b.z_range[0] else b.z_range[1] if self.z >= b.z_range[1] else self.z

        return self.point_in_range((x_point, y_point, z_point))

    def __repr__(self):
        return f"pos=<{self.x}, {self.y}, {self.z}>, r={self.r}"

def solution_part1(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
    with open(fname, "r") as f:
        nanobots: list[Nanobot] = []
        max_range: int = -1
        max_nanobot: Nanobot | None = None
        for line in f:
            m = LINE_REGEX.match(line)
            if m:
                x = int(m.group(1) + m.group(2))
                y = int(m.group(3) + m.group(4))
                z = int(m.group(5) + m.group(6))
                r = int(m.group(7) + m.group(8))
                nanobots.append(Nanobot(x, y, z, r))
                if (r > max_range):
                    max_range = r
                    max_nanobot = nanobots[-1]
            else:
                print("NO MATCH: ", line)
        assert(max_nanobot is not None)

        result = 0
        for n in nanobots:
            if max_nanobot.nanobot_in_range(n):
                result += 1
        return result

global MAXIMUM_SEEN
global MAXIMUM_POINT

MAXIMUM_SEEN = 0
MAXIMUM_POINT = (float('inf'), float('inf'), float('inf'))

def recursive_search(box: Box, nanobots: list[Nanobot]):
    global MAXIMUM_SEEN
    global MAXIMUM_POINT
    box_size = (box.x_range[1] - box.x_range[0]) // 2
    boxes_to_check = [
        Box((box.x_range[0], box.x_range[0] + box_size), (box.y_range[0], box.y_range[0] + box_size), (box.z_range[0], box.z_range[0] + box_size)),
        Box((box.x_range[0], box.x_range[0] + box_size), (box.y_range[0], box.y_range[0] + box_size), (box.z_range[0] + box_size + 1, box.z_range[1])),
        Box((box.x_range[0], box.x_range[0] + box_size), (box.y_range[0] + box_size + 1, box.y_range[1]), (box.z_range[0], box.z_range[0] + box_size)),
        Box((box.x_range[0], box.x_range[0] + box_size), (box.y_range[0] + box_size + 1, box.y_range[1]), (box.z_range[0] + box_size + 1, box.z_range[1])),
        Box((box.x_range[0] + box_size + 1, box.x_range[1]), (box.y_range[0], box.y_range[0] + box_size), (box.z_range[0], box.z_range[0] + box_size)),
        Box((box.x_range[0] + box_size + 1, box.x_range[1]), (box.y_range[0], box.y_range[0] + box_size), (box.z_range[0] + box_size + 1, box.z_range[1])),
        Box((box.x_range[0] + box_size + 1, box.x_range[1]), (box.y_range[0] + box_size + 1, box.y_range[1]), (box.z_range[0], box.z_range[0] + box_size)),
        Box((box.x_range[0] + box_size + 1, box.x_range[1]), (box.y_range[0] + box_size + 1, box.y_range[1]), (box.z_range[0] + box_size + 1, box.z_range[1]))
    ]

    maxes = []
    for b in boxes_to_check:
        # disqualify if there's not possibly enough
        count = 0
        for n in nanobots:
            if n.box_in_range(b):
                count += 1
        if count < MAXIMUM_SEEN:
            continue
        # If it's a single point, see how many are in range
        if box_size == 0:
            if count > MAXIMUM_SEEN:
                MAXIMUM_POINT = (b.x_range[0], b.y_range[0], b.z_range[0])
                MAXIMUM_SEEN = count
            elif count == MAXIMUM_SEEN and (abs(b.x_range[0]) + abs(b.y_range[0]) + abs(b.z_range[0])) < (abs(MAXIMUM_POINT[0]) + abs(MAXIMUM_POINT[1]) + abs(MAXIMUM_POINT[2])):
                MAXIMUM_POINT = (b.x_range[0], b.y_range[0], b.z_range[0])
            return count

        count = recursive_search(b, nanobots)
        if not count:
            continue
        maxes.append(count)
    return max(maxes) if len(maxes) > 0 else None

def solution_part2(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
    with open(fname, "r") as f:
        nanobots: list[Nanobot] = []
        ranges: list[list[int]] = [[0, 0], [0, 0], [0, 0]]
        for line in f:
            m = LINE_REGEX.match(line)
            if m:
                x = int(m.group(1) + m.group(2))
                y = int(m.group(3) + m.group(4))
                z = int(m.group(5) + m.group(6))
                r = int(m.group(7) + m.group(8))
                nanobots.append(Nanobot(x, y, z, r))

                ranges[0][0] = min(ranges[0][0], x)
                ranges[0][1] = max(ranges[0][1], x)
                ranges[1][0] = min(ranges[1][0], y)
                ranges[1][1] = max(ranges[1][1], y)
                ranges[2][0] = min(ranges[2][0], z)
                ranges[2][1] = max(ranges[2][1], z)
            else:
                print("NO MATCH: ", line)

        maximum_box_size = 1
        largest_range = max(ranges[0][1] - ranges[0][0], ranges[1][1] - ranges[1][0], ranges[2][1] - ranges[2][0])
        while maximum_box_size < largest_range:
            maximum_box_size *= 2

        maximum_box = Box((ranges[0][0], ranges[0][0] + maximum_box_size), (ranges[1][0], ranges[1][0] + maximum_box_size), (ranges[2][0], ranges[2][0] + maximum_box_size))

        global MAXIMUM_SEEN

        for i in range(len(nanobots), 0, -1):
            MAXIMUM_SEEN = i
            if recursive_search(maximum_box, nanobots):
                return abs(MAXIMUM_POINT[0]) + abs(MAXIMUM_POINT[1]) + abs(MAXIMUM_POINT[2])

print(solution_part1())
print(solution_part2())
