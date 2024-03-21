from random import randint

import pygame

from grid import Grid


class Game:

    COLOR_UNREVEALED = (150, 150, 150)
    COLOR_REVEALED = (200, 200, 200)
    COLOR_GRID_LINES = (100, 100, 100)
    COLOR_FLAGGED = (0, 0, 255)
    COLOR_BOMB = (255, 0, 0)
    # Define colors for numbers
    COLOR_FONTS = {
        1: (0, 0, 150),    # Dark blue for number 1
        2: (0, 100, 0),    # Dark green for number 2
        3: (200, 0, 0),    # Dark red for number 3
        4: (0, 0, 100),    # Dark blue for number 4
        5: (120, 60, 0),   # Dark brown for number 5
        6: (0, 120, 120),  # Dark cyan for number 6
        7: (0, 0, 0),      # Black for number 7
        8: (100, 100, 100) # Dark grey for number 8
    }

    def __init__(self, size, bombs_num, breadth=50):
        self.size = size
        self.bombs_num = bombs_num
        self.grid = Grid(size, bombs_num)
        self.breadth = breadth
        self.tiles_to_reveal = size * size - bombs_num
        self.fontSize = int(self.breadth)
        self.agent = QLearningAgent(size)
        self.unrevealed_tiles = [(i, j) for i in range(size) for j in range(size)]
    def reset_game(self):
        # Reset other game attributes
        self.agent.reset_q_table()
    def resetGame(self):
        self.tiles_to_reveal = self.size * self.size - self.bombs_num
        self.unrevealed_tiles = [(i, j) for i in range(self.size) for j in range(self.size)]
        self.grid = Grid(self.size, self.bombs_num)


    def draw(self, screen):
        y = 0

        for row in self.grid.grid:
            x = 0
            for tile in row:
                if tile.flagged:
                    pygame.draw.rect(screen, self.COLOR_FLAGGED, pygame.Rect(x, y, self.breadth, self.breadth))
                elif tile.revealed:
                    if tile.bomb:
                        pygame.draw.rect(screen, self.COLOR_BOMB, pygame.Rect(x, y, self.breadth, self.breadth))
                    else:
                        pygame.draw.rect(screen, self.COLOR_REVEALED, pygame.Rect(x, y, self.breadth, self.breadth))
                    if not tile.bomb and tile.adjacent_bombs > 0:
                        font = pygame.font.Font(None, self.fontSize)
                        text = font.render(str(tile.adjacent_bombs), True, self.COLOR_FONTS[tile.adjacent_bombs])
                        text_rect = text.get_rect(center=(x + self.breadth // 2, y + self.breadth // 2))
                        screen.blit(text, text_rect)
                else:
                    pygame.draw.rect(screen, self.COLOR_UNREVEALED, pygame.Rect(x, y, self.breadth, self.breadth))
                pygame.draw.rect(screen, self.COLOR_GRID_LINES, pygame.Rect(x, y, self.breadth, self.breadth), 1)
                x += self.breadth
            y += self.breadth

            for i in range(self.grid.size + 1):
                pygame.draw.line(screen, self.COLOR_GRID_LINES, (0, i * self.breadth), (self.breadth * self.grid.size, i * self.breadth), 1)
                pygame.draw.line(screen, self.COLOR_GRID_LINES, (i * self.breadth, 0), (i * self.breadth, self.breadth * self.grid.size), 1)

    def reveal_neighbors(self, row, col):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                x = row + dx
                y = col + dy
                if self.grid.isTileInGrid(x, y):
                    if not self.grid.isRevealed(x, y) and not self.grid.grid[x][y].bomb:
                        self.grid.setRevealed(x, y, True)
                        if (x, y) in self.unrevealed_tiles:  # Check if the tile is in the list
                            self.unrevealed_tiles.remove((x, y))  # Remove the tile if it exists in the list

                        self.tiles_to_reveal -= 1
                        if self.grid.isSafeTile(x, y):
                            self.reveal_neighbors(x, y)

    def revealTile(self, row, col):
        if self.grid.isRevealed(row, col):
            return True
        if self.grid.isFlagged(row, col):
            return True
        
        self.grid.setRevealed(row, col, True)
        self.unrevealed_tiles.remove( (row, col) )
        if self.grid.grid[row][col].bomb:
            print("Game Over!")
            return False
        
        self.tiles_to_reveal -= 1
        if self.grid.isSafeTile(row, col):
            self.reveal_neighbors(row, col)
        if self.tiles_to_reveal == 0:
            print("You won!")
            return False
        return True
        
    def flagTile(self, row, col):
        if self.grid.isRevealed(row,col):
            return True
        elif self.grid.isFlagged(row, col):
            self.grid.setFlagged(row, col ,False)
            self.unrevealed_tiles.append((row, col))
        else:
            self.grid.setFlagged(row, col ,True)
            self.unrevealed_tiles.remove((row, col))
        return True
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked_col = event.pos[0] // self.breadth
            clicked_row = event.pos[1] // self.breadth

            if event.button == 1: #leftclick
                return self.revealTile(clicked_row, clicked_col)
            
            elif event.button == 3: #rightclick
                return self.flagTile(clicked_row, clicked_col)
        return True
    
    def agent_play(self, delay_ms=100):
        if self.tiles_to_reveal == 0:
            print("Agent won!")
            return False
        if self.tiles_to_reveal == self.size*self.size-self.bombs_num:
            row, col = randint(0, self.size-1), randint(0, self.size-1)
            return self.revealTile(row, col)

        runGame = True

        if self.unrevealed_tiles:
            state = (self.unrevealed_tiles[0][0], self.unrevealed_tiles[0][1])
            action = self.agent.choose_action(state)

            reward = 0
            if action == 0:  # Reveal
                row, col = state
                runGame = self.revealTile(row, col)
                if runGame:
                    reward = 1 if self.tiles_to_reveal > 0 else 10  # Reward for successful reveal
                else:
                    reward = -10  # Penalty for revealing a bomb

            elif action == 1:  # Flag
                row, col = state
                runGame = self.flagTile(row, col)
                if runGame:
                    reward = 1  # Reward for successful flagging
                else:
                    reward = -1  # Penalty for flagging a revealed tile

            next_state = (row, col)
            self.agent.update_q_table(state, action, reward, next_state)

            pygame.time.delay(delay_ms)

        return runGame
    
import numpy as np


class QLearningAgent:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        # Modify Q-table shape to match the grid
        self.q_table = np.zeros((grid_size, grid_size, 3, 2))  # 3 possible states: unrevealed, revealed, flagged
        self.alpha = 0.1  # learning rate
        self.gamma = 0.9  # discount factor
        self.epsilon = 0.1  # exploration-exploitation trade-off

    def choose_action(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.choice([0, 1])  # explore
        else:
            return np.argmax(self.q_table[state[0], state[1], :, :])

    def update_q_table(self, state, action, reward, next_state):
        predict = self.q_table[state[0], state[1], :, action]
        target = reward + self.gamma * np.max(self.q_table[next_state[0], next_state[1], :, :])
        self.q_table[state[0], state[1], :, action] += self.alpha * (target - predict)
