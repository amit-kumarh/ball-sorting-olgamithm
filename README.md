# Ball Sort Puzzle Solver

Use A* to solve the ball sorting puzzle.

## Setup

To install the project dependencies, run

```
pip install -r requirements.txt
```

This project has 4 Python files that break down as follows:
- `game.py` - this file contains the logic to simulate the ball sorting puzzle game. It also contains functions to generate new games, a few constant example games, and all of our heuristic calculations
- `algorithm.py` - contains the main A* implementation
- `pickleball.py` - given a number of tubes, tube height, and number of games, generate and pickle a set of game starting configurations
- `run.py` - run and plot results for the set of games produced by `pickleball.py`. Note that there are two subcommands to this script
    - `run.py run` runs the algorithm and saves the explored states and path length for each test game into `results.json`
    - `run.py plot` loads the `results.json` file and plots the resulting curves.
    - The reason for this separation is we recommmend running the model using something like `pypy3` which performs much faster than base Python - but `matplotlib` is not compatible with `pypy`, so that section needs to be run with regular Python. 


## Background

The Ball Sort Puzzle is a type of logic game popularized in smartphone apps. It involves a number of bins filled with colored balls, and the objective is to rearrange the balls so that each bin contains balls of only one color or is left empty.

The rules of the game are as follows:

1. Each bin has a fixed maximum capacity, typically equal to the number of balls of a single color.
2. A ball can only be moved if it is the top ball in a bin (following the last-in, first-out principle).
3. A ball can be moved to another bin if the destination bin is either empty or if the top ball of the destination bin matches the color of the ball being moved and the bin is not yet full.

The ball sort puzzle shares some similarities with classic problems like the Tower of Hanoi, requiring careful planning to avoid "locking" balls into unsolvable states.

// INSERT PROOF

### Algorithm

Our solver uses the A* algorithm to find the optimal sequence of moves— that is, the shortest series of legal moves — needed to solve any given starting configuration. We apply the A* search algorithm, a pathfinding and graph traversal technique known for its efficiency in finding the least-cost path to a goal. A\* considers both:

- The cost so far (the number of moves made) and
- A heuristic estimate (an estimate of how many additional moves may be needed to reach the solved state).

Unlike simpler search methods like Dijkstra's algorihtm, which only considers the cost to *reach* a given path (which in this case is equal to the depth!), the addition of a heuristic allows A* to prioritizes both paths that are cheap to take *and* are likelier to converge on a solution quicker.

## Application to Ball Sorting

Being that A* is a graph traversal algorithm, we had to do some translation to map graph elements to game representation in order to apply the algorithm, since we don't have a precomputed graph of each possible game state.

1. Node -> Game State - We used a custom Python class to represent our game state, consisting of primarily a list of lists of variants of a Color enum. The class also includes some useful helper functions that allow us to validate and perform moves, check for win conditions, and evaluate various heuristic metrics about each state.

2. Edge -> Legal Game Move - at each branch point, we find all of the potential neighbors by analyzing the set of all possible moves.

3. Edge Weight -> A* is theoretically supposed to be performed on a weighted graph. However, in this case, each move costs the same as any other move - there are no cheaper moves, so all of our edge weights on our graph are taken to be a constant 1.

Additionally, there are a few other elements we had to implement:
- A* requires us to choose at each iteration the state with the lowest estimated cost (depth + heuristic). We used Python's heap queue for this in order to try and minimize the cost of loading and storing from thie sorted list.
- Each state additoinally tracks a little bit of metadata about itself - primarily its parent, and the move that led up to it - to allow us to later reconstruct the solution path.
- Lastly, we track which states have been popped off of our priority with a Python `set` to ensure we don't visit a state multiple times.

// INSERT HEURISTIC DESIGN

// INSERT DIAGRAMS FROM THE SLIDES

## Results

## Analysis

## Next Steps

This initial exploration showed a lot of promise, and there are certianly avenues for improvement we are excited about.

1. Heuristic Design - One of the things we realized over the course of the course of this project was that it was very difficult to intuitively compare different heuristics to each other and predict which one was better without implementing and testing it, which was an expensive process both computationally, and in terms of implementation time. As a result, this limited the number and variety of heuristics we were able to try, and ultimately we feel there's still lots of available exploration in this space to improve the algorithm performance.

2. Algorithm Efficiency - When we wrote the algorihm, we optimized for factors like readability, development time, and reliability, as we wanted to minimize the number of code/implementation hurdles we ran into in order to focus on our more conceptual learning goals. However, this trade-off was made primarily at the cost of efficiency - our algorithm runs quite slowly relative to the number of states it is exploring, which limited the number and complexity of the puzzles we were able to test. With mroe time, we believe there's plenty of opportunity to optimize our data structures and our algorithm implementation to tackle more complex variants of this puzzle.

3. Water Sorting? The ball sorting puzzle is one of two popular variants of this genre of puzzle, the other being the water sorting puzzle, which has the key difference that when one unit of water (vs a ball) is poured onto another of the same color, they join and become a 2 (or more) tall unit that must move as one. It'd be interesting to see how well our algorithm handles water sorting as opposed to ball sorting.

## Citations

[1] T. Ito, “Sorting Balls and Water: Equivalence and Computational Complexity,” Feb. 19, 2022.
