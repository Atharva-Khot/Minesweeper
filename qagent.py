import os

import numpy as np


class QLearningAgent:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.q_table_file = f"q_table_{grid_size}.npy"  # File to save/load Q-table
        if os.path.exists(self.q_table_file):
            self.q_table = np.load(self.q_table_file)  # Load Q-table if exists
        else:
            self.q_table = np.zeros((grid_size, grid_size, 2))  # Initialize Q-table
        self.alpha = 0.1  # learning rate
        self.gamma = 0.9  # discount factor
        self.epsilon = 0.9  # exploration-exploitation trade-off

    def choose_action(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.choice([0, 1])  # explore
        else:
            return np.argmax(self.q_table[state[0], state[1]])

    def update_q_table(self, state, action, reward, next_state):
        predict = self.q_table[state[0], state[1], action]
        target = reward + self.gamma * np.max(self.q_table[next_state[0], next_state[1]])
        self.q_table[state[0], state[1], action] += self.alpha * (target - predict)

    def save_q_table(self):
        np.save(self.q_table_file, self.q_table)  # Save Q-table to file

    def reset_q_table(self):
        self.q_table = np.zeros((self.grid_size, self.grid_size, 2))  # Reset Q-table
