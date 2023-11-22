import os

def solution_part1(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
    with open(fname, "r") as f:
        grid = [[c for c in line[:-1]] for line in f.readlines()]
        for _ in range(10):
            grid = get_next_grid(grid)

        trees = 0
        lumberyards = 0
        for row in grid:
            for c in row:
                if c == "|":
                    trees += 1
                elif c == "#":
                    lumberyards += 1
        print(f"{trees} trees, {lumberyards} lumberyards")
        return trees * lumberyards

def get_next_grid(grid: list[list[str]]):
    next_grid = [[x for x in row] for row in grid]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            neighbors = [x for x in [(i-1, j-1), (i-1, j), (i-1, j+1), (i, j-1), (i, j+1), (i+1, j-1), (i+1, j), (i+1, j+1)] if x[0] >= 0 and x[0] < len(grid) and x[1] >= 0 and x[1] < len(grid[i])]
            trees = 0
            lumberyards = 0
            for n in neighbors:
                val = grid[n[0]][n[1]]
                if val == "|":
                    trees += 1
                elif val == "#":
                    lumberyards += 1
            if grid[i][j] == "." and trees >= 3:
                next_grid[i][j] = "|"
            elif grid[i][j] == "|" and lumberyards >= 3:
                next_grid[i][j] = "#"
            elif grid[i][j] == "#":
                next_grid[i][j] = "#" if trees >= 1 and lumberyards >= 1 else "."

    return next_grid

def solution_part2(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
    with open(fname, "r") as f:
        cache: dict[str, int] = {}
        reverse_cache: dict[int, str] = {}
        grid = [[c for c in line[:-1]] for line in f.readlines()]

        i = 0
        while True:
            serialized_grid = "".join(["".join(line) for line in grid])
            if serialized_grid in cache:
                difference = i - cache[serialized_grid]
                final_serialized_grid = reverse_cache[1000000000 - (((1000000000 - i) // difference + 1) * difference)]
                return final_serialized_grid.count("|") * final_serialized_grid.count("#")
            cache[serialized_grid] = i
            reverse_cache[i] = serialized_grid
            grid = get_next_grid(grid)
            i += 1


print(solution_part1())
print(solution_part2())
