import pygame
import sys

from settings import *
from level import Level

class Game():
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.level = Level()
        pygame.display.set_caption("Pong")


    def run(self):
        while True:
            # event detection
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.level.run()

            pygame.display.flip()

            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()