import pygame
from pygame.locals import *
from pygame import mixer

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.music.load('lecture_code/media/music.ogg')
mixer.music.play(loops = -1)

import sys
from settings import *
from level import Level
import random
# import powerup
from powerup import *

class Game():
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.level = Level(self.screen)
        pygame.display.set_caption("Pong")


    def run(self):
        start_time = pygame.time.get_ticks()

        while True:
            # event detection
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
                if self.level.end_game:
                    if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                        self.level = Level(self.screen)
                        break
            
            self.level.run()
           
            if not self.level.end_game:
                # ~~~~ powerup position randomize block ~~~~~
                time_elapsed = pygame.time.get_ticks()
                changeHeight = False

                if (time_elapsed - start_time) > 3000:
                    changeHeight = True

                if changeHeight:
                    start_time = pygame.time.get_ticks()
                    Powerup.changeHeight(self.level.powerup)
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()