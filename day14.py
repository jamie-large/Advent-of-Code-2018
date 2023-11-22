import os

def solution_part1(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
    with open(fname, "r") as f:
        end = int(f.readline())

        scores = [3, 7]
        elf_1_index = 0
        elf_2_index = 1

        while len(scores) < end + 10:
            new_scores = scores[elf_1_index] + scores[elf_2_index]
            if new_scores >= 10:
                scores.append(1)
            scores.append(new_scores % 10)

            elf_1_index = (elf_1_index + 1 + scores[elf_1_index]) % len(scores)
            elf_2_index = (elf_2_index + 1 + scores[elf_2_index]) % len(scores)
        return "".join([str(c) for c in scores[end:end+10]])


def solution_part2(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
    with open(fname, "r") as f:
        target_str = f.readline()[:-1]
        target = [int(c) for c in target_str]

        scores = [3, 7]
        elf_1_index = 0
        elf_2_index = 1

        while True:
            new_scores = scores[elf_1_index] + scores[elf_2_index]
            if new_scores >= 10:
                scores.append(1)
                if target[-1] == 1 and len(scores) >= len(target) and scores[-1 * len(target):] == target:
                    return len(scores) - len(target)
            scores.append(new_scores % 10)
            if target[-1] == new_scores % 10 and len(scores) >= len(target) and scores[-1 * len(target):] == target:
                return len(scores) - len(target)

            elf_1_index = (elf_1_index + 1 + scores[elf_1_index]) % len(scores)
            elf_2_index = (elf_2_index + 1 + scores[elf_2_index]) % len(scores)

print(solution_part1())
print(solution_part2())
