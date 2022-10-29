import pygame
import globals
import enemy
import os

class Bullet(pygame.sprite.Sprite):

    ######################################################################
    # CONSTRUCTOR
    
    # x and y should be the coordinates of the ship (at least in the base game)

    # pass in the rect where the bullet should be shot from
    def __init__(self, groups, rect): #spritesDict, x, y):
        super().__init__(groups)
        # self.spritesDict = spritesDict
        self.pos = rect.midtop
        path = ".//media//image//bullet + fx + powerup + coin//shot//normalshot"
        self.image = pygame.image.load(os.path.join(path, "shot_0.png")).convert_alpha()
        self.rect = self.image.get_rect(center = self.pos)

        self.speed = 10
        # velocity[0] = speed X
        # velocity[1] = speed Y
        self.velocity = [self.speed, self.speed]

        self.cd = 5000
        
        # self.x = x
        # self.y = y

        # self.curSpeedX = 0
        # self.curSpeedY = -10

        # self.shouldDelete = False


    ######################################################################
    # GETTERS

    def get_width(self):
        return self.image.get_width()

    def get_height(self):
        return self.image.get_height()

    ######################################################################
    # OTIONAL

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0 - self.get_height():
            self.kill()


    # def update_location(self):
    #     oldX = self.x
    #     oldY = self.y

    #     self.x += self.curSpeedX
    #     self.y += self.curSpeedY


    #     wallsHitArr = globals.collision(self, self.spritesDict["walls"])
    #     if wallsHitArr:
    #         self.x = oldX
    #         self.y = oldY
    #         for wallSprite in wallsHitArr:
    #             if wallSprite.description == "horizontal top":
    #                 self.shouldDelete = True

    #     # bullet collides with enemy
    #     enemySpritesHitArr = globals.collision(self, self.spritesDict["enemies"])
    #     if enemySpritesHitArr:
    #         # mark the bullet itself for deletion
    #         self.shouldDelete = True

    #         # mark the hit enemies for deletion
    #         for enemySprite in enemySpritesHitArr:
    #             enemySprite.shouldDelete = True
            
    #         # create new enemies
    #         for i in range(len(enemySpritesHitArr)):
    #             self.spritesDict["enemies"].append(enemy.Enemy(self.spritesDict))