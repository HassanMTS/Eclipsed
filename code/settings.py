import pygame

# game setup
WIDTH    = 1280
HEIGHT   = 720
FPS      = 60
TILESIZE = 64

# weapons
weapon_data = {
    'sword': {"cooldown":100, "damage": 15, "graphic": "graphics/weapons/sword/full.png"},
    'lance': {"cooldown":400, "damage": 30, "graphic": "graphics/weapons/lance/full.png"},
    'axe': {"cooldown":300, "damage": 20, "graphic": "graphics/weapons/axe/full.png"},
    'rapier': {"cooldown":50, "damage": 8, "graphic": "graphics/weapons/rapier/full.png"},
    'sai': {"cooldown":80, "damage": 10, "graphic": "graphics/weapons/sai/full.png"}
}

magic_data = {
    "flame": {'strength': 5, "cost": 20, "graphic": "graphics/particles/flame/fire.png"},
    "heal": {'strength': 20, "cost": 10, "graphic": "graphics/particles/heal/heal.png"}
}

# UI
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = "graphics/font/joystix.ttf"
UI_FONT_SIZE = 18

# General colors
WATER_COLOR = "#71ddee"
UI_BG_COLOR = "#222222"
UI_BORDER_COLOR = "#111111"
TEXT_COLOR = "#EEEEEE"

# UI colors
HEALTH_COLOR = "red"
ENERGY_COLOR = "blue"
UI_BORDER_COLOR_ACTIVE = "gold"

# Upgrade menu
TEXT_COLOR_SELECTED = "#111111"
BAR_COLOR = "#EEEEEE"
BAR_COLOR_SELECTED = "#111111"
UPGRADE_BG_COLOR_SELECTED = "#EEEEEE"

TEXTBOX_HEIGHT = 150
TEXTBOX_SIDE_OFFSET = 200
TEXTBOX_BOTTOM_OFFSET = 25
TEXT_OFFSET = 15
FONT = UI_FONT
FONT_SIZE = UI_FONT_SIZE
#TEXT_COLOR = 'red'
TEXT_VERTICAL_DISTANCE = 30
TEXTBOX_BORDER_COLOR = UI_BORDER_COLOR
TEXTBOX_BG_COLOR = UI_BG_COLOR
TEXT_LINES_NUM = 4

BOSS_BAR_OFFSET = 200
BOSS_BAR_HEIGHT = 40
BOSS_BAR_HEIGHT_OFFSET = 30


# Enemy
monster_data = {
    'squid':{"health": 100, "exp": 100, "damage": 20, "attack_type": "slash", "attack_sound":"audio/attack/slash.wav", 'speed': 3, "resistance": 3, "attack_radius": 80, "notice_radius": 360},
    'raccoon':{"health": 300, "exp": 250, "damage": 40, "attack_type": "claw", "attack_sound":"audio/attack/claw.wav", 'speed': 2, "resistance": 3, "attack_radius": 120, "notice_radius": 400},
    'spirit':{"health": 100, "exp": 110, "damage": 8, "attack_type": "thunder", "attack_sound":"audio/attack/fireball.wav", 'speed': 4, "resistance": 3, "attack_radius": 60, "notice_radius": 350},
    'bamboo':{"health": 70, "exp": 120, "damage": 6, "attack_type": "leaf_attack", "attack_sound":"audio/attack/slash.wav", 'speed': 3, "resistance": 3, "attack_radius": 50, "notice_radius": 300}
}

warp_data = {
    1:{
        0:{"map":2, "zone":0, "offset":pygame.math.Vector2(0,TILESIZE)},
        1:{"map":2, "zone":1, "offset":pygame.math.Vector2(0,TILESIZE)},
        2:{"map":2, "zone":2, "offset":pygame.math.Vector2(0,TILESIZE)}
    },
    2:{
        0:{"map":1, "zone":0, "offset":pygame.math.Vector2(0,-TILESIZE)},
        1:{"map":1, "zone":1, "offset":pygame.math.Vector2(0,-TILESIZE)},
        2:{"map":1, "zone":2, "offset":pygame.math.Vector2(0,-TILESIZE)}
    }
}
