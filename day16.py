import os

SAMPLE_INSTRUCTION_MAP = {
    0: "addr",
    1: "addi",
    2: "mulr",
    3: "muli",
    4: "banr",
    5: "bani",
    6: "borr",
    7: "bori",
    8: "setr",
    9: "seti",
    10: "gtir",
    11: "gtri",
    12: "gtrr",
    13: "eqir",
    14: "eqri",
    15: "eqrr"
}

def execute_instruction(instruction: tuple[int, int, int, int], registry: tuple[int, int, int, int], instruction_map: dict[int, str]):
    registry_copy = [x for x in registry]
    inst = instruction_map[instruction[0]]
    if inst == "addr":
        registry_copy[instruction[3]] = registry[instruction[1]] + registry[instruction[2]]
    elif inst == "addi":
        registry_copy[instruction[3]] = registry[instruction[1]] + instruction[2]
    elif inst == "mulr":
        registry_copy[instruction[3]] = registry[instruction[1]] * registry[instruction[2]]
    elif inst == "muli":
        registry_copy[instruction[3]] = registry[instruction[1]] * instruction[2]
    elif inst == "banr":
        registry_copy[instruction[3]] = registry[instruction[1]] & registry[instruction[2]]
    elif inst == "bani":
        registry_copy[instruction[3]] = registry[instruction[1]] & instruction[2]
    elif inst == "borr":
        registry_copy[instruction[3]] = registry[instruction[1]] | registry[instruction[2]]
    elif inst == "bori":
        registry_copy[instruction[3]] = registry[instruction[1]] | instruction[2]
    elif inst == "setr":
        registry_copy[instruction[3]] = registry[instruction[1]]
    elif inst == "seti":
        registry_copy[instruction[3]] = instruction[1]
    elif inst == "gtir":
        registry_copy[instruction[3]] = 1 if instruction[1] > registry[instruction[2]] else 0
    elif inst == "gtri":
        registry_copy[instruction[3]] = 1 if registry[instruction[1]] > instruction[2] else 0
    elif inst == "gtrr":
        registry_copy[instruction[3]] = 1 if registry[instruction[1]] > registry[instruction[2]] else 0
    elif inst == "eqir":
        registry_copy[instruction[3]] = 1 if instruction[1] == registry[instruction[2]] else 0
    elif inst == "eqri":
        registry_copy[instruction[3]] = 1 if registry[instruction[1]] == instruction[2] else 0
    elif inst == "eqrr":
        registry_copy[instruction[3]] = 1 if registry[instruction[1]] == registry[instruction[2]] else 0
    return (registry_copy[0], registry_copy[1], registry_copy[2], registry_copy[3])

def solution_part1(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
    with open(fname, "r", encoding="utf8") as f:
        final_count = 0
        while True:
            spl = f.readline().split()
            if len(spl) < 5:
                break
            original_registry = (int(spl[1][1:-1]), int(spl[2][:-1]), int(spl[3][:-1]), int(spl[4][:-1]))

            spl = f.readline().split()
            instruction = (int(spl[0]), int(spl[1]), int(spl[2]), int(spl[3]))

            spl = f.readline().split()
            updated_registry = (int(spl[1][1:-1]), int(spl[2][:-1]), int(spl[3][:-1]), int(spl[4][:-1]))

            possibilities = 0
            for i in SAMPLE_INSTRUCTION_MAP:
                result = execute_instruction((i, instruction[1], instruction[2], instruction[3]), original_registry, SAMPLE_INSTRUCTION_MAP)
                if result == updated_registry:
                    possibilities += 1

            if possibilities >= 3:
                final_count += 1
            f.readline()
        return final_count

def solution_part2(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
    with open(fname, "r") as f:
        possibilities_map: dict[int, set[str]] = {}
        while True:
            spl = f.readline().split()
            if len(spl) < 5:
                break
            original_registry = (int(spl[1][1:-1]), int(spl[2][:-1]), int(spl[3][:-1]), int(spl[4][:-1]))

            spl = f.readline().split()
            instruction = (int(spl[0]), int(spl[1]), int(spl[2]), int(spl[3]))

            spl = f.readline().split()
            updated_registry = (int(spl[1][1:-1]), int(spl[2][:-1]), int(spl[3][:-1]), int(spl[4][:-1]))

            possibilities: set[str] = set()
            for i in SAMPLE_INSTRUCTION_MAP:
                result = execute_instruction((i, instruction[1], instruction[2], instruction[3]), original_registry, SAMPLE_INSTRUCTION_MAP)
                if result == updated_registry:
                    possibilities.add(SAMPLE_INSTRUCTION_MAP[i])

            if instruction[0] not in possibilities_map:
                possibilities_map[instruction[0]] = possibilities
            else:
                possibilities_map[instruction[0]] = possibilities_map[instruction[0]].intersection(possibilities)

            if len(possibilities_map[instruction[0]]) == 1:
                solved = list(possibilities_map[instruction[0]])[0]
                for i in possibilities_map:
                    if i != instruction[0] and solved in possibilities_map[i]:
                        possibilities_map[i].remove(solved)

            f.readline()

        instruction_map: dict[int, str] = {}
        for i in possibilities_map:
            instruction_map[i] = list(possibilities_map[i])[0]

        f.readline()
        registry = (0, 0, 0, 0)
        while True:
            spl = f.readline().split()
            if len(spl) < 4:
                break

            instruction = (int(spl[0]), int(spl[1]), int(spl[2]), int(spl[3]))
            registry = execute_instruction(instruction, registry, instruction_map)

        return registry[0]

print(solution_part1())
print(solution_part2())
