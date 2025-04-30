import heapq
import copy
from game import G1, G2

class Node:
    """
    Representation of a game state in the A* graph.

    Attributes:
        state: An instance of BallSorter representing the current state of the game.
        parent: An instance of BallSorter representing the previous state of the game in the sequence of moves.
        prev_move: A tuple representing the move made to go from the parent node to the current node.
    """
    def __init__(self, state, prev_move, parent=None, g=0, h=0):
        self.state = state # instance of BallSorter
        self.parent = parent
        self.prev_move = prev_move
        self.g = g  # Cost so far
        self.h = h  # Heuristic
        self.f = g + h

    def __lt__(self, other):
        return self.f < other.f

def a_star(start_state, heuristic_fn):
    open_list = []
    heapq.heappush(open_list, Node(start_state, None, parent=None, g=0, h=heuristic_fn(start_state)))
    closed_set = set()

    while open_list:
        current_node = heapq.heappop(open_list)
        # print(heuristic_fn(current_node.state))
        # print(current_node.state)

        if current_node.state.done():
            print(current_node.state)
            path = []
            while current_node:
                path.append(current_node.prev_move)
                current_node = current_node.parent
            return path[::-1], len(closed_set)+1  # Reverse path

        closed_set.add(current_node.state)

        for neighbor_move in current_node.state.get_neighbors():
            new_node = copy.deepcopy(current_node)
            new_node.state.move(*neighbor_move)

            if new_node.state in closed_set:
                continue

            g = new_node.g + 1
            h = heuristic_fn(new_node.state)
            neighbor_node = Node(new_node.state, neighbor_move, parent=current_node, g=g, h=h)

            heapq.heappush(open_list, neighbor_node)

    return None  # No path found

heuristics = [
    lambda s: s.misplaced_balls(),
    lambda s: s.heuristic_1(),
    lambda s: s.transitions(),
    lambda s: s.heuristic_4(col_weight=1, color_weight=1),
]

names = ["Heuristic 1", "Heuristic 2", "Heuristic 3", "Heuristic 4"]

# print(a_star(G1, heuristics[2]))
