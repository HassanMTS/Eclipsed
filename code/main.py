import pygame, sys
from settings import *
from level import Level
from debug import debug

class Game:

    def __init__(self):

        # General setup
        pygame.init()
        pygame.display.set_caption("Eclipsed")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.active_level = 1
        self.levels = {}
        self.levels[self.active_level] = Level(self.active_level, self.change_active_level)

        # Sound
        main_sound = pygame.mixer.Sound('audio/main.ogg')
        main_sound.set_volume(0.2)
        main_sound.play(loops = -1)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.levels[self.active_level].toggle_menu()

            self.screen.fill("black")
            self.levels[self.active_level].run()
            pygame.display.update()
            self.clock.tick(FPS)

    def change_active_level(self, ID, warp_info):
        if ID in self.levels.keys():
            self.active_level = ID
            self.levels[self.active_level].player.hitbox.center = self.levels[self.active_level].warp_zones[warp_info[0]].rect.center + warp_info[1]
        else:
            self.levels[ID] = Level(ID, self.change_active_level, player = self.levels[self.active_level].player, warp_info = warp_info)
            self.active_level = ID


if __name__ == '__main__':
    game = Game()
    game.run()
