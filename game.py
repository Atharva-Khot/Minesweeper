from random import randint

import pygame
from grid import Grid


class Game:
    def __init__(self, size, bombs_num):
        self.grid = Grid(size, bombs_num)
        self.breadth = 50
        self.tiles_to_reveal = size * size - bombs_num

    def draw(self, screen):
        y = 0
        for row in self.grid.grid:
            x = 0
            for tile in row:
                if tile.flagged:
                    pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(x, y, self.breadth, self.breadth))
                elif tile.revealed:
                    if tile.bomb:
                        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(x, y, self.breadth, self.breadth))
                    else:
                        pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(x, y, self.breadth, self.breadth))
                    if not tile.bomb and tile.adjacent_bombs > 0:
                        font = pygame.font.Font(None, 36)
                        text = font.render(str(tile.adjacent_bombs), True, (0, 0, 0))
                        text_rect = text.get_rect(center=(x + self.breadth // 2, y + self.breadth // 2))
                        screen.blit(text, text_rect)
                else:
                    pygame.draw.rect(screen, (150, 150, 150), pygame.Rect(x, y, self.breadth, self.breadth))
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x, y, self.breadth, self.breadth), 1)
                x += self.breadth
            y += self.breadth
        for i in range(self.grid.size + 1):
            pygame.draw.line(screen, (0, 0, 0), (0, i * self.breadth), (self.breadth * self.grid.size, i * self.breadth), 1)
            pygame.draw.line(screen, (0, 0, 0), (i * self.breadth, 0), (i * self.breadth, self.breadth * self.grid.size), 1)

    def reveal_neighbors(self, row, col):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                x = row + dx
                y = col + dy
                if self.grid.isTileInGrid(x, y):
                    if not self.grid.isRevealed(x, y) and not self.grid.grid[x][y].bomb:
                        self.grid.setRevealed(x, y, True)
                        self.tiles_to_reveal -= 1
                        if self.grid.isSafeTile(x, y):
                            self.reveal_neighbors(x, y)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked_col = event.pos[0] // self.breadth
            clicked_row = event.pos[1] // self.breadth

            if event.button == 1: #leftclick
                if not self.grid.isRevealed(clicked_row, clicked_col) and not self.grid.isFlagged(clicked_row, clicked_col):
                    self.grid.setRevealed(clicked_row, clicked_col, True)
                    if self.grid.grid[clicked_row][clicked_col].bomb:
                        print("Game Over!")
                        return False
                    
                    self.tiles_to_reveal -= 1
                    if self.grid.isSafeTile(clicked_row, clicked_col):
                        self.reveal_neighbors(clicked_row, clicked_col)
                    if self.tiles_to_reveal == 0:
                        print("You won!")
                        return False
                    
            elif event.button == 3: #rightclick
                if self.grid.isRevealed(clicked_row, clicked_col):
                    return True
                elif self.grid.isFlagged(clicked_row, clicked_col):
                    self.grid.setFlagged(clicked_row, clicked_col ,False)
                else:
                    self.grid.setFlagged(clicked_row, clicked_col ,True)
            
        return True
    def agent_play(self, delay_ms=500):
        if self.tiles_to_reveal == 0:
            print("Agent won!")
            return False

        unrevealed_tiles = [(i, j) for i in range(self.grid.size) for j in range(self.grid.size)
                            if not self.grid.isRevealed(i, j)]

        if unrevealed_tiles:
            
            random_tile = unrevealed_tiles[randint(0, len(unrevealed_tiles) - 1)]
            row, col = random_tile

            if not self.grid.isFlagged(row, col):
                self.grid.setRevealed(row, col, True)
                if self.grid.grid[row][col].bomb:
                    print("Game Over!")
                    return False

                self.tiles_to_reveal -= 1
                if self.grid.isSafeTile(row, col):
                    self.reveal_neighbors(row, col)

                pygame.time.delay(delay_ms+200)

        return True
