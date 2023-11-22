def solution_part1(fname: str = "inputs/day1.txt"):
    with open(fname, "r") as f:
        count = 0
        for line in f:
            count += int(line)
        return count

def solution_part2(fname: str = "inputs/day1.txt"):
    with open(fname, "r") as f:
        count = 0
        seen_counts = set([0])
        instructions = [int(x) for x in f.readlines()]

        i = 0
        while True:
            count += instructions[i]
            if count in seen_counts:
                return count
            seen_counts.add(count)

            i = ((i + 1) % len(instructions))

print(solution_part1())
print(solution_part2())
