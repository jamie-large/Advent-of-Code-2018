import os
from typing import Literal

Direction = Literal["^", ">", "v", "<"]
TURNS = ["L", "S", "R"]

class Cart:
    def __init__(self, x: int, y: int, dir: Direction):
        self.x: int = x
        self.y: int = y
        self.dir: Direction = dir
        self.turn_index: int = 0

    def adjust_position(self, grid: list[list[str]]):
        track = grid[self.y][self.x]
        if self.dir == "^":
            if track == "|":
                self.y -= 1
            elif track == "/":
                self.x += 1
                self.dir = ">"
            elif track == "\\":
                self.x -= 1
                self.dir = "<"
            elif track == "+":
                if TURNS[self.turn_index] == "L":
                    self.x -= 1
                    self.dir = "<"
                elif TURNS[self.turn_index] == "S":
                    self.y -= 1
                elif TURNS[self.turn_index] == "R":
                    self.x += 1
                    self.dir = ">"
                self.turn_index = (self.turn_index + 1) % 3
        elif self.dir == ">":
            if track == "-":
                self.x += 1
            elif track == "/":
                self.y -= 1
                self.dir = "^"
            elif track == "\\":
                self.y += 1
                self.dir = "v"
            elif track == "+":
                if TURNS[self.turn_index] == "L":
                    self.y -= 1
                    self.dir = "^"
                elif TURNS[self.turn_index] == "S":
                    self.x += 1
                elif TURNS[self.turn_index] == "R":
                    self.y += 1
                    self.dir = "v"
                self.turn_index = (self.turn_index + 1) % 3
        elif self.dir == "v":
            if track == "|":
                self.y += 1
            elif track == "/":
                self.x -= 1
                self.dir = "<"
            elif track == "\\":
                self.x += 1
                self.dir = ">"
            elif track == "+":
                if TURNS[self.turn_index] == "L":
                    self.x += 1
                    self.dir = ">"
                elif TURNS[self.turn_index] == "S":
                    self.y += 1
                elif TURNS[self.turn_index] == "R":
                    self.x -= 1
                    self.dir = "<"
                self.turn_index = (self.turn_index + 1) % 3
        elif self.dir == "<":
            if track == "-":
                self.x -= 1
            elif track == "/":
                self.y += 1
                self.dir = "v"
            elif track == "\\":
                self.y -= 1
                self.dir = "^"
            elif track == "+":
                if TURNS[self.turn_index] == "L":
                    self.y += 1
                    self.dir = "v"
                elif TURNS[self.turn_index] == "S":
                    self.x -= 1
                elif TURNS[self.turn_index] == "R":
                    self.y -= 1
                    self.dir = "^"
                self.turn_index = (self.turn_index + 1) % 3

def solution_part1(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
    with open(fname, "r") as f:
        grid = [[c for c in line[:-1]] for line in f]
        carts: list[Cart] = []
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] == ">":
                    carts.append(Cart(x, y, ">"))
                    grid[y][x] = "-"
                elif grid[y][x] == "<":
                    carts.append(Cart(x, y, "<"))
                    grid[y][x] = "-"
                elif grid[y][x] == "^":
                    carts.append(Cart(x, y, "^"))
                    grid[y][x] = "|"
                elif grid[y][x] == "v":
                    carts.append(Cart(x, y, "v"))
                    grid[y][x] = "|"

        while True:
            carts.sort(key = lambda c: c.y * 100000 + c.x)
            for c in carts:
                c.adjust_position(grid)
                for i in range(len(carts)):
                    if c != carts[i] and c.x == carts[i].x and c.y == carts[i].y:
                        return c.x, c.y



def solution_part2(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
    with open(fname, "r") as f:
        grid = [[c for c in line[:-1]] for line in f]
        carts: list[Cart] = []
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] == ">":
                    carts.append(Cart(x, y, ">"))
                    grid[y][x] = "-"
                elif grid[y][x] == "<":
                    carts.append(Cart(x, y, "<"))
                    grid[y][x] = "-"
                elif grid[y][x] == "^":
                    carts.append(Cart(x, y, "^"))
                    grid[y][x] = "|"
                elif grid[y][x] == "v":
                    carts.append(Cart(x, y, "v"))
                    grid[y][x] = "|"

        while len(carts) > 1:
            carts.sort(key = lambda c: c.y * 100000 + c.x)
            to_remove = []
            for i in range(len(carts)):
                carts[i].adjust_position(grid)
                for j in [x for x in range(len(carts)) if x not in to_remove]:
                    if i != j and carts[i].x == carts[j].x and carts[i].y == carts[j].y:
                        to_remove.append(i)
                        to_remove.append(j)
            to_remove.sort(reverse=True)
            for i in to_remove:
                carts.pop(i)

        return carts[0].x, carts[0].y


print(solution_part1())
print(solution_part2())
