import os
from typing import Literal

class Agent:
    def __init__(self, type: Literal["E", "G"], x: int, y: int, ap: int = 3):
        self.type = type
        self.x = x
        self.y = y
        self.hp = 200
        self.ap = ap

    def move(self, grid: list[list[str]]):
        enemy_type = "G" if self.type == "E" else "E"

        # Don't move if already next to an enemy
        starting_neighbors =  set([(self.x, self.y - 1), (self.x - 1, self.y), (self.x + 1, self.y), (self.x, self.y + 1)])
        if any(grid[n[1]][n[0]] == enemy_type for n in starting_neighbors):
            return

        # Find nearest valid square using BFS
        destination: tuple[int, int, int] = (9999999, 9999999, 9999999)
        queue: list[tuple[int, int, int]] = [(self.x, self.y, 0)]
        visited: set[tuple[int, int]] = set([(self.x, self.y)])
        while len(queue) > 0:
            current = queue.pop(0)
            if current[-1] > destination[-1]:
                break

            # if there's an enemy in range and it's closer, update destination
            neighbors = [(current[0], current[1] - 1), (current[0] - 1, current[1]), (current[0] + 1, current[1]), (current[0], current[1] + 1)]
            if any(grid[y][x] == enemy_type for x, y in neighbors) and (current[1] < destination[1] or (current[1] == destination[1] and current[0] < destination[0])):
                destination = current

            # add valid neighbors to queue
            for n in neighbors:
                if n not in visited and grid[n[1]][n[0]] == ".":
                    queue.append((n[0], n[1], current[-1] + 1))
                    visited.add(n)

        # If no enemies are reachable, do nothing
        if destination == (9999999, 9999999, 9999999):
            return

        # Find best starting square using BFS
        starting_square: tuple[int, int] = (9999999, 9999999)
        queue: list[tuple[int, int, int]] = [destination]
        visited: set[tuple[int, int]] = set([(destination[0], destination[1])])
        while len(queue) > 0:
            current = queue.pop(0)
            if current[-1] == 0:
                break

            if (current[0], current[1]) in starting_neighbors and (current[1] < starting_square[1] or (current[1] == starting_square[1] and current[0] < starting_square[0])):
                starting_square = (current[0], current[1])

            # add valid neighbors to queue
            for n in [(current[0], current[1] - 1), (current[0] - 1, current[1]), (current[0] + 1, current[1]), (current[0], current[1] + 1)]:
                if n not in visited and grid[n[1]][n[0]] == ".":
                    queue.append((n[0], n[1], current[-1] - 1))
                    visited.add(n)

        grid[self.y][self.x] = "."
        self.x = starting_square[0]
        self.y = starting_square[1]
        grid[self.y][self.x] = self.type

    def attack(self, grid: list[list[str]], agents):
        enemy_type = "G" if self.type == "E" else "E"

        # attack if next to an enemy
        starting_neighbors =  [(self.x, self.y - 1), (self.x - 1, self.y), (self.x + 1, self.y), (self.x, self.y + 1)]
        min_neighbor = (999999, 999999)
        min_hp = 999999
        for p in starting_neighbors:
            if p in agents and agents[p].type == enemy_type and (agents[p].hp < min_hp or (agents[p].hp == min_hp and \
               (agents[p].y < min_neighbor[1] or (agents[p].y == min_neighbor[1] and agents[p].x < min_neighbor[0])))):
                min_neighbor = p
                min_hp = agents[p].hp

        if min_neighbor in agents:
            agents[min_neighbor].hp -= self.ap
            if agents[min_neighbor].hp <= 0:
                grid[min_neighbor[1]][min_neighbor[0]] = "."
                return agents.pop(min_neighbor).type


def solution_part1(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
    with open(fname, "r") as f:
        grid = [[c for c in line[:-1]] for line in f.readlines()]
        agents: dict[tuple[int, int], Agent] = {}

        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] in ("E", "G"):
                    agents[(x, y)] = Agent(grid[y][x], x, y)

        round = 0
        while True:
            agent_positions = [p for p in agents]

            agent_positions.sort(key=lambda p: p[1] * 100000 + p[0])

            for j in range(len(agent_positions)):
                p = agent_positions[j]
                if p not in agents:
                    continue
                a = agents[p]
                a.move(grid)
                if (a.x, a.y) != p:
                    agents[(a.x, a.y)] = a
                    agents.pop(p)

                killed = a.attack(grid, agents)
                if killed is not None and all(b.type == a.type for b in agents.values()):
                    r = round + 1 if j == len(agent_positions) - 1 else round
                    return r * sum([a.hp for a in agents.values()])

            round += 1


def solution_part2(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
    with open(fname, "r") as f:
        original_grid = [[c for c in line[:-1]] for line in f.readlines()]
        agents: dict[tuple[int, int], Agent] = {}

        elf_ap = 4
        while True:
            grid = [[x for x in row] for row in original_grid]
            agents: dict[tuple[int, int], Agent] = {}
            for y in range(len(grid)):
                for x in range(len(grid[y])):
                    if grid[y][x] in ("E", "G"):
                        agents[(x, y)] = Agent(grid[y][x], x, y, 3 if grid[y][x] == "G" else elf_ap)

            round = 0
            while True:
                agent_positions = [p for p in agents]
                agent_positions.sort(key=lambda p: p[1] * 100000 + p[0])

                for j in range(len(agent_positions)):
                    p = agent_positions[j]
                    if p not in agents:
                        continue
                    a = agents[p]
                    a.move(grid)
                    if (a.x, a.y) != p:
                        agents[(a.x, a.y)] = a
                        agents.pop(p)

                    killed = a.attack(grid, agents)
                    if killed == "E":
                        break

                    if killed == "G" and all(b.type == a.type for b in agents.values()):
                        r = round + 1 if j == len(agent_positions) - 1 else round
                        return r * sum([a.hp for a in agents.values()])
                else:
                    round += 1
                    continue
                break

            elf_ap += 1


print(solution_part1())
print(solution_part2())
