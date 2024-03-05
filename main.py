from random import randint

import pygame
from game import Game


def main():
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()

    game = Game(10, 8)

    running = True
    while running:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            running = game.handle_event(event)

        running = game.agent_play()

        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
