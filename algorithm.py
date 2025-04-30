import heapq
import copy
from game import G1, G2

class Node:
    """
    Represents a node in the A* search graph for the ball sorting puzzle.

    Attributes:
        state (BallSorter): The current game state.
        parent (Node): The parent node representing the previous game state.
        prev_move (tuple): The move that led from the parent state to the current state.
        g (int): The cost from the start node to this node (number of moves so far).
        h (int): The heuristic estimate of the remaining cost to reach the goal.
        f (int): The total estimated cost (f = g + h).
    """
    def __init__(self, state, prev_move, parent=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.prev_move = prev_move
        self.g = g  # Cost so far
        self.h = h  # Heuristic
        self.f = g + h

    def __lt__(self, other):
        return self.f < other.f

def a_star(start_state, heuristic_fn):
    """
    Performs A* search to solve the ball sorting puzzle.

    Args:
        start_state (BallSorter): The initial state of the game.
        heuristic_fn (function): A function that takes a game state and returns an estimated cost to the goal.

    Returns:
        tuple[list[tuple], int]: A tuple containing:
            - A list of moves (as tuples) representing the shortest path to the goal state.
            - The number of explored states.
        Returns None if no solution is found.
    """
    open_list = []
    heapq.heappush(open_list, Node(start_state, None, parent=None, g=0, h=heuristic_fn(start_state)))
    closed_set = set()

    while open_list:
        current_node = heapq.heappop(open_list)

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

