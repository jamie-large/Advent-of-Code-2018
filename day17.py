import os

def solution_part1(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
    with open(fname, "r") as f:
        grid: dict[tuple[int, int], str] = { (0, 500): "+" }
        total_x_range = (99999, -99999)
        total_y_range = (99999, -99999)
        for line in f:
            spl = line.split()
            second_spl = spl[1].split("..")
            x_range = (int(spl[0][2:-1]), int(spl[0][2:-1])) if line[0] == "x" else (int(second_spl[0][2:]), int(second_spl[1]))
            y_range = (int(spl[0][2:-1]), int(spl[0][2:-1])) if line[0] == "y" else (int(second_spl[0][2:]), int(second_spl[1]))

            if x_range[0] < total_x_range[0]:
                total_x_range = (x_range[0], total_x_range[1])
            if x_range[1] > total_x_range[1]:
                total_x_range = (total_x_range[0], x_range[1])
            if y_range[0] < total_y_range[0]:
                total_y_range = (y_range[0], total_y_range[1])
            if y_range[1] > total_y_range[1]:
                total_y_range = (total_y_range[0], y_range[1])

            for x in range(x_range[0], x_range[1] + 1):
                for y in range(y_range[0], y_range[1] + 1):
                    grid[(x, y)] = "#"

        stack: list[tuple[int, int]] = [(500, 0)]
        watered_tiles: set[tuple[int, int]] = set(stack)
        while len(stack) > 0:
            current = stack.pop()
            watered_tiles.add(current)
            if grid.get(current, ".") in ("~", "|"):
                continue
            grid[current] = "x"
            # If at the bottom, done
            if current[1] == total_y_range[1]:
                grid[current] = "|"
                continue

            below_square = grid.get((current[0], current[1] + 1), ".")
            # move down if the water can
            if below_square == ".":
                stack.append(current)
                stack.append((current[0], current[1] + 1))
                continue
            if below_square == "|":
                grid[current] = "|"
                continue

            # move left/right if the water can
            left_square = grid.get((current[0] - 1, current[1]), ".")
            right_square = grid.get((current[0] + 1, current[1]), ".")
            if left_square == "." or right_square == ".":
                stack.append(current)
                if left_square == ".":
                    stack.append((current[0] - 1, current[1]))
                if right_square == ".":
                    stack.append((current[0] + 1, current[1]))
            elif left_square == "|" or right_square == "|":
                grid[current] = "|"
            elif left_square == "~" or right_square == "~":
                grid[current] = "~"
            elif left_square == "x" and right_square == "#":
                x = current[0]
                test = grid.get((x, current[1]), ".")
                while test == "x":
                    x -= 1
                    test = grid.get((x, current[1]), ".")
                if test in ("#", "~", "|"):
                    grid[current] = "|" if test == "|" else "~"
                else:
                    stack.append(current)
                    stack.append((x, current[1]))
            elif left_square == "#" and right_square == "x":
                x = current[0]
                test = grid.get((x, current[1]), ".")
                while test == "x":
                    x += 1
                    test = grid.get((x, current[1]), ".")
                if test in ("#", "~", "|"):
                    grid[current] = "|" if test == "|" else "~"
                else:
                    stack.append(current)
                    stack.append((x, current[1]))
            else:
                grid[current] = "~"

        result = 0
        for tile in watered_tiles:
            if tile[1] >= total_y_range[0] and tile[1] <= total_y_range[1]:
                result += 1
        return result



def solution_part2(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
    with open(fname, "r") as f:
        grid: dict[tuple[int, int], str] = { (0, 500): "+" }
        total_x_range = (99999, -99999)
        total_y_range = (99999, -99999)
        for line in f:
            spl = line.split()
            second_spl = spl[1].split("..")
            x_range = (int(spl[0][2:-1]), int(spl[0][2:-1])) if line[0] == "x" else (int(second_spl[0][2:]), int(second_spl[1]))
            y_range = (int(spl[0][2:-1]), int(spl[0][2:-1])) if line[0] == "y" else (int(second_spl[0][2:]), int(second_spl[1]))

            if x_range[0] < total_x_range[0]:
                total_x_range = (x_range[0], total_x_range[1])
            if x_range[1] > total_x_range[1]:
                total_x_range = (total_x_range[0], x_range[1])
            if y_range[0] < total_y_range[0]:
                total_y_range = (y_range[0], total_y_range[1])
            if y_range[1] > total_y_range[1]:
                total_y_range = (total_y_range[0], y_range[1])

            for x in range(x_range[0], x_range[1] + 1):
                for y in range(y_range[0], y_range[1] + 1):
                    grid[(x, y)] = "#"

        stack: list[tuple[int, int]] = [(500, 0)]
        watered_tiles: set[tuple[int, int]] = set(stack)
        while len(stack) > 0:
            current = stack.pop()
            watered_tiles.add(current)
            if grid.get(current, ".") in ("~", "|"):
                continue
            grid[current] = "x"
            # If at the bottom, done
            if current[1] == total_y_range[1]:
                grid[current] = "|"
                continue

            below_square = grid.get((current[0], current[1] + 1), ".")
            # move down if the water can
            if below_square == ".":
                stack.append(current)
                stack.append((current[0], current[1] + 1))
                continue
            if below_square == "|":
                grid[current] = "|"
                continue

            # move left/right if the water can
            left_square = grid.get((current[0] - 1, current[1]), ".")
            right_square = grid.get((current[0] + 1, current[1]), ".")
            if left_square == "." or right_square == ".":
                stack.append(current)
                if left_square == ".":
                    stack.append((current[0] - 1, current[1]))
                if right_square == ".":
                    stack.append((current[0] + 1, current[1]))
            elif left_square == "|" or right_square == "|":
                grid[current] = "|"
            elif left_square == "~" or right_square == "~":
                grid[current] = "~"
            elif left_square == "x" and right_square == "#":
                x = current[0]
                test = grid.get((x, current[1]), ".")
                while test == "x":
                    x -= 1
                    test = grid.get((x, current[1]), ".")
                if test in ("#", "~", "|"):
                    grid[current] = "|" if test == "|" else "~"
                else:
                    stack.append(current)
                    stack.append((x, current[1]))
            elif left_square == "#" and right_square == "x":
                x = current[0]
                test = grid.get((x, current[1]), ".")
                while test == "x":
                    x += 1
                    test = grid.get((x, current[1]), ".")
                if test in ("#", "~", "|"):
                    grid[current] = "|" if test == "|" else "~"
                else:
                    stack.append(current)
                    stack.append((x, current[1]))
            else:
                grid[current] = "~"

        result = 0
        for tile in grid:
            if grid[tile] == "~":
                result += 1
        return result

print(solution_part1())
print(solution_part2())
