import os

def solution_part1(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
    with open(fname, "r") as f:
        points: dict[tuple[int, int], int] = dict()
        for line in f:
            x, y = line.split(",")
            points[(int(x), int(y))] = 0

        min_x = min(points, key=lambda x: x[0])[0]
        max_x = max(points, key=lambda x: x[0])[0]
        min_y = min(points, key=lambda x: x[1])[1]
        max_y = max(points, key=lambda x: x[1])[1]

        for i in range(min_x, max_x + 1):
            for j in range(min_y, max_y + 1):
                # find closest point
                min_distance = 99999999
                closest_point = (-1, -1)
                tie = False
                for point in points:
                    manhattan_distance = abs(point[0] - i) + abs(point[1] - j)
                    if manhattan_distance < min_distance:
                        closest_point = point
                        min_distance = manhattan_distance
                        tie = False
                    elif manhattan_distance == min_distance:
                        tie = True
                if not tie:
                    points[closest_point] += 1

        largest_area = 0
        for point in points:
            if point[0] in (min_x, max_x) or point[1] in (min_y, max_y):
                continue
            if points[point] > largest_area:
                largest_area = points[point]

        return largest_area



def solution_part2(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt", cutoff: int = 10000):
    with open(fname, "r") as f:

        points: dict[tuple[int, int], int] = dict()
        for line in f:
            x, y = line.split(",")
            points[(int(x), int(y))] = 0

        min_x = min(points, key=lambda x: x[0])[0]
        max_x = max(points, key=lambda x: x[0])[0]
        min_y = min(points, key=lambda x: x[1])[1]
        max_y = max(points, key=lambda x: x[1])[1]

        queue = [((min_x + max_x) // 2, (min_y + max_y) // 2)]
        seen = set(queue)
        found_a_start = False
        count = 0
        while len(queue) > 0:
            i, j = queue.pop(0)
            total_manhattan_distance = 0
            for p in points:
                total_manhattan_distance += abs(i - p[0]) + abs(j - p[1])
            neighbors = [(i+1, j), (i-1, j), (i, j-1), (i, j+1)] if total_manhattan_distance < cutoff or not found_a_start else []
            if total_manhattan_distance < cutoff:
                found_a_start = True
                count += 1

            for n in neighbors:
                if n not in seen:
                    seen.add(n)
                    queue.append(n)

        return count




print(solution_part1())
print(solution_part2())
