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
