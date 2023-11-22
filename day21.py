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
            # Once we hit instruction 28, we exit if registry[0] is equal to registry[5]
            if registry[instruction_pointer] == 28:
                return registry[5]

def solution_part2(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
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

        seen_reg_5: set[int] = set()
        last_seen_reg_5: int = -1

        while registry[instruction_pointer] < len(instructions):
            execute_instruction(instructions[registry[instruction_pointer]], registry)
            registry[instruction_pointer] += 1
            # Once we hit instruction 28, we exit if registry[0] is equal to registry[5]
            if registry[instruction_pointer] == 28:
                if registry[5] in seen_reg_5:
                    return last_seen_reg_5
                last_seen_reg_5 = registry[5]
                seen_reg_5.add(registry[5])


print(solution_part1())
print(solution_part2())
