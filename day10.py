import os, re

LINE_REGEX = re.compile("position=< *(-*)(\d+), *(-*)(\d+)> velocity=< *(-*)(\d+), *(-*)(\d+)>")

class Point:
    def __init__(self, x: int, y: int, x_veloc: int, y_veloc: int):
        self.x = x
        self.y = y
        self.x_veloc = x_veloc
        self.y_veloc = y_veloc

    def update_position(self):
        self.x += self.x_veloc
        self.y += self.y_veloc

    def __repr__(self):
        return f"({self.x}, {self.y}) at <{self.x_veloc}, {self.y_veloc}>"

def solution_part1(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
    with open(fname, "r") as f:
        points: list[Point] = []
        for line in f:
            m = LINE_REGEX.match(line)
            if m:
                x = int(m.group(1) + m.group(2))
                y = int(m.group(3) + m.group(4))
                x_veloc = int(m.group(5) + m.group(6))
                y_veloc = int(m.group(7) + m.group(8))
                points.append(Point(x, y, x_veloc, y_veloc))
            else:
                print("NO MATCH: ", line)

        while True:
            points_set = set([(p.x, p.y) for p in points])

            min_x = min(p.x for p in points)
            max_x = max(p.x for p in points)
            min_y = min(p.y for p in points)
            max_y = max(p.y for p in points)
            if max_y - min_y <= 10:
                for j in range(min_y, max_y + 1):
                    for i in range(min_x, max_x + 1):
                        print("#" if (i, j) in points_set else ".", end="")

                    print()

                if input("Type 'n' to stop: ") == "n":
                    break

            for p in points:
                p.update_position()

def solution_part2(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
    with open(fname, "r") as f:
        points: list[Point] = []
        for line in f:
            m = LINE_REGEX.match(line)
            if m:
                x = int(m.group(1) + m.group(2))
                y = int(m.group(3) + m.group(4))
                x_veloc = int(m.group(5) + m.group(6))
                y_veloc = int(m.group(7) + m.group(8))
                points.append(Point(x, y, x_veloc, y_veloc))
            else:
                print("NO MATCH: ", line)
        counter = 0
        while True:
            min_y = min(p.y for p in points)
            max_y = max(p.y for p in points)
            if max_y - min_y <= 10:
                break

            for p in points:
                p.update_position()
            counter += 1

        return counter

solution_part1()
print(solution_part2())
