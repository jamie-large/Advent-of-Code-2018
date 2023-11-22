import os
from datetime import datetime

SLEEP = -1
WAKE = -2

def solution_part1(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
    with open(fname, "r") as f:
        instructions = [parse_line(l) for l in f.readlines()]
        instructions.sort(key=lambda x: x[0])

        minutes_slept = get_guard_sleep_map(instructions)

        sleepiest_guard = -1
        most_sleep = -1
        for guard in minutes_slept:
            s = sum(minutes_slept[guard].values())
            if s > most_sleep:
                most_sleep = s
                sleepiest_guard = guard

        sleepiest_minute = -1
        most_sleep = -1
        for minute in minutes_slept[sleepiest_guard]:
            if minutes_slept[sleepiest_guard][minute] > most_sleep:
                most_sleep = minutes_slept[sleepiest_guard][minute]
                sleepiest_minute = minute
        return sleepiest_guard * sleepiest_minute


def parse_line(line: str) -> tuple[datetime, int]:
    spl = line.split()
    date = datetime.strptime(f"{spl[0]} {spl[1]}", "[%Y-%m-%d %H:%M]")
    type = WAKE if spl[2] == "wakes" else SLEEP if spl[2] == "falls" else int(spl[3][1:])
    return (date, type)

def get_guard_sleep_map(instructions: list[tuple[datetime, int]]):
    # guard -> (minute -> time slept)
    minutes_slept: dict[int, dict[int, int]] = {}

    current_guard = -1
    i = 0
    while i < len(instructions):
        inst = instructions[i]
        if inst[1] == SLEEP:
            if current_guard not in minutes_slept:
                minutes_slept[current_guard] = {}
            current_minutes_slept = minutes_slept[current_guard]
            for j in range(inst[0].minute, instructions[i+1][0].minute):
                current_minutes_slept[j] = current_minutes_slept.get(j, 0) + 1
            i += 2
        else:
            current_guard = inst[1]
            i += 1

    return minutes_slept


def solution_part2(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
    with open(fname, "r") as f:
        instructions = [parse_line(l) for l in f.readlines()]
        instructions.sort(key=lambda x: x[0])

        minutes_slept = get_guard_sleep_map(instructions)

        sleepiest_guard = -1
        sleepiest_minute = -1
        most_sleep = -1
        for guard in minutes_slept:
            for minute in minutes_slept[guard]:
                if minutes_slept[guard][minute] > most_sleep:
                    most_sleep = minutes_slept[guard][minute]
                    sleepiest_guard = guard
                    sleepiest_minute = minute

        return sleepiest_guard * sleepiest_minute

print(solution_part1())
print(solution_part2())
