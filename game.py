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

    def is_valid_move(self, src, dest):
        # check top of src matches top of dest
        if self.state[src][-1] == self.state[dest][-1] and len(self.state[dest]) < self.max_in_col:
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
        pass
        
