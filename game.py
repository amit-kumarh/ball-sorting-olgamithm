from enum import Enum


class Color(Enum):
    RED = 0
    ORANGE = 1
    YELLOW = 2
    GREEN = 3
    BLUE = 4
    INDIGO = 5
    VIOLET = 6


class BallSorter:
    def __init__(self, initial_config, max_in_col) -> None:
        self.num_cols = len(initial_config)
        self.max_in_col = max_in_col
        self.state = initial_config

    def __repr__(self) -> str:
        out = ""
        for line in self.state:
            out += "| "
            if len(line) == 0:
                out += "   |"
            for c in line:
                out += c.name + " | "
            out += "\n"
        return out

    def is_valid_move(self, src, dest):
        # check top of src matches top of dest
        if (
            len(self.state[src]) > 0
            and (
                len(self.state[dest]) == 0
                or self.state[src][-1] == self.state[dest][-1]
            )
            and len(self.state[dest]) < self.max_in_col
        ):
            return True
        return False

    def move(self, src, dest):
        self.state[dest].append(self.state[src].pop())

    def done(self):
        for col in self.state:
            if len(set(col)) > 1:
                return False
        return True

    def get_neighbors(self):
        neighbors = []
        for si, _ in enumerate(self.state):
            for di, _ in enumerate(self.state):
                if si == di:
                    continue
                if self.is_valid_move(si, di):
                    neighbors.append((si, di))
        return neighbors

    def heuristic(self):
        score = 0

        for col in self.state:
            unique_colors = set(col)
            if len(unique_colors) > 1:
                score += len(col) + len(unique_colors)

        return score


## EXAMPLE GAMES
G1 = BallSorter(
    [
        [Color.BLUE, Color.ORANGE, Color.RED, Color.BLUE],
        [Color.ORANGE, Color.ORANGE, Color.RED, Color.BLUE],
        [Color.RED, Color.BLUE, Color.ORANGE, Color.RED],
        [],
        [],
    ],
    4,
)

def test_solve():
    print(G1)
    G1.move(0, 3)
    G1.move(1, 3)
    G1.move(0, 4)
    G1.move(1, 4)
    G1.move(2, 4)
    G1.move(0, 1)
    G1.move(2, 1)
    G1.move(0, 3)
    G1.move(2, 3)
    G1.move(2, 4)
    print(G1)
    print(G1.done())
