import os

def solution_part1(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
    with open(fname, "r") as f:
        line = f.readline()
        state = line[15:-1]
        line = f.readline()
        line = f.readline()

        instructions: dict[str, str] = {}

        while line and len(line) > 1:
            instructions[line[:5]] = line[-2]
            line = f.readline()

        zero_index = 0
        # print(f"{0}: {''.join(state)}, {zero_index}")

        for c in range(20):
            state = ("." * 4) + state + ("." * 4)
            zero_index += 4
            new_state = [c for c in state]
            for i in range(2, len(state) - 2):
                # print(f"Checking {state[i-2:i+3]} - {instructions.get(state[i-2:i+3], '.')}")
                if state[i-2:i+3] in instructions:
                    new_state[i] = instructions[state[i-2:i+3]]
                else:
                    new_state[i] = "."

            start = new_state.index("#")
            end = len(new_state) - 1 - new_state[::-1].index("#")
            state = "".join(new_state)[start:end+1]
            zero_index -= start
            # print(f"{c+1}: {''.join(state)}, {zero_index}")

        value = 0
        for i in range(len(state)):
            if state[i] == "#":
                value += i - zero_index
        return value


def solution_part2(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
    with open(fname, "r") as f:
        line = f.readline()
        state = line[15:-1]
        line = f.readline()
        line = f.readline()

        instructions: dict[str, str] = {}

        while line and len(line) > 1:
            instructions[line[:5]] = line[-2]
            line = f.readline()

        zero_index = 0
        # print(f"{0}: {''.join(state)}, {zero_index}")

        value = 0
        for i in range(len(state)):
            if state[i] == "#":
                value += i - zero_index

        previous_values = [0, 0, 0, 0, value]

        c = 0
        while True:
            state = ("." * 4) + state + ("." * 4)
            zero_index += 4
            new_state = [c for c in state]
            for i in range(2, len(state) - 2):
                # print(f"Checking {state[i-2:i+3]} - {instructions.get(state[i-2:i+3], '.')}")
                if state[i-2:i+3] in instructions:
                    new_state[i] = instructions[state[i-2:i+3]]
                else:
                    new_state[i] = "."

            start = new_state.index("#")
            end = len(new_state) - 1 - new_state[::-1].index("#")
            state = "".join(new_state)[start:end+1]
            zero_index -= start
            # print(f"{c+1}: {''.join(state)}, {zero_index}")
            new_value = 0
            for i in range(len(state)):
                if state[i] == "#":
                    new_value += i - zero_index

            previous_values.pop(0)
            previous_values.append(new_value - value)

            c += 1

            if all(v == previous_values[0] for v in previous_values):
                return new_value + (50000000000 - c) * previous_values[0]

            value = new_value


print(solution_part1())
print(solution_part2())
