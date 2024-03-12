from random import randint

import pygame
from game import Game
import time

def main():

    SIZE = 10
    BOMBS = 5
    BREADTH = 50

    pygame.init()
    screen = pygame.display.set_mode((SIZE*BREADTH, SIZE*BREADTH))
    clock = pygame.time.Clock()

    game = Game(SIZE, BOMBS, BREADTH)

    maxGames = 10
    gamesPlayed = 0
    running = True
    while gamesPlayed < maxGames:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            running = game.handle_event(event)
        #running = game.agent_play()
        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)
        
        if not running:
            pygame.init()
            game.resetGame()
            gamesPlayed += 1
            time.sleep(2)

    pygame.quit()

if __name__ == "__main__":
    main()
