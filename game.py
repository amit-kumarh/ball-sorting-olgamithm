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
    """
    Represents a ball sort puzzle game state.

    Attributes:
        num_cols (int): The number of columns in the game.
        max_in_col (int): The maximum number of balls that each column can hold
        state (List[List[Color]]): The game state, where each list represents a 
            column containing `Color` objects.
    """
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
        """
        Checks if moving the top ball from the source column to the destination column is valid.

        Args:
            src (int): Index of the source column.
            dest (int): Index of the destination column.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
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
        """
        Moves the top ball from the source column to the destination column.
        """
        self.state[dest].append(self.state[src].pop())

    def done(self):
        """
        Checks whether the puzzle is solved.
        """
        good_col = lambda col: (len(set(col)) == 1 and len(col) == self.max_in_col) or (len(col) == 0)
        return all(good_col(col) for col in self.state)

    def get_neighbors(self):
        """
        Generates all valid moves from the current state.
        """
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
        Heuristic based on the number of unique colors in each column.
        For each incomplete or mixed column, adds the number of unique colors as penalty
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
        Heuristic that penalizes misplaced balls in each column.
        For each column, adds a penalty for balls that do not match the most frequent color.
        Also adds a small penalty if the column is not full.
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
        Heuristic that penalizes color transitions between adjacent balls in each column.
        Adds 1 point for each transition where two adjacent balls are different.
        Also adds a small penalty for incomplete uniform columns.
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
        """
        Weighted heuristic combining column length and color diversity.

        For each non-uniform column, adds:
            - (col_weight * number of balls), and
            - (color_weight * number of unique colors).
        Adds a small penalty for incomplete uniform columns.
        """
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
    """
    Generates a randomized, solvable ball sort puzzle.

    Args:
        num_tubes (int): Total number of tubes in the puzzle.
        balls_per_tube (int): Number of balls each tube can hold. Each color will appear this many times.

    Returns:
        BallSorter: An initialized BallSorter instance with the generated puzzle state.
    """
    
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
