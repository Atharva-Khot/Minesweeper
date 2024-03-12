from random import shuffle
from tile import Tile

class Grid:
    def __init__(self, size, bombs_num):
        self.size = size
        self.grid = [[Tile() for _ in range(size)] for _ in range(size)]
        self.place_bombs(bombs_num)
        self.calculate_adjacent_bombs()

    def place_bombs(self, bombs_num):
        all_positions = [(x, y) for x in range(self.size) for y in range(self.size)]
        shuffle(all_positions)
    
        bomb_positions = all_positions[:bombs_num]

        for x, y in bomb_positions:
            self.grid[x][y].bomb = True

    def calculate_adjacent_bombs(self):
        for i in range(self.size):
            for j in range(self.size):
                count = 0
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if self.isTileInGrid(i+dx, j+dy):
                            count += self.grid[i + dx][j + dy].bomb
                self.grid[i][j].adjacent_bombs = count
    
    def isRevealed(self, row, col):
        return self.grid[row][col].revealed

    def setRevealed(self, row, col, value):
        self.grid[row][col].revealed = value
    
    def isFlagged(self, row, col):
        return self.grid[row][col].flagged

    def setFlagged(self, row, col, value):
        self.grid[row][col].flagged = value

    def isTileInGrid(self, row, col):
        return (0 <= row < self.size) and (0 <= col < self.size)

    def isSafeTile(self, row, col):
        return self.grid[row][col].adjacent_bombs == 0
    
    def isFullMarked(self, row, col):
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if self.isTileInGrid(row+dx, col+dy):
                    count += self.grid[row + dx][col + dy].bomb
        return self.grid[row][col].adjacent_bombs == count
    
    def isGameOver(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j].revealed == self.grid[i][j].bomb:
                    return False
        return True