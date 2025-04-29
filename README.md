# Ball Sort Puzzle Solver

### Setup

### Background

The Ball Sort Puzzle is a type of logic game popularized in smartphone apps. It involves a number of bins filled with colored balls, and the objective is to rearrange the balls so that each bin contains balls of only one color or is left empty.

The rules of the game are as follows:

1. Each bin has a fixed maximum capacity, typically equal to the number of balls of a single color.
2. A ball can only be moved if it is the top ball in a bin (following the last-in, first-out principle).
3. A ball can be moved to another bin if the destination bin is either empty or if the top ball of the destination bin matches the color of the ball being moved and the bin is not yet full.

The ball sort puzzle shares some similarities with classic problems like the Tower of Hanoi, requiring careful planning to avoid "locking" balls into unsolvable states.

### Implementation

Our solver uses the A* algorithm to find the optimal sequence of moves— that is, the shortest series of legal moves — needed to solve any given starting configuration. We apply the A* search algorithm, a pathfinding and graph traversal technique known for its efficiency in finding the least-cost path to a goal. A\* considers both:

- The cost so far (the number of moves made) and
- A heuristic estimate (an estimate of how many additional moves may be needed to reach the solved state).

By combining these two factors, A\* is able to explore the most promising sequences of moves first, greatly reducing the number of configurations it needs to check compared to uninformed search methods.
