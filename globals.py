import os
import pygame

pygame.init() # <- ? does this go here
pygame.mixer.pre_init(44100, -16, 2, 512)

DISPLAY_WIDTH = 1440
DISPLAY_HEIGHT = 890
IMAGE_SCALE = 0.7
TILE = 90

# SOUNDS
POWERUP_SOUND = pygame.mixer.Sound("./Audio/sfx/forceField_003.ogg")
# PLAYER SOUNDS
NORMAL_LASER_SOUND = pygame.mixer.Sound("./Audio/sfx/laserSmall_002.ogg")
TWIN_LASER_SOUND = pygame.mixer.Sound("./Audio/sfx/laserSmall_003.ogg")
PLAYER_EXPLOSION_SOUND = pygame.mixer.Sound("./Audio/sfx/explosionCrunch_004.ogg")
PLAYER_HIT_SOUND = pygame.mixer.Sound("./Audio/sfx/impactPlate_medium_002.ogg")
# ENEMY SOUNDS
SMALL_ENEMY_LASER_SOUND = pygame.mixer.Sound("./Audio/sfx/laserSmall_004.ogg")
SMALL_ENEMY_EXPLOSION_SOUND = pygame.mixer.Sound("./Audio/sfx/explosionCrunch_000.ogg")
ENEMY_HIT_SOUND = pygame.mixer.Sound("./Audio/sfx/impactPlate_medium_001.ogg")

# EXPLOSION
EXPLOSION_SOUND = pygame.mixer.Sound("./Audio/sfx/explosionCrunch_000.ogg")
# SET VOLUME
NORMAL_LASER_SOUND.set_volume(0.20)
TWIN_LASER_SOUND.set_volume(0.25)
SMALL_ENEMY_LASER_SOUND.set_volume(0.25)
POWERUP_SOUND.set_volume(0.12)
EXPLOSION_SOUND.set_volume(0.04)
PLAYER_EXPLOSION_SOUND.set_volume(0.15)
PLAYER_HIT_SOUND.set_volume(0.20)
ENEMY_HIT_SOUND.set_volume(0.15)


# spritesToTestAgainstArr can either be a single sprite or an array of similar sprites (ex. enemies, walls etc.)
# returns an array of all the elements to test against it collided with
def collision(spriteToTest, spritesToTestAgainstArr):

    collidedWithArr = []

    # the values need to be aadjusted to be within the range of the window or it messes up the calculations
    def outside_range_fixer(arr, coord):
        output = []
        for num in arr:
            if num < 0:
                num = 0
            elif coord == "x" and num > DISPLAY_WIDTH:
                num = DISPLAY_WIDTH
            elif coord == "y" and num > DISPLAY_HEIGHT:
                num = DISPLAY_HEIGHT
            output.append(num)
        return output


    # min, max
    x = [spriteToTest.x, spriteToTest.x + spriteToTest.get_width()]
    x = outside_range_fixer(x, "x")
    y = [spriteToTest.y, spriteToTest.y + spriteToTest.get_height()]
    y = outside_range_fixer(y, "y")
    
    if type(spritesToTestAgainstArr) != list: spritesToTestAgainstArr = [spritesToTestAgainstArr]

    for spriteToTestAgainst in spritesToTestAgainstArr:
        xTarget = [spriteToTestAgainst.x, spriteToTestAgainst.x + spriteToTestAgainst.get_width()]
        xTarget = outside_range_fixer(xTarget, "x")
        yTarget = [spriteToTestAgainst.y, spriteToTestAgainst.y + spriteToTestAgainst.get_height()]
        yTarget = outside_range_fixer(yTarget, "y")

        xCollision = False
        for num in x:
            if num >= xTarget[0] and num <= xTarget[1]:
                xCollision = True

        yCollision = False
        for num in y:
            if num >= yTarget[0] and num <= yTarget[1]:
                yCollision = True

        if xCollision and yCollision:
            collidedWithArr.append(spriteToTestAgainst)
    
    return collidedWithArr


# returns an array containing just the sprites
def dict_to_list(inputDict):
    outputArr = []
    for listItem in inputDict.values():
        for sprite in listItem:
            outputArr.append(sprite)
    return outputArr

def count_image(path):
    count = 0
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)): count += 1
    return count

def scale_image(image):
    return pygame.transform.smoothscale(image, (image.get_width() * IMAGE_SCALE, image.get_height() * IMAGE_SCALE)).convert_alpha()