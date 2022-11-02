import pygame
import globals
import sys
from level import Level
from sprites import Sprites

#################################################################

class Game():                             
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((globals.DISPLAY_WIDTH, globals.DISPLAY_HEIGHT)) 
        pygame.display.set_caption("Space Invaders")
        self.level = 1

    def run(self):
        self.level = Level(self.screen, self.level)

        while (1):
            self.level.run()
            
            # sprites.animate()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()