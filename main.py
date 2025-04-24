import heapq
import copy
from game import BallSorter, G1, G2, generate_tube_puzzle
from collections import namedtuple



class Node:
    def __init__(self, state, prev_move, parent=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.prev_move = prev_move
        self.g = g  # Cost so far
        self.h = h  # Heuristic
        self.f = g + h

    def __lt__(self, other):
        return self.f < other.f

def a_star(start_state):
    open_list = []
    heapq.heappush(open_list, Node(start_state, None, parent=None, g=0, h=start_state.heuristic()))
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
            h = new_node.state.heuristic()
            neighbor_node = Node(new_node.state, neighbor_move, parent=current_node, g=g, h=h)

            heapq.heappush(open_list, neighbor_node)

    return None  # No path found

game = generate_tube_puzzle(15, 4)
print(game)
print(*a_star(game), sep='\n\n')
