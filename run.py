import pygame
import globals
import sys
from level import Level
from sprites import Sprites

#################################################################

class Game():                             
    def __init__(self):
        # pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((globals.DISPLAY_WIDTH, globals.DISPLAY_HEIGHT)) 
        pygame.display.set_caption("Space Invaders")
        self.level = 1

    def run(self):
        self.level = Level(self.screen, self.level)
        music_playing = True

        while (1):
            self.level.run()
            
            # sprites.animate()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_m:
                            if music_playing:
                                pygame.mixer.music.pause()
                                music_playing = False
                            else:
                                pygame.mixer.music.unpause()
                                music_playing = True


            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()