import os

def solution_part1(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
    with open(fname, "r") as f:
        spl = f.readline().split()
        n_players, n_marbles = int(spl[0]), int(spl[6])

        marbles = [0]
        player_scores = [0 for _ in range(n_players)]
        current_player = 0
        current_marble = 0

        for current_marble_score in range(1, n_marbles + 1):
            if current_marble_score % 23 == 0:
                player_scores[current_player] += current_marble_score
                player_scores[current_player] += marbles.pop(current_marble - 7)
                current_marble = (current_marble - 6) % len(marbles) if current_marble - 7 < 0 else current_marble - 7
            else:
                new_index = (current_marble + 2) % len(marbles)
                marbles.insert(new_index, current_marble_score)
                current_marble = new_index

            current_player = (current_player + 1) % n_players

        return max(player_scores)

class Marble:
    def __init__(self, score: int):
        self.score = score
        self.prev: Marble
        self.next: Marble

def solution_part2(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
    with open(fname, "r") as f:
        spl = f.readline().split()
        n_players, n_marbles = int(spl[0]), int(spl[6]) * 100

        marbles = [Marble(0), Marble(1), Marble(2)]
        marbles[0].next = marbles[2]
        marbles[1].next = marbles[0]
        marbles[2].next = marbles[1]
        marbles[0].prev = marbles[1]
        marbles[1].prev = marbles[2]
        marbles[2].prev = marbles[0]

        player_scores = [0 for _ in range(n_players)]
        current_player = 0
        current_marble: Marble = marbles[2]

        for current_marble_score in range(3, n_marbles + 1):
            if current_marble_score % 23 == 0:
                player_scores[current_player] += current_marble_score
                for _ in range(7):
                    current_marble = current_marble.prev
                player_scores[current_player] += current_marble.score
                current_marble.prev.next = current_marble.next
                current_marble.next.prev = current_marble.prev
                current_marble = current_marble.next
            else:
                new_marble = Marble(current_marble_score)
                new_marble.prev = current_marble.next
                new_marble.next = current_marble.next.next
                new_marble.prev.next = new_marble
                new_marble.next.prev = new_marble
                current_marble = new_marble
            current_player = (current_player + 1) % n_players

        return max(player_scores)

print(solution_part1())
print(solution_part2())
