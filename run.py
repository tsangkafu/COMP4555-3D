import pygame
import globals
import sys
from level import Level
from sprites import Sprites

#################################################################

class Game():                             
    def __init__(self):
        # pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((globals.DISPLAY_WIDTH, globals.DISPLAY_HEIGHT)) 
        pygame.display.set_caption("Space Invaders")
        self.stage = 1
        self.font = pygame.font.Font("./media/fonts/Retro Gaming.ttf", 72)
        self.sub_text = pygame.font.Font("./media/fonts/Retro Gaming.ttf", 48)

    def run(self):
        self.level = Level(self.screen, self.stage, 0)
        music_playing = True
        victory_sound_control = True

        while (1):
            self.level.run()
            
            # sprites.animate()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_m:
                            if music_playing:
                                pygame.mixer.music.pause()
                                music_playing = False
                            else:
                                pygame.mixer.music.unpause()
                                music_playing = True
            
            # GO TO NEXT STAGE
            if len(self.level.enemy_sprites) == 0:
                if (victory_sound_control):
                    pygame.mixer.Sound.play(globals.VICTORY_SOUND)
                    victory_sound_control = False
                if self.stage < 3:
                    stage_clear_text = self.font.render("STAGE: " + str(self.stage) + " CLEARED", True, ( 0, 255, 150))
                    extraPoints = 500 * self.stage
                    stage_clear_text_3 = self.sub_text.render("BONUS: +" + str(extraPoints) + " POINTS", True, ( 0, 255, 150))
                    stage_clear_text_2 = self.sub_text.render("PRESS ENTER TO CONTINUE", True, (0, 255, 150))
                    self.screen.blit(stage_clear_text, (globals.DISPLAY_WIDTH/2 - stage_clear_text.get_width()/2, globals.DISPLAY_HEIGHT/2 - stage_clear_text.get_height()/2 - 30))
                    self.screen.blit(stage_clear_text_2, (globals.DISPLAY_WIDTH/2 - stage_clear_text_2.get_width()/2, globals.DISPLAY_HEIGHT/2 - stage_clear_text_2.get_height()/2 + 30))
                    self.screen.blit(stage_clear_text_3, (globals.DISPLAY_WIDTH/2 - stage_clear_text_3.get_width()/2, globals.DISPLAY_HEIGHT/2 - stage_clear_text_3.get_height()/2 + 150))
                    
                    if pygame.key.get_pressed()[pygame.K_RETURN]:
                        victory_sound_control = True
                        pygame.mixer.Sound.play(globals.NEXTSTAGE_SOUND)
                        self.stage += 1
                        score = self.level.score_value + extraPoints
                        del self.level
                        self.level = Level(self.screen, self.stage, score)
                if self.stage == 3:
                    extraPoints = 500 * self.stage
                    score = self.level.score_value + extraPoints
                    stage_clear_text = self.font.render("ALL STAGES CLEARED:", True, (0, 255, 150))
                    self.screen.blit(stage_clear_text, (globals.DISPLAY_WIDTH/2 - stage_clear_text.get_width()/2, globals.DISPLAY_HEIGHT/2 - stage_clear_text.get_height()/2 - 30))
                    stage_clear_text_2 = self.font.render("FINAL SCORE: " + str(score), True, (0, 255, 150))
                    self.screen.blit(stage_clear_text_2, (globals.DISPLAY_WIDTH/2 - stage_clear_text_2.get_width()/2, globals.DISPLAY_HEIGHT/2 - stage_clear_text_2.get_height()/2 + 35))
                    stage_clear_text_3 = self.sub_text.render("BONUS: +" + str(extraPoints) + " POINTS", True, ( 0, 255, 150))
                    self.screen.blit(stage_clear_text_3, (globals.DISPLAY_WIDTH/2 - stage_clear_text_3.get_width()/2, globals.DISPLAY_HEIGHT/2 - stage_clear_text_3.get_height()/2 + 150))

                    stage_clear_text_4 = self.sub_text.render("PRESS BACKSPACE TO PLAY AGAIN", True, (0, 255, 150))
                    self.screen.blit(stage_clear_text_4, (globals.DISPLAY_WIDTH/2 - stage_clear_text_4.get_width()/2, globals.DISPLAY_HEIGHT/2 - stage_clear_text_4.get_height()/2 + 100))
                    if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
                        del self.level
                        self.stage = 1
                        self.level = Level(self.screen, self.stage, 0)

            # PLAYER DEATH RESTART SCREEN
            if self.level.player.hp <= 0:
                stage_clear_text = self.font.render("GAME OVER", True, (0, 255, 150))
                self.screen.blit(stage_clear_text, (globals.DISPLAY_WIDTH/2 - stage_clear_text.get_width()/2, globals.DISPLAY_HEIGHT/2 - stage_clear_text.get_height()/2 - 30))
                stage_clear_text_2 = self.font.render("YOUR SCORE: " + str(self.level.score_value), True, (0, 255, 150))
                self.screen.blit(stage_clear_text_2, (globals.DISPLAY_WIDTH/2 - stage_clear_text_2.get_width()/2, globals.DISPLAY_HEIGHT/2 - stage_clear_text_2.get_height()/2 + 35))
                stage_clear_text_3 = self.sub_text.render("PRESS ENTER TO TRY AGAIN", True, (0, 255, 150))
                self.screen.blit(stage_clear_text_3, (globals.DISPLAY_WIDTH/2 - stage_clear_text_3.get_width()/2, globals.DISPLAY_HEIGHT/2 - stage_clear_text_3.get_height()/2 + 100))
                if pygame.key.get_pressed()[pygame.K_RETURN]:
                    pygame.mixer.Sound.play(globals.RETRY_SOUND) 
                    self.stage = 1 # restarts to first level
                    del self.level
                    self.level = Level(self.screen, self.stage, 0)

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()