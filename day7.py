import os

class Step:
    def __init__(self, name: str):
        self.name = name
        self.prereqs: set[Step] = set()
        self.children: set[Step] = set()
        self.finish_time: int | None = None

def solution_part1(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
    with open(fname, "r") as f:
        steps: dict[str, Step] = {}
        for line in f:
            spl = line.split()
            prereq_step = spl[1]
            next_step = spl[-3]
            if prereq_step not in steps:
                steps[prereq_step] = Step(prereq_step)
            if next_step not in steps:
                steps[next_step] = Step(next_step)
            prereq_step = steps[prereq_step]
            next_step = steps[next_step]
            prereq_step.children.add(next_step)
            next_step.prereqs.add(prereq_step)

        available_steps = [s for s in steps if len(steps[s].prereqs) == 0]
        result: list[str] = []

        while len(available_steps) > 0:
            available_steps.sort()
            current_step = available_steps.pop(0)
            result.append(current_step)
            current_step = steps[current_step]
            for child in current_step.children:
                child.prereqs.remove(current_step)
                if len(child.prereqs) == 0:
                    available_steps.append(child.name)
        return "".join(result)


def solution_part2(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt", n_workers: int = 5, delay: int = 60):
    with open(fname, "r") as f:
        steps: dict[str, Step] = {}
        for line in f:
            spl = line.split()
            prereq_step = spl[1]
            next_step = spl[-3]
            if prereq_step not in steps:
                steps[prereq_step] = Step(prereq_step)
            if next_step not in steps:
                steps[next_step] = Step(next_step)
            prereq_step = steps[prereq_step]
            next_step = steps[next_step]
            prereq_step.children.add(next_step)
            next_step.prereqs.add(prereq_step)

        available_steps = [s for s in steps if len(steps[s].prereqs) == 0]
        pending_steps: set[str] = set()
        completed_steps: set[str] = set()

        t = 0
        while len(completed_steps) < len(steps):
            # figure out if any steps are done
            for s in [x for x in pending_steps]:
                current_step = steps[s]
                if current_step.finish_time == t:
                    pending_steps.remove(s)
                    completed_steps.add(s)
                    for child in current_step.children:
                        child.prereqs.remove(current_step)
                        if len(child.prereqs) == 0:
                            available_steps.append(child.name)

            available_steps.sort()
            while len(available_steps) > 0 and len(pending_steps) < n_workers:
                current_step = available_steps.pop(0)
                pending_steps.add(current_step)
                steps[current_step].finish_time = t + delay + 1 + ord(current_step) - ord("A")
            t += 1
        return t - 1




print(solution_part1())
print(solution_part2())
