import pygame
import psutil
import globals
import wall
import background
import player
import enemy

class Sprites():
    def __init__(self, screen):
        self.screen = screen
        self.dict = {}
        self.populate_dict_always()


    # this is run despite of level
    def populate_dict_always(self):

        self.dict["walls"] = []
        self.dict["walls"].append(wall.Wall(0, 0, 0, globals.DISPLAY_HEIGHT, "vertical left"))
        self.dict["walls"].append(wall.Wall(0, 0, globals.DISPLAY_WIDTH, 0, "horizontal top"))
        self.dict["walls"].append(wall.Wall(globals.DISPLAY_WIDTH, 0, 0, globals.DISPLAY_HEIGHT, "vertical right"))
        self.dict["walls"].append(wall.Wall(0, globals.DISPLAY_HEIGHT, globals.DISPLAY_WIDTH, 0, "horizontal bottom"))

        self.dict["background"] = []
        self.dict["background"].append(background.Background())

        self.dict["player"] = []
        self.dict["player"].append(player.Player(pygame.sprite.Group(), self.dict))

        self.dict["enemies"] = []
        for i in range(6):
            self.dict["enemies"].append(enemy.Enemy(self.dict))

        self.dict["bullets"] = []


    def animate(self):

        def run():
            #print(f"RAM memory % used: {psutil.virtual_memory()[2]}")
            # print(f"RAM Used (GB): {psutil.virtual_memory()[3]/1000000000}")
            rm_unsused_sprites()
            user_input()
            update_locations()
            display_changes()

        def rm_unsused_sprites():
            for listItem in self.dict.values():
                # trick to itterate over an array and remove items from it at the same time
                for sprite in listItem[:]:
                    if hasattr(sprite, 'shouldDelete') and sprite.shouldDelete:
                        listItem.remove(sprite) # this removes its reference in self.dict
                        del sprite # this removes the sprite instance itself

        def user_input():
            for event in pygame.event.get():
                for sprite in globals.dict_to_list(self.dict):
                    if hasattr(sprite, 'user_input'):
                        sprite.user_input(event)

        def update_locations():
            for sprite in globals.dict_to_list(self.dict):
                if hasattr(sprite, 'update_location'):
                    sprite.update_location()
                
                try: self.screen.blit(sprite.image, (sprite.x, sprite.y))
                except: pass

        def display_changes():
            pygame.display.update()

        run()