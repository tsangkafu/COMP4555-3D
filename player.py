import pygame
import globals
import bullet
import os

class Player(pygame.sprite.Sprite):

    ######################################################################
    # CONSTRUCTOR
    
    def __init__(self, groups):#, spritesDict):
        super().__init__(groups)
        # self.spritesDict = spritesDict

        # you can change to tank_blue/tank_pink
        self.color = "green"

        # count the number of image in one file, this will change because different sprite has different files
        path = ".//media//image//tank+weapon//tank_"  + self.color
        num_of_img = globals.count_image(path)
        
        # a list that store all the image of a sprite
        self.animation = []
        # loop through each image and append it to the animation list
        for i in range(num_of_img):
            # scale the image
            image = globals.scale_image(pygame.image.load(os.path.join(path, str(i) + ".png")).convert_alpha())
            self.animation.append(image)
            
        self.current_frame = 0
        self.image = self.animation[self.current_frame]
        # 10 being the offset from the bottom
        self.rect = self.image.get_rect(center = (globals.DISPLAY_WIDTH / 2, globals.DISPLAY_HEIGHT - self.get_height() + 10))
        

        # pass in the rect (position) of the base (things that look like balls) so that the weapon can follow
        self.weapon = Weapon(groups, self.rect)
        
        self.speed = 7

        # self.curSpeedX = 0
        # self.curSpeedY = 0


    ######################################################################
    # GETTERS

    def get_width(self):
        return self.image.get_width()

    def get_height(self):
        return self.image.get_height()


    ######################################################################
    # OTIONAL
        
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left >= 0:
            self.rect.x -= self.speed
        elif keys[pygame.K_RIGHT] and self.rect.right <= globals.DISPLAY_WIDTH:
            self.rect.x += self.speed

        # animate the player
        # current frame increment being the speed of how fast the animation is
        self.current_frame += 0.2

        # reset the frame when the current frame exceed the number of available image
        if self.current_frame >= len(self.animation):
            self.current_frame = 0
        self.image = self.animation[int(self.current_frame)]


    # def update_location(self):
    #     oldX = self.x
    #     oldY = self.y

    #     self.x += self.curSpeedX
    #     self.y += self.curSpeedY

    #     if globals.collision(self, self.spritesDict["walls"]):
    #         self.x = oldX
    #         self.y = oldY


    # ######################################################################
    # # OTHER

    # def shoot(self):
    #     self.spritesDict["bullets"].append(bullet.Bullet(self.spritesDict, self.x, self.y))

class Weapon(pygame.sprite.Sprite):
    def __init__(self, groups, base_rect):
        super().__init__(groups)
        self.base_rect = base_rect
        # scale the image
        self.image = globals.scale_image(pygame.image.load(os.path.join(".//media//image//tank+weapon//weapon", "0.png")).convert_alpha())
        self.rect = self.image.get_rect(center = self.base_rect.center)

    def update(self):
        self.rect.center = (self.base_rect.center[0], self.base_rect.center[1] - 20)