import pygame
import globals
import random
import os
from bullet import Bullet


class Enemy(pygame.sprite.Sprite):

    ######################################################################
    # CONSTRUCTOR

    # groups being the enemy sprites
    # level being the enemy level, there are total 6 levels of different enemy we can use
    # feel free to mix and match
    # level 0 being the basic ufo
    # level 1 - 6 are new enemy (level 5 being the biggest, level 6 is just some normal enemy)
    # here provided a list that what colors are available in what enemies
    # bullet being the bullet type that the enemy has, there's 3 bullet type
    ENEMIES_CONFIG = {
        0: {
            "color": ["red", "pink", "blue"],
            "hp": 2,
            "bullet": 1,
            "cd": 20000
        },
        1: {
            "color": ["red", "blue"],
            "hp": 1,
            "bullet": 1,
            "cd": 20000
        },
        2: ["red", "blue"],
        3: ["blue", "yellow"],
        4: ["green", "blue"],
        5: ["green", "blue"],
        6: ["orange", "red"]
    }
    def __init__(self, groups, level, color, pos):#spritesDict):
        super().__init__(groups)
        #self.spritesDict = spritesDict
        self.level = level
        self.name = "enemy"
        self.bullet_sprites = pygame.sprite.Group()
        # you can change to tank_blue/tank_pink
        self.color = color
        # change this to change the animation set of the enemy
        # there are "rotation", "shot", and "walk", some sprites may not have all
        # but all sprite has rotation
        self.action = "rotation"

        # count the number of image in one file, this will change because different sprite has different files
        path = f".//media//image//invader_{str(level)}//invader_{str(level)}_{self.color}_{self.action}"
        num_of_img = globals.count_image(path)
        
        # a list that store all the image of a sprite
        self.animation = []
        # loop through each image and append it to the animation list
        for i in range(num_of_img):
            # scale only enemies that is not level 1 (cause level 1 is small already)
            if level != 1:
                image = globals.scale_image(pygame.image.load(os.path.join(path, str(i) + ".png")).convert_alpha())
                self.animation.append(image)
            else:
                self.animation.append(pygame.image.load(os.path.join(path, str(i) + ".png")).convert_alpha())
            
        self.current_frame = random.randint(0, len(self.animation) - 1)
        self.image = self.animation[self.current_frame]
        
        self.rect = self.image.get_rect(topleft = pos)

        self.hp = Enemy.ENEMIES_CONFIG[self.level]["hp"]
        self.bullet = Enemy.ENEMIES_CONFIG[self.level]["bullet"]
        self.cd = Enemy.ENEMIES_CONFIG[self.level]["cd"]
        self.cd_tracker = pygame.time.get_ticks() - random.randint(0, self.cd)

        self.speed = 3

        # velocity[0] = speed X
        # velocity[1] = speed Y
        self.velocity = [self.speed, self.speed]
        
        # self.x = random.randint(0, globals.DISPLAY_WIDTH - self.get_width())
        # self.y = random.randint(0, globals.DISPLAY_HEIGHT - 300) # 300 being the distance from the bottom

        # self.curSpeedX = 2
        # self.curSpeedY = 0

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
    # change direction when on border
        if self.rect.right >= globals.DISPLAY_WIDTH or self.rect.left <= 0:
            self.speed *= -1

        self.rect.x += self.speed

        # animate the enemy
        # current frame increment being the speed of how fast the animation is
        self.current_frame += 0.2

        # reset the frame when the current frame exceed the number of available image
        if self.current_frame >= len(self.animation):
            self.current_frame = 0
        self.image = self.animation[int(self.current_frame)]

        self.shoot()

    # shoot every {cd} second
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.cd_tracker >= self.cd:
            pygame.mixer.Sound.play(globals.SMALL_ENEMY_LASER_SOUND)
            Bullet(self.bullet_sprites, self, 0)
            self.cd_tracker = now





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
    #             if wallSprite.description.startswith("vertical"):
    #                 self.curSpeedX *= -1
    #                 self.y += 40
    #             elif wallSprite.description == "horizontal bottom":
    #                 self.shouldDelete = True
            
