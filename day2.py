def solution_part1(fname: str = "inputs/day2.txt"):
    with open(fname, "r") as f:
        twice_counts = 0
        thrice_counts = 0
        for line in f:
            counts = [0 for _ in range(26)]
            for c in line[:-1]:
                counts[ord(c) - ord('a')] += 1
            seen_2 = False
            seen_3 = False
            for i in counts:
                if i == 2 and not seen_2:
                    twice_counts += 1
                    seen_2 = True
                elif i == 3 and not seen_3:
                    thrice_counts += 1
                    seen_3 = True
                if seen_2 and seen_3:
                    break
        return twice_counts * thrice_counts


def solution_part2(fname: str = "inputs/day2.txt"):
    with open(fname, "r") as f:
        previous_words = []
        for line in f:
            for previous_word in previous_words:
                difference_count = 0
                for i in range(len(previous_word)):
                    if line[i] != previous_word[i]:
                        difference_count += 1
                        if difference_count > 1:
                            break
                if difference_count == 1:
                    return "".join([previous_word[i] for i in range(len(previous_word)) if previous_word[i] == line[i]])
            previous_words.append(line[:-1])

print(solution_part1())
print(solution_part2())
