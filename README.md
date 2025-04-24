# Ball Sort Puzzle Solver

### Setup

In order to run the solver, you need to create an instance of the initial game state of `BallSorter` class. Then pass this instance into the `a_star` function for it to return the shortest set of steps to solve that puzzle!

### Background

The Ball Sort Puzzle is a sorting game popularized by smartphone apps. The game consists of a set of tubes with colored balls in them, and the objective is sort the balls by color so each tube contains only one color of balls. Each tube acts as a stack -- the first ball in is the last ball out.

### Implementation

Our solver uses the A* algorithm to find the optimal path of moves to solve the puzzle. The A* algorithm is a heuristic pathfinding algorithm
