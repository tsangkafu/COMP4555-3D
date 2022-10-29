import pygame
from player import Player
from background import Background
import psutil
from levels import LEVELS
import enemy
import random
import globals

class Level():
    def __init__(self, screen, level):
        self.screen = screen
        self.level = level
        # the player sprite store all the component of the player including the base and the weapon
        self.player_sprites = pygame.sprite.Group()
        self.player = Player(self.player_sprites)

        self.enemy_sprites = pygame.sprite.Group()

        self.background = Background()

        self.populate_enemies()
    
    # all the level behaviors here
    def run(self):
            self.screen.blit(self.background.image, (0, 0))
            self.player_sprites.draw(self.screen)
            self.enemy_sprites.draw(self.screen)

            # this will call the update() in all player sprites
            self.player_sprites.update()
            self.enemy_sprites.update()

    def populate_enemies(self):
        for i, row in enumerate(LEVELS[int(self.level)]):
            for j, col in enumerate(row):
                x = j * globals.TILE
                y = i * globals.TILE
                if col != " ":
                    color = random.choice(enemy.Enemy.ENEMIES[int(col)])
                    enemy.Enemy(self.enemy_sprites, int(col), color, (x, y))