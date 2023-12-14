import pygame
from settings import *
from text_box import Text_Box

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface = pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        if sprite_type == 'stump' or sprite_type == 'object':
            self.rect = self.image.get_rect(topleft = (pos[0], pos[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft = pos)

        if sprite_type == 'object':
            self.hitbox = self.rect.inflate(-2,-50)
            self.hitbox.bottom = self.rect.bottom - 5
        else:
            self.hitbox = self.rect.inflate(0,-10)

class Interactable(Tile):
    def __init__(self, pos, groups, sprite_type, text, toggle_text_box, surface):
        super().__init__(pos, groups, sprite_type, surface)
        self.text_box = Text_Box(text, toggle_text_box)
        self.interaction_box = pygame.Rect(0,0,TILESIZE,20)
        self.interaction_box.midbottom = self.rect.midbottom

class Warp_Zone(Tile):
    def __init__(self, pos, warp_info, groups, sprite_type):
        super().__init__(pos, groups, sprite_type)
        self.map = warp_info["map"]
        self.warp_linked = warp_info["zone"]
        self.offset = warp_info["offset"]
