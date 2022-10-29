import pygame
from player import Player
from background import Background
import psutil
from levels import LEVELS
import enemy
import random
import globals
from exposion import Exposion

class Level():
    def __init__(self, screen, level):
        self.screen = screen
        self.level = level

        self.enemy_sprites = pygame.sprite.Group()

        self.background = Background()

        self.populate_enemies()
        
        # the player sprite store all the component of the player including the base and the weapon
        self.player_sprites = pygame.sprite.Group()
        self.player = Player(self.player_sprites)

        self.exposion_sprites = pygame.sprite.Group()
    
    # all the level behaviors here
    def run(self):
            self.screen.blit(self.background.image, (0, 0))
            self.player_sprites.draw(self.screen)
            self.enemy_sprites.draw(self.screen)

            # this will call the update() in all sprites
            self.player_sprites.update()
            self.enemy_sprites.update()

            self.player.bullet_sprites.draw(self.screen)
            self.player.bullet_sprites.update()

            self.detect_collision()

            self.exposion_sprites.draw(self.screen)
            self.exposion_sprites.update()


    def populate_enemies(self):
        for i, row in enumerate(LEVELS[int(self.level)]):
            for j, col in enumerate(row):
                x = j * globals.TILE
                y = i * globals.TILE
                if col != " ":
                    color = random.choice(enemy.Enemy.ENEMIES[int(col)])
                    enemy.Enemy(self.enemy_sprites, int(col), color, (x, y))

    def detect_collision(self):
        # groupcollide will return a dict of which the enemy collided is the key
        enemy_collided = pygame.sprite.groupcollide(self.enemy_sprites, self.player.bullet_sprites, False, True)
        # loop through the dict
        for enemy in enemy_collided:
            enemy.hp -= 1
            if enemy.hp <= 0:
                enemy.kill()
                Exposion(self.exposion_sprites, enemy.level, enemy.rect.center)