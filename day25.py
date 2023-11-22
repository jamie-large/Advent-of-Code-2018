import os, re

LINE_REGEX = re.compile("(-?[0-9]+),(-?[0-9]+),(-?[0-9]+),(-?[0-9]+)")

Point = tuple[int, int, int, int]

def dist(p1: tuple, p2: tuple):
    return sum([abs(p1[i] - p2[i]) for i in range(len(p1))])

def solution_part1(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
    with open(fname, "r") as f:
        points: set[Point] = set()
        for line in f:
            m = LINE_REGEX.match(line)
            if m:
                points.add((int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))))
            else:
                print(f"Failed to find match: {line}")
                return

        num_constellations = 0
        while len(points) > 0:
            num_constellations += 1
            stack = [points.pop()]
            visited: set[Point] = set(stack)
            while len(stack) > 0:
                current_point = stack.pop()
                # find all points to add
                points_to_add: set[Point] = set()
                for p in points:
                    if dist(current_point, p) <= 3:
                        points_to_add.add(p)
                for p in points_to_add:
                    points.remove(p)
                    visited.add(p)
                    stack.append(p)
        return num_constellations

print(solution_part1())
