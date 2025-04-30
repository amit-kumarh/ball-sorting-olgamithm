import sys
import pickle
import json
from algorithm import *
from game import *

heuristics = [
    lambda s: s.unique_and_length(col_weight=1, color_weight=1),
    lambda s: s.misplaced_balls(),
    # lambda s: s.transitions(),
    # lambda s: s.heuristic_1(),
]

names = ["Unique + Length", "Misplaced Balls", "Transitions", "Heuristic 4"]



def main():
    """
    Runs A* search on a set of pre-generated ball sorting games using multiple heuristics.
    """
    with open("games.pickle", "rb") as pf:
       games = pickle.load(pf)

    scores_dict = {}
    states_dict = {}
    for i, (heuristic, name) in enumerate(zip(heuristics, names)):
        scores = []
        states = []
        for j, game in enumerate(games):
            path, num_states = a_star(game, heuristic)
            print(f"heuristic {i}, game {j}, length of path: {len(path)}, number of states explored: {num_states}")
            states.append(num_states)
            scores.append(len(path))
        scores_dict[name] = scores
        states_dict[name] = states

    with open("results.json", "w") as of:
        json.dump([scores_dict, states_dict], of)

def plot():
    """
    Plots and summarizes the performance of each heuristic function.
    """
    import matplotlib.pyplot as plt
    import pandas as pd

    with open("results.json", "r") as in_f:
        scores_dict, states_dict = json.load(in_f)

    plt.boxplot(states_dict.values(), tick_labels=list(states_dict.keys()))
    plt.xlabel("Heuristic Function")
    plt.ylabel("States Explored")
    plt.title("Ball Sorter Heuristic Performance")
    plt.savefig("artifacts/states.png")
    plt.show()

    for k, v in states_dict.items():
        print(pd.Series(v).describe())

    print('='*50)

    for k, v in scores_dict.items():
        print(pd.Series(v).describe())

    plt.boxplot(scores_dict.values(), tick_labels=list(scores_dict.keys()))
    plt.xlabel("Heuristic Function")
    plt.ylabel("Number of moves to solved")
    plt.title("Ball Sorter Path Length")
    plt.savefig("artifacts/scores.png")
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: run.py {run|plot}\n\nPypy is recommended with run mode to increase performance")
        sys.exit(1)

    if sys.argv[1] == "run":
        main()
    elif sys.argv[1] == "plot":
        plot()
