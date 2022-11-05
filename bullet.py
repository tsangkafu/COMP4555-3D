import pygame
import globals
import os

# key being the level of the enemy
# value being the bullet it uses
ENEMY_BULLET = {

}

class Bullet(pygame.sprite.Sprite):

    ######################################################################
    # CONSTRUCTOR
    
    # x and y should be the coordinates of the ship (at least in the base game)

    # pass in the rect where the bullet should be shot from
    # ship can be enemy or player, bullet will adjust its action
    def __init__(self, groups, ship, x_speed): #spritesDict, x, y):
        super().__init__(groups)
        # self.spritesDict = spritesDict
        self.ship = ship
        if self.ship.name == "player":
            self.pos = (ship.rect.midtop[0], ship.rect.midtop[1])
            path = ".//media//image//bullet + fx + powerup + coin//shot//normalshot"
            self.image = globals.scale_image(pygame.image.load(os.path.join(path, "shot_0.png")).convert_alpha())
            self.rect = self.image.get_rect(center = self.pos)
        # enemy bullet start pos
        else:
            self.pos = (ship.rect.midbottom[0], ship.rect.midbottom[1])
            path = ".//media//image//bullet + fx + powerup + coin//bullet_" + str(ship.bullet)
            self.image = globals.scale_image(pygame.image.load(os.path.join(path, "0.png")).convert_alpha())
            self.rect = self.image.get_rect(center = self.pos)

        self.speed = 10
        self.x_speed = x_speed

        # velocity[0] = speed X
        # velocity[1] = speed Y
        self.velocity = [self.speed, self.speed]
        self.bullet_size = 0

        # used as a point of reference to stop the bullet from getting too big
        self.original_size = self.image.get_size()
        # a copy of the original image, used to prevent the image getting pixelized when transform from small to big
        self.og_image = self.image.copy()
        # the bullet should be invisible at the beginning
        self.image = pygame.transform.scale(self.image, (0, 0))
        

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
        # animate the bullet - when it first shoots it will be smaller and later turns to original size
        def bullet_animation():
            if self.bullet_size < 1:
                self.bullet_size += 0.1
                self.image = pygame.transform.scale(self.og_image,
                    (self.original_size[0] * self.bullet_size,
                    self.original_size[1] * self.bullet_size))

                # update the rect accordingly
                self.rect = self.image.get_rect(center = self.rect.center)


        if self.ship.name == "player":
            bullet_animation()

            self.rect.y -= self.speed
            self.rect.x += self.x_speed

            # "kill" the bullet when its out of screen
            if self.rect.y <= 0 - self.get_height():
                self.kill()
        # enemy's bullet
        else:
            bullet_animation()
            self.rect.y += self.speed


            if self.rect.y >= globals.DISPLAY_HEIGHT + self.get_height():
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