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
        self.speed = BALL_SPEED_NORMAL
        self.crit_speed = 0
        self.velocity = pygame.Vector2((self.speed, self.speed))
        # pygame.SRCALPHA to make the surface transparent
        self.image = pygame.Surface(
            (self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color,
                           (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=pos)

    def update(self, color):

        # reverse y when the ball reaches top or bottom
        if self.rect.top <= 0:
            if self.velocity[1] < 0:
                # pygame.mixer.Sound.play(PONG_SOUND)
                self.bounce("y")

        if self.rect.bottom >= HEIGHT:
            if self.velocity[1] > 0:
                # pygame.mixer.Sound.play(PONG_SOUND)
                self.bounce("y")

        # reverse x when the ball collides the board
        if self.rect.colliderect(self.player.rect):
            # fixing ball getting stuck issue
            # if the speed x of the ball is a positive number
            # meaning it is going to the right
            # if it has bounced off already (x < 0)
            # then don't change its direction
            if self.velocity[0] > 0:
                # pygame.mixer.Sound.play(PONG_SOUND)
                self.bounce("x")

        if self.rect.colliderect(self.opponent.rect):
            if self.velocity[0] < 0:
                # pygame.mixer.Sound.play(PONG_SOUND)
                self.bounce("x")

        # when the ball reaches left or right, scores
        if self.rect.left <= 0 - 100:
            self.player.score += 1
            self.crit_speed = 0
            self.restart()
        elif self.rect.right >= WIDTH + 100:
            self.opponent.score += 1
            self.crit_speed = 0
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

        # theme color change
        pygame.draw.circle(self.image, color,
                           (self.radius, self.radius), self.radius)

    def bounce(self, coord, bungieSpeed="off", criticalspeed="off"):
        if coord == "x":
            self.velocity[0] *= -1
            # if the ball is hitting the player's paddle
            if self.rect.colliderect(self.player.rect):
                # if the center of the ball is outside of the board
                # meaning it's hitting the paddle on the upper edge
                if self.rect.center[1] < self.player.rect.topleft[1]:
                    # if the ball is coming from top to bottom, change the direction
                    if self.velocity[1] > 0:
                        self.velocity[1] *= -1
                # when the ball hitting the lower edge of the paddle
                if self.rect.center[1] > self.player.rect.bottomleft[1]:
                    # if the ball is coming from bottom to top, change the direction
                    if self.velocity[1] < 0:
                        self.velocity[1] *= -1

            elif self.rect.colliderect(self.opponent.rect):
                self.crit_speed = 0
                # if the center of the ball is outside of the board
                # meaning it's hitting the paddle on the upper edge
                if self.rect.center[1] < self.opponent.rect.topright[1]:
                    # if the ball is coming from top to bottom, change the direction
                    if self.velocity[1] > 0:
                        self.velocity[1] *= -1
                # when the ball hitting the lower edge of the paddle
                if self.rect.center[1] > self.opponent.rect.bottomright[1]:
                    # if the ball is coming from bottom to top, change the direction
                    if self.velocity[0] < 0:
                        self.velocity[1] *= -1

        elif coord == "y":
            self.velocity[1] *= -1
        self.toggle_bungie_speed(bungieSpeed)

        if (self.rect.right <= WIDTH - 20 and self.rect.colliderect(self.player.rect)):
            print('activate')
            self.velocity[1] *= -1
            self.toggle_critical_speed(criticalspeed)

    def restart(self):
        # pygame.mixer.Sound.play(SCORE_SOUND)
        self.speed = BALL_SPEED_NORMAL
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.velocity[0] *= random.choice((1, -1))
        self.velocity[1] *= random.choice((1, -1))

    def toggle_critical_speed(self, onOff):
        for i, coordSpeed in enumerate(self.velocity):
            # need to preserve the sign, aka the direction the ball is going in
            isNegative = True if coordSpeed < 0 else False
            absoluteValue = abs(coordSpeed)
            newSpeedx = 0
            newSpeedy = 0
            if self.rect.center[1] < self.player.rect.topleft[1] or self.rect.center[1] > self.player.rect.bottomleft[1]:
                newSpeedx = BALL_SPEED_NORMAL / 2
                newSpeedy = BALL_SPEED_NORMAL * 2
                if self.rect.center[1] < self.player.rect.topleft[1]:
                    if self.velocity[1] > 0:
                        self.velocity[1] *= -1
                elif self.rect.center[1] > self.player.rect.bottomleft[1]:
                    if self.velocity[1] < 0:
                        self.velocity[1] *= -1
            else:
                newSpeedx = BALL_SPEED_NORMAL * 2
                newSpeedy = BALL_SPEED_NORMAL * 2

            if isNegative:
                newSpeedx *= -1
                newSpeedy *= -1

            self.velocity[0] = newSpeedx
            self.velocity[1] = newSpeedy

    # def const_crit_speed(self, coordx, coordy):
        # if coordx > BALL_SPEED_NORMAL or coordy > BALL_SPEED_NORMAL

    def toggle_bungie_speed(self, onOff):
        for i, coordSpeed in enumerate(self.velocity):
            # need to preserve the sign, aka the direction the ball is going in
            isNegative = True if coordSpeed < 0 else False
            absoluteValue = abs(coordSpeed)
            newSpeed = BALL_SPEED_NORMAL + \
                random.randint(-2, 2) if onOff == "off" else BALL_SPEED_BUNGIE
            if isNegative:
                newSpeed *= -1
            self.velocity[i] = newSpeed
