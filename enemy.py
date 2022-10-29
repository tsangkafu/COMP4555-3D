import pygame
import globals
import random

class Enemy():

    ######################################################################
    # CONSTRUCTOR

    def __init__(self, spritesDict):
        self.spritesDict = spritesDict
        
        self.image = pygame.image.load("./media/images/ufo.png")
        
        self.x = random.randint(0, globals.DISPLAY_WIDTH - self.get_width())
        self.y = random.randint(0, globals.DISPLAY_HEIGHT - 300) # 300 being the distance from the bottom

        self.curSpeedX = 2
        self.curSpeedY = 0

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
                if wallSprite.description.startswith("vertical"):
                    self.curSpeedX *= -1
                    self.y += 40
                elif wallSprite.description == "horizontal bottom":
                    self.shouldDelete = True
            
        
