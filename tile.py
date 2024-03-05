class Tile:
    def __init__(self):
        self.bomb = False
        self.revealed = False
        self.flagged = False
        self.adjacent_bombs = 0
