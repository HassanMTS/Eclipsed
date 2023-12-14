import pygame
from settings import *
from enemy import Enemy
from math import dist

class Boss(Enemy):
    def __init__(self, boss_name, pos, groups, obstacle_sprites, damage_player, trigger_death_particles, add_exp):
        super().__init__(boss_name, pos, groups, obstacle_sprites, damage_player, trigger_death_particles, add_exp)
        self.display_surface = pygame.display.get_surface()

        self.health_bar_rect = pygame.Rect(BOSS_BAR_OFFSET, HEIGHT - BOSS_BAR_HEIGHT_OFFSET - BOSS_BAR_HEIGHT, WIDTH - 2 * BOSS_BAR_OFFSET, BOSS_BAR_HEIGHT)
        self.max_health = self.health

        self.font = pygame.font.Font(UI_FONT, FONT_SIZE + 5)
        self.boss_text_surf = self.font.render(boss_name, False, TEXT_COLOR)
        self.boss_text_rect = self.boss_text_surf.get_rect(midbottom = self.health_bar_rect.midtop + pygame.math.Vector2(0,-10))

        self.fight_started = False

    def show_bar(self):
        if self.fight_started:
            pygame.draw.rect(self.display_surface, UI_BG_COLOR, self.health_bar_rect)
            ratio = self.health / self.max_health
            current_width = self.health_bar_rect.width * ratio
            current_rect = self.health_bar_rect.copy()
            current_rect.width = current_width

            pygame.draw.rect(self.display_surface, HEALTH_COLOR, current_rect)
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, self.health_bar_rect, 3)
            self.display_surface.blit(self.boss_text_surf, self.boss_text_rect)

    def detect_fight(self, player):
        if "attack" in self.status or "move" in self.status:
            self.fight_started = True
        else:
            if dist(self.hitbox.center, player.hitbox.center) >= 600:
                self.fight_started = False
                self.health = self.max_health

    def enemy_update(self, player):
        self.get_status(player)
        self.detect_fight(player)
        self.actions(player)
        self.show_bar()
