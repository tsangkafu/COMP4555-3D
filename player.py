import pygame
import globals
from bullet import Bullet
import os

class Player(pygame.sprite.Sprite):

    ######################################################################
    # CONSTRUCTOR
    def __init__(self, groups):#, spritesDict):
        super().__init__(groups)
        # self.spritesDict = spritesDict
        self.name = "player"
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
        self.weapon = Weapon(groups, self)
        self.hp_bar = HealthBar(groups, self)
        self.speed = 10
        self.bullet_sprites = pygame.sprite.Group()
        self.bullet = 3
        self.shoot_cooldown = 0

        self.max_hp = 3
        self.hp = 3
        self.shield = 0
        


    ######################################################################
    # GETTERS

    def get_width(self):
        return self.image.get_width()

    def get_height(self):
        return self.image.get_height()


    ######################################################################
    # OPTIONAL
        
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left >= 0:
            self.rect.x -= self.speed
        elif keys[pygame.K_RIGHT] and self.rect.right <= globals.DISPLAY_WIDTH:
            self.rect.x += self.speed
        
        if keys[pygame.K_SPACE]:
            # limit the bullet that the player can shot
            if self.shoot_cooldown == 0:
                if len(self.bullet_sprites) < self.bullet:
                    if self.weapon.type == "normal":
                        pygame.mixer.Sound.play(globals.NORMAL_LASER_SOUND)
                        Bullet(self.bullet_sprites, self, 0)
                        self.shoot_cooldown = 20
                    if self.weapon.type == "twin":
                        pygame.mixer.Sound.play(globals.TWIN_LASER_SOUND)
                        Bullet(self.bullet_sprites, self, -1)
                        Bullet(self.bullet_sprites, self, 1)
                        self.shoot_cooldown = 20
                    if self.weapon.type == "plasma":
                        pygame.mixer.Sound.play(globals.PLASMA_LASER_SOUND)
                        Bullet(self.bullet_sprites, self, 0)
                        self.shoot_cooldown = 5
                    

        # decrement shoot_cooldown on each loop
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        # animate the player
        # current frame increment being the speed of how fast the animation is
        self.current_frame += 0.2

        # reset the frame when the current frame exceed the number of available image
        if self.current_frame >= len(self.animation):
            self.current_frame = 0
        self.image = self.animation[int(self.current_frame)]
        
# mapping for the image file and bullet number, the first value being the image index, the second being the bullet number
WEAPON_MAP = {
    "normal": [0, 3],
    "twin": [1, 6],
    "laser": [2, 1],
    "plasma": [3, 10]
}

class Weapon(pygame.sprite.Sprite):
    def __init__(self, groups, player):
        super().__init__(groups)
        self.type = "normal"
        self.player = player
        # scale the image
        self.image = globals.scale_image(pygame.image.load(os.path.join(".//media//image//tank+weapon//weapon", "0.png")).convert_alpha())
        self.rect = self.image.get_rect(center = self.player.rect.center)

    def update(self):
        self.rect.center = (self.player.rect.center[0], self.player.rect.center[1] - 20)

    def switch_weapon(self, type):
        self.type = type
        weapon_index = WEAPON_MAP[type][0]
        self.image = globals.scale_image(pygame.image.load(os.path.join(".//media//image//tank+weapon//weapon", str(weapon_index) + ".png")).convert_alpha())
        self.player.bullet = WEAPON_MAP[type][1]

class HealthBar(pygame.sprite.Sprite):
    def __init__(self, groups, player):
        super().__init__(groups)
        self.player = player
        self.player_rect = player.rect
        self.hp_bar_w = self.player_rect.w
        self.image = pygame.Surface((self.hp_bar_w, 10)).convert_alpha()
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(center = self.player_rect.center)
    
    def update(self):
        ratio = self.player.hp / self.player.max_hp
        new_hp_bar_w = self.hp_bar_w * ratio
        if self.player.hp <= 0:
            new_hp_bar_w = 0
        self.image = pygame.Surface((new_hp_bar_w, 10)).convert_alpha()
        if ratio == 1:
            self.image.fill((0, 255, 0))
        elif ratio > 0.5:
            self.image.fill((255, 255, 0))
        else:
            self.image.fill((255, 0, 0))
        self.rect.center = self.player_rect.midbottom

class Shield(pygame.sprite.Sprite):
    def __init__(self, groups, player):
        super().__init__(groups)
        self.player = player
        self.player_rect = player.rect
        self.hp = 2
        # count the number of image in one file, this will change because different sprite has different files
        path = ".//media//image//bullet + fx + powerup + coin//bubbleshield"
        num_of_img = globals.count_image(path)
        
        # a list that store all the image of a sprite
        self.animation = []
        # loop through each image and append it to the animation list
        for i in range(num_of_img):
            # scale the image
            image = pygame.image.load(os.path.join(path, str(i) + ".png")).convert_alpha()
            self.animation.append(image)
            
        self.current_frame = 0
        self.image = self.animation[self.current_frame]
        self.rect = self.image.get_rect(center = self.player_rect.center)

    def update(self):
        self.rect.center = self.player_rect.center

        # current frame increment being the speed of how fast the animation is
        self.current_frame += 0.2

        # reset the frame when the current frame exceed the number of available image
        if self.current_frame >= len(self.animation):
            self.current_frame = 0
        self.image = self.animation[int(self.current_frame)]

        if self.hp <= 0:
            self.kill()
            del self