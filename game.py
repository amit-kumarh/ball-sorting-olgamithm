from enum import Enum
import random
import collections


class Color(Enum):
    RED = 0
    ORANGE = 1
    YELLOW = 2
    GREEN = 3
    BLUE = 4
    CYAN = 5
    VIOLET = 6
    PINK = 7
    MINT = 8
    GRAY = 9
    BLACK = 10
    WHITE = 11
    INDIGO = 12
    FUCHSIA= 13
    AZURE = 14
    SAGE = 15
    CRIMSON = 16
    CARDINAL = 17
    MARIGOLD = 18
    COBALT = 19


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
        good_col = lambda col: (len(set(col)) == 1 and len(col) == self.max_in_col) or (len(col) == 0)
        return all(good_col(col) for col in self.state)

    def get_neighbors(self):
        neighbors = []
        for si, _ in enumerate(self.state):
            for di, _ in enumerate(self.state):
                if si == di:
                    continue
                if self.is_valid_move(si, di):
                    neighbors.append((si, di))
        return neighbors
    
    def unique_colors(self):
        """
        Heuristic based on number of unique colors in each column.

        Sums up unique colors in each non-finished column.
        """
        unique = 0
        for tube in self.state:
            if not tube:
                continue

            # if a column is complete, no penalty
            if len(set(tube)) == 1 and len(tube) == self.max_in_col:
                continue

            # add number of transitions
            unique += len(set(tube))
                    
        return unique
    
    def misplaced_balls(self):
        """
        Heuristic based on misplaced colors.

        Sums up balls that do not match the majority color in each column.
        """
        heuristic = 0
        for tube in self.state:
            if not tube:
                continue

            if len(tube) < self.max_in_col:
                heuristic += 1

            # if all balls are the same, no penalty
            if len(set(tube)) == 1:
                continue

            # penalize number of balls that don't match the majority color in the tube
            most_frequent = collections.Counter(tube).most_common(1)[0][0]
            for cost, ball in zip(range(4,0,-1), tube):
                if ball != most_frequent:
                    heuristic += cost

        return heuristic

    def transitions(self):
        """
        Heuristic based on transitions.

        Sums up transitions between balls.
        """
        heuristic = 0
        for tube in self.state:
            if not tube:
                continue

            # if all balls are the same, no penalty
            if len(set(tube)) == 1:
                if len(tube) < self.max_in_col:
                    heuristic += 1
                continue

            # add number of transitions
            for i in range(len(tube)-1):
                if tube[i] != tube[i+1]:
                    heuristic += 1

        return heuristic

    def unique_and_length(self, col_weight, color_weight):
        # Length of unsolved column + number of unique colors 
        score = 0

        for col in self.state:
            if not col:
                continue

            unique_colors = set(col)
            if len(unique_colors) != 1:
                score += col_weight*len(col) + color_weight*len(unique_colors)
            elif len(col) < self.max_in_col:
                score += 1

        return score

def generate_tube_puzzle(num_tubes: int, balls_per_tube: int) -> BallSorter:
    if num_tubes < 3:
        raise ValueError("Number of tubes must be at least 3 to generate a solvable puzzle.")

    # Calculate the number of colors.  We want each color to appear 4 times,
    # and we need at least one empty tube to make the puzzle solvable.
    num_colors = num_tubes - 2

    # Ensure we don't try to use more colors than we have defined.
    if num_colors > len(Color):
        raise ValueError(f"Not enough colors available.  Cannot generate puzzle with {num_tubes} tubes.")

    # Create a list of all the balls, 4 of each color.
    balls = []
    for color_index in range(num_colors):
        color = Color(color_index)
        balls.extend([color] * balls_per_tube)

    # Shuffle the balls randomly.
    random.shuffle(balls)

    # Distribute the balls into the tubes.
    tubes = [[] for _ in range(num_tubes)]
    ball_index = 0
    for tube_index in range(num_tubes - 2):  # Leave the last two tubes empty
        for _ in range(balls_per_tube):
            tubes[tube_index].append(balls[ball_index])
            ball_index += 1

    return BallSorter(tubes, balls_per_tube)


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

G2 = BallSorter(
    [
        [Color.GREEN, Color.MINT, Color.PINK, Color.VIOLET],
        [Color.GRAY, Color.GRAY, Color.PINK, Color.BLUE],
        [Color.GREEN, Color.ORANGE, Color.VIOLET, Color.RED],
        [Color.GRAY, Color.BLUE, Color.CYAN, Color.BLUE],
        [Color.BLUE, Color.CYAN, Color.MINT, Color.RED],
        [Color.PINK, Color.RED, Color.ORANGE, Color.CYAN],
        [Color.CYAN, Color.MINT, Color.ORANGE, Color.RED],
        [Color.MINT, Color.PINK, Color.GRAY, Color.GREEN],
        [Color.VIOLET, Color.GREEN, Color.VIOLET, Color.ORANGE],
        [],
        [],
    ],
    4,
)
