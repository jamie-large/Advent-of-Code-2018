import os
from heapq import heapify, heappush, heappop

def solution_part1(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
    with open(fname, "r") as f:
        depth = int(f.readline().split()[-1])
        target = tuple([int(t) for t in f.readline().split()[-1].split(",")])

        def calculate_erosion_level(geologic_index: int):
            return (geologic_index + depth) % 20183

        cave_map: list[list[int]] = []
        for y in range(target[1] + 1):
            cave_map.append([])
            for x in range(target[0] + 1):
                if (x, y) == (0, 0) or (x, y) == target:
                    cave_map[y].append(calculate_erosion_level(0))
                elif y == 0:
                    cave_map[y].append(calculate_erosion_level(x * 16807))
                elif x == 0:
                    cave_map[y].append(calculate_erosion_level(y * 48271))
                else:
                    cave_map[y].append(calculate_erosion_level(cave_map[y-1][x] * cave_map[y][x-1]))

        risk_level = 0
        for row in cave_map:
            for num in row:
                risk_level += (num % 3)
        return risk_level


ROCK = 0
WET = 1
NARROW = 2

NEITHER = 0
TORCH = 1
CLIMBING_GEAR = 2

def solution_part2(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
    with open(fname, "r") as f:
        depth = int(f.readline().split()[-1])
        target = tuple([int(t) for t in f.readline().split()[-1].split(",")])

        def calculate_erosion_level(geologic_index: int):
            return (geologic_index + depth) % 20183

        cave_map: list[list[int]] = []
        for y in range(target[1] + 1):
            cave_map.append([])
            for x in range(target[0] + 1):
                if (x, y) == (0, 0) or (x, y) == target:
                    cave_map[y].append(calculate_erosion_level(0))
                elif y == 0:
                    cave_map[y].append(calculate_erosion_level(x * 16807))
                elif x == 0:
                    cave_map[y].append(calculate_erosion_level(y * 48271))
                else:
                    cave_map[y].append(calculate_erosion_level(cave_map[y-1][x] * cave_map[y][x-1]))

        # for row in cave_map:
        #     print()
        #     for num in row:
        #         print(num % 3, end='')

        def calculate_unknown_position(x: int, y: int):
            for j in range(y+1):
                if j == len(cave_map):
                    cave_map.append([])
                for i in range(len(cave_map[j]), x+1):
                    if j == 0:
                        cave_map[j].append(calculate_erosion_level(i * 16807))
                    elif i == 0:
                        cave_map[j].append(calculate_erosion_level(j * 48271))
                    else:
                        cave_map[j].append(calculate_erosion_level(cave_map[j-1][i] * cave_map[j][i-1]))


        def tool_is_valid(x: int, y: int, tool: int):
            n_type = cave_map[y][x] % 3
            return (n_type != ROCK or tool != NEITHER) and (n_type != WET or tool != TORCH) and (n_type != NARROW or tool != CLIMBING_GEAR)


        # (steps, position, tool)
        min_heap: list[tuple[int, tuple[int, int], int]] = [(0, (0, 0), TORCH)]
        heapify(min_heap)
        # (position, tool) -> steps
        visited: dict[tuple[tuple[int, int], int], int] = {}
        visited[((0, 0), TORCH)] = 0

        while len(min_heap) > 0:
            steps, (x, y), tool = heappop(min_heap)

            if (x, y) == target and tool == TORCH:
                return steps

            if visited[((x, y), tool)] < steps:
                continue

            # changing tools is valid (if we haven't done so already)
            other_tools = [NEITHER, TORCH, CLIMBING_GEAR]
            other_tools.remove(tool)
            for ot in other_tools:
                if (not tool_is_valid(x, y, ot)) or (((x, y), ot) in visited and visited[((x, y), ot)] <= steps + 7):
                    continue
                visited[((x, y), ot)] = steps + 7
                heappush(min_heap, (steps + 7, (x, y), ot))

            # find valid neighbors
            neighbors = [(x-1, y), (x, y-1), (x+1, y), (x, y+1)]
            neighbors = [(a, b) for a, b in neighbors if a >= 0 and b >= 0]

            for a, b in neighbors:
                # calculate position if necessary
                if b >= len(cave_map) or a >= len(cave_map[b]):
                    calculate_unknown_position(a, b)
                # figure out if we can/want to move there
                if (not tool_is_valid(a, b, tool)) or (((a, b), tool) in visited and visited[((a, b), tool)] <= steps + 1):
                    continue
                if (a, b) == target and tool == TORCH:
                    return steps + 1
                visited[((a, b), tool)] = steps + 1
                heappush(min_heap, (steps + 1, (a, b), tool))

print(solution_part1())
print(solution_part2())
