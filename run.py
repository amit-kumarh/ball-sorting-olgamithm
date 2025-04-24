import sys
import pickle
import json
from algorithm import *
from game import *


def main():
    with open("games.pickle", "rb") as pf:
       games = pickle.load(pf)

    scores_dict = {}
    states_dict = {}
    for heuristic, name in zip(heuristics, names):
        scores = []
        states = []
        for game in games:
            print(game)
            path, num_states = a_star(game)
            print(len(path), states)
            states.append(num_states)
            scores.append(len(path))
        scores_dict[name] = scores
        states_dict[name] = states

    with open("results.json", "w") as of:
        json.dump([scores_dict, states_dict], of)

def plot():
    import matplotlib.pyplot as plt

    with open("results.json", "r") as in_f:
        scores_dict, states_dict = json.load(in_f)

    plt.boxplot(states_dict.values(), tick_labels=list(states_dict.keys()))
    plt.xlabel("Heuristic Function")
    plt.ylabel("States Explored")
    plt.title("Ball Sorter Heuristic Performance")
    plt.show()

    plt.boxplot(scores_dict.values(), tick_labels=list(scores_dict.keys()))
    plt.xlabel("Heuristic Function")
    plt.ylabel("Number of moves to solved")
    plt.title("Ball Sorter Path Length")
    plt.show()

if __name__ == "__main__":
    if sys.argv[1] == "run":
        main()
    elif sys.argv[1] == "plot":
        plot()
