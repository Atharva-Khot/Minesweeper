from random import randint
from tile import Tile

class Grid:
    def __init__(self, size, bombs_num):
        self.size = size
        self.grid = [[Tile() for _ in range(size)] for _ in range(size)]
        self.place_bombs(bombs_num)
        self.calculate_adjacent_bombs()

    def place_bombs(self, bombs_num):
        for _ in range(bombs_num):
            while True:
                x = randint(0, self.size - 1)
                y = randint(0, self.size - 1)
                if not self.grid[x][y].bomb:
                    self.grid[x][y].bomb = True
                    break

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