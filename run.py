import sys
import pickle
import json
from algorithm import *
from game import *


def main():
    with open("games.pickle", "rb") as pf:
       games = pickle.load(pf)

    res = []
    for game in games:
        print(game)
        path, score = a_star(game)
        print(score)
        res.append(score)

    with open("results.json", "w") as of:
        json.dump({"Heuristic 1": res}, of)



def plot():
    import matplotlib.pyplot as plt

    with open("results.json", "r") as in_f:
        res = json.load(in_f)

    plt.boxplot(res.values(), tick_labels=list(res.keys()))
    plt.xlabel("Heuristic Function")
    plt.ylabel("States Explored")
    plt.title("Ball Sorter Heuristic Performance")
    plt.show()

if __name__ == "__main__":
    if sys.argv[1] == "run":
        main()
    elif sys.argv[1] == "plot":
        plot()
