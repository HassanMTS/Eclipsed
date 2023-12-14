import pygame
from math import sin

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.centerx += self.direction.x * speed
        self.collision("horizontal")

        self.hitbox.centery += self.direction.y * speed
        self.collision("vertical")

        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if self.sprite_type == "player":
            obstacle_sprites = self.level_sprites[self.active_level]["obstacle_sprites"]
        else:
            obstacle_sprites = self.obstacle_sprites

        if self.sprite_type == "player":
            for warp_zone in self.level_sprites[self.active_level]["warp_sprites"].sprites():
                if warp_zone.hitbox.colliderect(self.hitbox):
                    self.level_funcs[self.active_level]["reset_enemy_positions"]()
                    self.change_active_level(warp_zone.map, (warp_zone.warp_linked, warp_zone.offset))
                    self.active_level = warp_zone.map
                    #self.hitbox.topleft = (warp_zone.x, warp_zone.y)

        if direction == "horizontal":
            for sprite in obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == "vertical":
            for sprite in obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0
