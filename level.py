import pygame
from player import Player
from background import Background
import psutil
from levels import LEVELS
import enemy
import random
import globals
from exposion import Exposion
from hit import Hit
from powerup import Powerup

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
        self.hit_sprites = pygame.sprite.Group()

        self.powerup_sprites = pygame.sprite.Group()
  
        self.powerup_start = 0
        self.powerup_timer = pygame.time.get_ticks()

        # Score Board
        self.score_value = 0
        self.font = pygame.font.Font("./media/fonts/Retro Gaming.ttf", 24)
    
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
            
            for enemy in self.enemy_sprites:
                enemy.bullet_sprites.draw(self.screen)
                enemy.bullet_sprites.update()

            self.detect_collision()

            self.exposion_sprites.draw(self.screen)
            self.exposion_sprites.update()

            self.hit_sprites.draw(self.screen)
            self.hit_sprites.update()

            self.powerup_sprites.draw(self.screen)
            self.powerup_sprites.update()

            self.powerup_timer = pygame.time.get_ticks()
            if self.powerup_timer - self.powerup_start > 10000:
                self.player.weapon.switch_weapon("normal")
                self.player.bullet = 3
                self.powerup_start = pygame.time.get_ticks()

            score = self.font.render("SCORE: "+str(self.score_value), True, (0, 255, 150))
            self.screen.blit(score, (10, 10))

    def populate_enemies(self):
        for i, row in enumerate(LEVELS[int(self.level)]):
            for j, col in enumerate(row):
                x = j * globals.TILE
                y = i * globals.TILE
                if col != " ":
                    color = random.choice(enemy.Enemy.ENEMIES_CONFIG[int(col)]["color"])
                    enemy.Enemy(self.enemy_sprites, int(col), color, (x, y))

    def detect_collision(self):
        # groupcollide will return a dict of which the enemy collided is the key
        enemy_collided = pygame.sprite.groupcollide(self.enemy_sprites, self.player.bullet_sprites, False, True)
        # loop through the dict
        for enemy in enemy_collided:
            Hit(self.hit_sprites, enemy.rect.center)
            pygame.mixer.Sound.play(globals.ENEMY_HIT_SOUND) 
            enemy.hp -= 1
            if enemy.hp <= 0:
                enemy.kill()
                pygame.mixer.Sound.play(globals.EXPLOSION_SOUND) 
                Exposion(self.exposion_sprites, enemy.level, enemy.rect.center)
                self.score_value += enemy.score_value
                # drop rate is inverse of decimal, so 25% 
                if random.random() > 0.80:
                    powerup = Powerup(self.powerup_sprites, enemy.rect.center)
                    self.powerup_sprites.add(powerup)
                del enemy

        for enemy in self.enemy_sprites:
            for bullet in enemy.bullet_sprites:
                if bullet.rect.colliderect(self.player.weapon.rect):
                    Hit(self.hit_sprites, self.player.rect.center)
                    bullet.kill()
                    if self.player.shield == 0:
                        pygame.mixer.Sound.play(globals.PLAYER_HIT_SOUND)  
                        self.player.hp -= 1
                    else:
                        pygame.mixer.Sound.play(globals.PLAYER_HIT_SOUND) 
                        self.player.shield -= 1
                    # if self.player.hp > 0:
                    #     Exposion(self.exposion_sprites, 1, self.player.rect.center)
                    if self.player.hp == 0:
                        pygame.mixer.Sound.play(globals.PLAYER_EXPLOSION_SOUND) 
                        Exposion(self.exposion_sprites, 2, self.player.rect.center)
                        self.player_sprites.empty()
        
        #powerup collision, activate different effects depending on powerup.type
        powerups_collided = pygame.sprite.groupcollide(self.powerup_sprites, self.player_sprites, True, False)
        for powerup in powerups_collided:
            pygame.mixer.Sound.play(globals.POWERUP_SOUND) 
            # max hp = 3
            if powerup.type == 'heal':
                if self.player.hp < 3: 
                    self.player.hp += 1
            if powerup.type == 'shield':
                if self.player.shield < 1:
                    self.player.shield += 1
            if powerup.type == 'twin':
                self.player.weapon.switch_weapon("twin")
                self.player.bullet = 9
                self.powerup_start = pygame.time.get_ticks()
            del powerup