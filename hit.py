import pygame
import globals
import os


class Hit(pygame.sprite.Sprite):
    # level being the level of the enemy, different enemy will have different exposure animation
    # pos being the position of the
    def __init__(self, groups, pos):
        super().__init__(groups)

        # count the number of image in one file, this will change because different sprite has different files
        path = f".//media//image//bullet + fx + powerup + coin//hit_fx"
        num_of_img = globals.count_image(path)

        # a list that store all the image of a sprite
        self.animation = []

        # loop through each image and append it to the animation list
        for i in range(num_of_img):
            image = globals.scale_image(pygame.image.load(
                os.path.join(path, str(i) + ".png")).convert_alpha())
            self.animation.append(image)

        self.current_frame = 0
        self.image = self.animation[self.current_frame]
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        # animate the explosion
        # current frame increment being the speed of how fast the animation is
        self.current_frame += 1

        # reset the frame when the current frame exceed the number of available image
        if self.current_frame >= len(self.animation):
            self.kill()
            del self
        else:
            self.image = self.animation[int(self.current_frame)]
