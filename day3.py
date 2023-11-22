import os

def solution_part1(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
    with open(fname, "r") as f:
        single_locations: set[tuple[int, int]] = set()
        double_locations: set[tuple[int, int]] = set()
        for line in f:
            spl = line.split()
            x, y = [int(c) for c in spl[2][:-1].split(",")]
            width, height = [int(c) for c in spl[3].split("x")]

            for i in range(x, x + width):
                for j in range(y, y + height):
                    if (i, j) in single_locations:
                        double_locations.add((i, j))
                    else:
                        single_locations.add((i, j))

        return len(double_locations)


def solution_part2(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
    with open(fname, "r") as f:
        fabric_map: dict[tuple[int, int], list[str]] = {}
        unoverlapped_zones: set[str] = set()

        for line in f:
            spl = line.split()
            name = spl[0]
            x, y = [int(c) for c in spl[2][:-1].split(",")]
            width, height = [int(c) for c in spl[3].split("x")]

            unoverlapped_zones.add(name)

            for i in range(x, x + width):
                for j in range(y, y + height):
                    if (i, j) in fabric_map:
                        for zone_name in fabric_map[(i, j)]:
                            if zone_name in unoverlapped_zones:
                                unoverlapped_zones.remove(zone_name)
                        if name in unoverlapped_zones:
                            unoverlapped_zones.remove(name)
                    else:
                        fabric_map[(i, j)] = []
                    fabric_map[(i, j)].append(name)
        return unoverlapped_zones.pop()[1:]


print(solution_part1())
print(solution_part2())
