import pygame
import globals
import enemy

class Bullet():

    ######################################################################
    # CONSTRUCTOR
    
    # x and y should be the coordinates of the ship (at least in the base game)
    def __init__(self, spritesDict, x, y):
        self.spritesDict = spritesDict
        
        self.image = pygame.image.load("./media/images/bullet.png")
        
        self.x = x
        self.y = y

        self.curSpeedX = 0
        self.curSpeedY = -10

        self.shouldDelete = False


    ######################################################################
    # GETTERS

    def get_width(self):
        return self.image.get_width()

    def get_height(self):
        return self.image.get_height()

    ######################################################################
    # OTIONAL

    def update_location(self):
        oldX = self.x
        oldY = self.y

        self.x += self.curSpeedX
        self.y += self.curSpeedY


        wallsHitArr = globals.collision(self, self.spritesDict["walls"])
        if wallsHitArr:
            self.x = oldX
            self.y = oldY
            for wallSprite in wallsHitArr:
                if wallSprite.description == "horizontal top":
                    self.shouldDelete = True

        # bullet collides with enemy
        enemySpritesHitArr = globals.collision(self, self.spritesDict["enemies"])
        if enemySpritesHitArr:
            # mark the bullet itself for deletion
            self.shouldDelete = True

            # mark the hit enemies for deletion
            for enemySprite in enemySpritesHitArr:
                enemySprite.shouldDelete = True
            
            # create new enemies
            for i in range(len(enemySpritesHitArr)):
                self.spritesDict["enemies"].append(enemy.Enemy(self.spritesDict))