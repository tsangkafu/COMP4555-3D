import pygame
import random
from settings import *

class Ball(pygame.sprite.Sprite):
    # pos = position
    # group = sprite group
    def __init__(self, radius, pos, color, group, player, opponent, powerup):
        super().__init__(group)
        self.player = player
        self.opponent = opponent
        self.powerup = powerup
        self.radius = radius
        self.speed = 7
        self.velocity = [self.speed, self.speed]
        # pygame.SRCALPHA to make the surface transparent
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center = pos)

    def update(self, color):
        # reverse y when the ball reaches top or bottom
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            pygame.mixer.Sound.play(PONG_SOUND)
            self.velocity[1] *= -1
        # reverse x when the ball collides the board
        if self.rect.colliderect(self.player.rect) or self.rect.colliderect(self.opponent.rect):
            pygame.mixer.Sound.play(PONG_SOUND)
            self.velocity[0] *= -1
        
        # when the ball reaches left or right, scores
        if self.rect.left <= 0:
            self.player.score += 1
            self.restart()
        elif self.rect.right >= WIDTH:
            self.opponent.score += 1
            self.restart()

        # powerup collision 
        # todo: remove powerup on collision + implement powerup timers
        # if self.rect.colliderect(self.powerup.rect):
        #     pygame.mixer.Sound.play(PONG_SOUND)
        #     self.player.change_size(240)
        #     self.powerup.moveOffscreen()

        # move ball after velocity is set
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        #theme color change
        pygame.draw.circle(self.image, color, (self.radius, self.radius), self.radius)

    def restart(self):
        pygame.mixer.Sound.play(SCORE_SOUND)
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.velocity[0] *= random.choice((1, -1))
        self.velocity[1] *= random.choice((1, -1))

    def change_speed(self):
        pass