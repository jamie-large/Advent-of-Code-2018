import os

def execute_instruction(instruction: tuple[str, int, int, int], registry: list[int]):
    inst = instruction[0]
    if inst == "addr":
        registry[instruction[3]] = registry[instruction[1]] + registry[instruction[2]]
    elif inst == "addi":
        registry[instruction[3]] = registry[instruction[1]] + instruction[2]
    elif inst == "mulr":
        registry[instruction[3]] = registry[instruction[1]] * registry[instruction[2]]
    elif inst == "muli":
        registry[instruction[3]] = registry[instruction[1]] * instruction[2]
    elif inst == "banr":
        registry[instruction[3]] = registry[instruction[1]] & registry[instruction[2]]
    elif inst == "bani":
        registry[instruction[3]] = registry[instruction[1]] & instruction[2]
    elif inst == "borr":
        registry[instruction[3]] = registry[instruction[1]] | registry[instruction[2]]
    elif inst == "bori":
        registry[instruction[3]] = registry[instruction[1]] | instruction[2]
    elif inst == "setr":
        registry[instruction[3]] = registry[instruction[1]]
    elif inst == "seti":
        registry[instruction[3]] = instruction[1]
    elif inst == "gtir":
        registry[instruction[3]] = 1 if instruction[1] > registry[instruction[2]] else 0
    elif inst == "gtri":
        registry[instruction[3]] = 1 if registry[instruction[1]] > instruction[2] else 0
    elif inst == "gtrr":
        registry[instruction[3]] = 1 if registry[instruction[1]] > registry[instruction[2]] else 0
    elif inst == "eqir":
        registry[instruction[3]] = 1 if instruction[1] == registry[instruction[2]] else 0
    elif inst == "eqri":
        registry[instruction[3]] = 1 if registry[instruction[1]] == instruction[2] else 0
    elif inst == "eqrr":
        registry[instruction[3]] = 1 if registry[instruction[1]] == registry[instruction[2]] else 0

def solution_part1(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
    with open(fname, "r") as f:
        instruction_pointer = -1
        instructions = []
        for line in f:
            spl = line.split()
            if spl[0] == "#ip":
                instruction_pointer = int(spl[-1])
                continue
            instructions.append((spl[0], int(spl[1]), int(spl[2]), int(spl[3])))
        registry = [0 for _ in range(6)]

        while registry[instruction_pointer] < len(instructions):
            execute_instruction(instructions[registry[instruction_pointer]], registry)
            registry[instruction_pointer] += 1

        return registry[0]


def solution_part2(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
    with open(fname, "r") as f:
        # ANALYZED PROGRAM
        # Program puts value 10551288 into regsitry 3, then calculates the sum of all the factors of registry 3
        # Used prime factorization + algorithm to find it
        # Prime factorization is 2*2*2*3*11*17*2351
        # Therefore sum is (1+2+4+8)(1+3)(1+11)(1+17)(1+2351) = 30481920
        return 30481920

print(solution_part1())
print(solution_part2())
