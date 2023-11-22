import os

def solution_part1(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
    with open(fname, "r") as f:
        serial_number = int(f.readline())
        grid: list[list[int]] = []
        max_value = -1000000
        max_location = (0, 0)
        for y in range(1, 301):
            for x in range(1, 301):
                rack_id = x + 10
                power_level = rack_id * y
                power_level += serial_number
                power_level *= rack_id
                power_level = (power_level // 100) % 10
                power_level -= 5

                if x == 1:
                    grid.append([])
                grid[-1].append(power_level)

                if x >= 3 and y >= 3:
                    value = grid[y-3][x-3] + grid[y-3][x-2] + grid[y-3][x-1] + \
                            grid[y-2][x-3] + grid[y-2][x-2] + grid[y-2][x-1] + \
                            grid[y-1][x-3] + grid[y-1][x-2] + grid[y-1][x-1]
                    if value > max_value:
                        max_value = value
                        max_location = (x-2, y-2)

        return max_location

def solution_part2(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
    with open(fname, "r") as f:
        serial_number = int(f.readline())
        grid: list[list[int]] = []
        max_value = -1000000
        max_location = (0, 0, 0)
        for y in range(1, 301):
            for x in range(1, 301):
                rack_id = x + 10
                power_level = rack_id * y
                power_level += serial_number
                power_level *= rack_id
                power_level = (power_level // 100) % 10
                power_level -= 5

                if x == 1 and y == 1:
                    grid.append([power_level])
                elif x == 1:
                    grid.append([power_level + grid[-1][0]])
                elif y == 1:
                    grid[-1].append(power_level + grid[-1][-1])
                else:
                    grid[-1].append(power_level + grid[y-2][x-1] + grid[y-1][x-2] - grid[y-2][x-2])

                for i in range(1, min(x, y) + 1):
                    value = grid[y-1][x-1] - grid[y-1-i][x-1] - grid[y-1][x-1-i] + grid[y-1-i][x-1-i]
                    if value > max_value:
                        max_value = value
                        max_location = (x-i+1, y-i+1, i)

        return max_location

print(solution_part1())
print(solution_part2())
