import random
from abc import ABCMeta, abstractmethod
import pdb
from minesweeper import *
from bokeh.plotting import figure, show, output_file
import numpy as np
from sklearn.linear_model import Ridge
from itertools import compress
import matplotlib.pyplot as plt
import csv
from Agent import *
import time

WIDTH = 25
HEIGHT = 25
MINES_COUNT = 125
# viz = GameVisualizer(2)

ai = LoadModel("res/model.pkl15046")
config = ai.config
game = ai.game

lstSteps = []
counterWins = 0
games = []
GAMES_COUNT = 100
counter = 0

time.sleep(4)

# Define the file name for the CSV file
csv_file = "game_data.csv"

# Open the CSV file in write mode and create a CSV writer object
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(["Game", "Moves", "Outcome"])  # Adjust headers as needed

    while counter < GAMES_COUNT:
        stepsCount = 0
        game = Game(config)
        ai.ResetAgentState(game)
        board = None
        flags = []

        # if viz:
        #     viz.start(game)

        while not game.is_game_over():
            coords = ai.next()
            result = game.select(*coords)
            flags = ai.get_flags()
            board = game.board

            if result is None:
                continue

            if not result.explosion:
                stepsCount += 1
                ai.update(result)
                game.set_flags(ai.get_flags())

                if game.num_exposed_squares == game.num_safe_squares:
                    outcome = "Win"
                    counterWins += 1
                else:
                    outcome = "Lose"
                # if viz:
                #     viz.update(game)
    
        # if viz:
        #     viz.finish()

        counter += 1
        lstSteps.append(stepsCount)
        games.append(counter)

        # Count flagged and correctly flagged tiles
        marked, correct = game.count_flagged_tiles()
        correctly_marked = sum(1 for x, y in flags if game.board[x][y] == True)

        print("iteration", counter, "outcome:", outcome, "steps:", stepsCount, "marked", marked, "correct", correct)

        # Write game data to CSV
        writer.writerow([counter, stepsCount, outcome])

# Print a message indicating the CSV file has been created
print(f"Game data has been saved to {csv_file}")

print(f"Accuracy: won {counterWins} games out of {GAMES_COUNT} ")
print(f"Average steps {sum(lstSteps)/GAMES_COUNT}")

# Calculate cumulative steps
cumulative_steps = np.cumsum(lstSteps)
for  i in range(GAMES_COUNT):
    cumulative_steps[i] += cumulative_steps[i] / (i + 1)

plt.plot(games, cumulative_steps)
plt.title('Cumulative Steps vs Number of Games')
plt.xlabel('Number of Games')
plt.ylabel('Cumulative Steps')
plt.show()
