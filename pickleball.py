import game
import pickle
import sys

def play_pickleball(num_games, num_tubes, balls_per_tube):
    games = []
    for _ in range(num_games):
        games.append(game.generate_tube_puzzle(num_tubes, balls_per_tube))

    with open('games.pickle', 'wb') as file:
        pickle.dump(games, file)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: pickleball <num_games> <num_tubes> <balls_per_tube>")
        sys.exit(1)

    play_pickleball(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))

