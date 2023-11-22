import os

def solution_part1(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
    with open(fname, "r") as f:
        numbers: list[int] = [int(x) for x in f.readline().split()]
        total_metadata: int = 0

        stack: list[tuple[int, int]] = [(numbers[0], numbers[1])]
        i = 2
        while i < len(numbers) and len(stack) > 0:
            if stack[-1][0] == 0:
                for _ in range(stack.pop(-1)[1]):
                    total_metadata += numbers[i]
                    i += 1
            else:
                stack[-1] = (stack[-1][0] - 1, stack[-1][1])
                stack.append((numbers[i], numbers[i+1]))
                i += 2
        return total_metadata


def solution_part2(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
    with open(fname, "r") as f:
        numbers: list[int] = [int(x) for x in f.readline().split()]

        return recursive_solver(numbers)[0]

def recursive_solver(numbers: list[int], i: int = 0):
    num_child_nodes = numbers[i]
    num_metadata = numbers[i+1]
    i += 2

    children: list[int] = []
    for _ in range(num_child_nodes):
        c, i = recursive_solver(numbers, i)
        children.append(c)

    result = 0
    for _ in range(num_metadata):
        if num_child_nodes == 0:
            result += numbers[i]
        elif numbers[i] > 0 and numbers[i] <= len(children):
            result += children[numbers[i] - 1]
        i += 1

    return result, i

print(solution_part1())
print(solution_part2())
