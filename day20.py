import os
from collections import defaultdict

def solution_part1(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
    with open(fname, "r") as f:
        route = f.readline()
        # x_pos, y_pos, route_index
        queue: list[tuple[int, int, int]] = [(0, 0, 1)]
        visited: set[tuple[int, int, int]] = set(queue)

        room_map: defaultdict[tuple[int, int], str] = defaultdict(lambda: "#")

        while len(queue) > 0:
            x_pos, y_pos, route_index = queue.pop(0)
            room_map[(x_pos, y_pos)] = "."

            directive = route[route_index]
            next_stops: list[tuple[int, int, int]] = []

            if directive == "$":
                continue
            elif directive == ")":
                next_stops.append((x_pos, y_pos, route_index + 1))
            elif directive in ("(", "|"):
                # find the matching closing parenthesis
                count = 1
                i = route_index + 1
                if directive == "(":
                    next_stops.append((x_pos, y_pos, i))
                while count != 0:
                    if route[i] == "(":
                        count += 1
                    elif route[i] == ")":
                        count -= 1
                    elif route[i] == "|" and directive == "(" and count == 1:
                        next_stops.append((x_pos, y_pos, i+1))
                    i += 1
                if directive == "|":
                    next_stops.append((x_pos, y_pos, i))
            elif directive == "N":
                room_map[(x_pos, y_pos + 1)] = "-"
                next_stops.append((x_pos, y_pos + 2, route_index + 1))
            elif directive == "E":
                room_map[(x_pos + 1, y_pos)] = "|"
                next_stops.append((x_pos + 2, y_pos, route_index + 1))
            elif directive == "S":
                room_map[(x_pos, y_pos - 1)] = "-"
                next_stops.append((x_pos, y_pos - 2, route_index + 1))
            elif directive == "W":
                room_map[(x_pos - 1, y_pos)] = "|"
                next_stops.append((x_pos - 2, y_pos, route_index + 1))

            for ns in next_stops:
                if ns not in visited:
                    queue.append(ns)
                    visited.add(ns)

        # Do BFS on the room map to find longest route
        bfs_queue: list[tuple[int, int, int]] = [(0, 0, 0)]
        bfs_visited: set[tuple[int, int]] = set([(0, 0)])
        max_doors = 0
        while len(bfs_queue) > 0:
            x_pos, y_pos, doors = bfs_queue.pop(0)
            max_doors = doors if doors > max_doors else max_doors

            next_stops = []
            if room_map[(x_pos + 1, y_pos)] == "|":
                next_stops.append((x_pos + 2, y_pos, doors + 1))
            if room_map[(x_pos - 1, y_pos)] == "|":
                next_stops.append((x_pos - 2, y_pos, doors + 1))
            if room_map[(x_pos, y_pos + 1)] == "-":
                next_stops.append((x_pos, y_pos + 2, doors + 1))
            if room_map[(x_pos, y_pos - 1)] == "-":
                next_stops.append((x_pos, y_pos - 2, doors + 1))
            for ns in next_stops:
                if (ns[0], ns[1]) not in bfs_visited:
                    bfs_queue.append(ns)
                    bfs_visited.add((ns[0], ns[1]))

        return max_doors

def draw_map(room_map: defaultdict[tuple[int, int], str]):
    x_min, y_min, x_max, y_max = 0, 0, 0, 0
    for x, y in room_map:
        if x < x_min:
            x_min = x
        if x > x_max:
            x_max = x
        if y < y_min:
            y_min = y
        if y > y_max:
            y_max = y

    for y in range(y_max + 1, y_min - 2, -1):
        buffer = []
        for x in range(x_min - 1, x_max + 2):
            buffer.append(room_map[(x, y)] if x != 0 or y != 0 else "X")
        print("".join(buffer))


def solution_part2(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
    with open(fname, "r") as f:
        route = f.readline()
        # x_pos, y_pos, route_index
        queue: list[tuple[int, int, int]] = [(0, 0, 1)]
        visited: set[tuple[int, int, int]] = set(queue)

        room_map: defaultdict[tuple[int, int], str] = defaultdict(lambda: "#")

        while len(queue) > 0:
            x_pos, y_pos, route_index = queue.pop(0)
            room_map[(x_pos, y_pos)] = "."

            directive = route[route_index]
            next_stops: list[tuple[int, int, int]] = []

            if directive == "$":
                continue
            elif directive == ")":
                next_stops.append((x_pos, y_pos, route_index + 1))
            elif directive in ("(", "|"):
                # find the matching closing parenthesis
                count = 1
                i = route_index + 1
                if directive == "(":
                    next_stops.append((x_pos, y_pos, i))
                while count != 0:
                    if route[i] == "(":
                        count += 1
                    elif route[i] == ")":
                        count -= 1
                    elif route[i] == "|" and directive == "(" and count == 1:
                        next_stops.append((x_pos, y_pos, i+1))
                    i += 1
                if directive == "|":
                    next_stops.append((x_pos, y_pos, i))
            elif directive == "N":
                room_map[(x_pos, y_pos + 1)] = "-"
                next_stops.append((x_pos, y_pos + 2, route_index + 1))
            elif directive == "E":
                room_map[(x_pos + 1, y_pos)] = "|"
                next_stops.append((x_pos + 2, y_pos, route_index + 1))
            elif directive == "S":
                room_map[(x_pos, y_pos - 1)] = "-"
                next_stops.append((x_pos, y_pos - 2, route_index + 1))
            elif directive == "W":
                room_map[(x_pos - 1, y_pos)] = "|"
                next_stops.append((x_pos - 2, y_pos, route_index + 1))

            for ns in next_stops:
                if ns not in visited:
                    queue.append(ns)
                    visited.add(ns)

        # Do BFS on the room map to find longest route
        bfs_queue: list[tuple[int, int, int]] = [(0, 0, 0)]
        bfs_visited: set[tuple[int, int]] = set([(0, 0)])
        count = 0
        while len(bfs_queue) > 0:
            x_pos, y_pos, doors = bfs_queue.pop(0)
            if doors >= 1000:
                count += 1

            next_stops = []
            if room_map[(x_pos + 1, y_pos)] == "|":
                next_stops.append((x_pos + 2, y_pos, doors + 1))
            if room_map[(x_pos - 1, y_pos)] == "|":
                next_stops.append((x_pos - 2, y_pos, doors + 1))
            if room_map[(x_pos, y_pos + 1)] == "-":
                next_stops.append((x_pos, y_pos + 2, doors + 1))
            if room_map[(x_pos, y_pos - 1)] == "-":
                next_stops.append((x_pos, y_pos - 2, doors + 1))
            for ns in next_stops:
                if (ns[0], ns[1]) not in bfs_visited:
                    bfs_queue.append(ns)
                    bfs_visited.add((ns[0], ns[1]))

        return count

print(solution_part1())
print(solution_part2())
