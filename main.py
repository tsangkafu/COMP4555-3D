from pickle import GLOBAL
import pygame
from pygame.locals import *
from pygame import mixer

import random
from powerup import *
from level import Level
from settings import *
import sys



class Game():
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.level = Level(self.screen)
        pygame.display.set_caption("Pong")

    def run(self):
        start_time = pygame.time.get_ticks()
        mixer.music.load('media//music.ogg')
        mixer.music.play(loops=-1)
        mixer.music.set_volume(0.3)
        music_playing = True

        while True:
            # event detection
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
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
