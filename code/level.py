import pygame
from settings import *
from tile import Tile, Interactable, Warp_Zone
from player import Player
from debug import debug
from support import import_csv_layout, import_folder, import_text
from random import choice, randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade
from boss import Boss

class Level:
    def __init__(self, ID, change_active_level, player = None, warp_info = None):

        # Get display surface
        self.screen = pygame.display.get_surface()
        self.game_paused = False
        self.ID = ID

        # Sprite group setup
        self.visible_sprites = YSortCameraGroup(ID)
        self.obstacle_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.interactable_sprites = pygame.sprite.Group()
        self.warp_sprites = pygame.sprite.Group()

        # Attack sprites
        self.current_attack = None

        # Text
        self.text_dict = import_text("game_info/text.txt")
        self.text_on_screen = False
        self.can_toggle_text = True
        self.toggle_text_time = None
        self.toggle_text_cooldown = 150

        # Warps
        self.warp_dict = warp_data[self.ID]
        self.warp_zones = {}

        # Create map
        if player == None:
            self.create_player = True
        else:
            self.create_player = False
            self.player = player
            self.visible_sprites.add(self.player)

        self.change_active_level = change_active_level

        self.create_map(self.ID)

        if not self.create_player:
            self.player.hitbox.center = self.warp_zones[warp_info[0]].rect.center + warp_info[1]

        # Add player functions
        self.player.level_funcs[self.ID] = {}
        self.player.level_funcs[self.ID]["create_attack"] = self.create_attack
        self.player.level_funcs[self.ID]["destroy_attack"] = self.destroy_attack
        self.player.level_funcs[self.ID]["create_magic"] = self.create_magic
        self.player.level_funcs[self.ID]["toggle_text_box"] = self.toggle_text_box
        self.player.level_funcs[self.ID]["reset_enemy_positions"] = self.reset_enemy_positions
        self.player.active_level = self.ID

        self.player.level_sprites[self.ID] = {}
        self.player.level_sprites[self.ID]["obstacle_sprites"] = self.obstacle_sprites
        self.player.level_sprites[self.ID]["interactable_sprites"] = self.interactable_sprites
        self.player.level_sprites[self.ID]["warp_sprites"] = self.warp_sprites

        # User interface
        self.ui = UI()
        self.upgrade = Upgrade(self.player)

        # Animation Player
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

    def create_map(self, ID):
        layout = {
            "boundary":import_csv_layout(f"map/{ID}/map_FloorBlocks.csv"),
            "warps":import_csv_layout(f"map/{ID}/map_Warps.csv"),
            "grass":import_csv_layout(f"map/{ID}/map_Grass.csv"),
            "object":import_csv_layout(f"map/{ID}/map_Objects.csv"),
            "entities": import_csv_layout(f"map/{ID}/map_Entities.csv")
        }

        graphics = {
            'grass':import_folder(f"graphics/Grass"),
            'objects':import_folder(f"graphics/objects")
        }

        for style, layout in layout.items():
            for row_index, row in enumerate(layout):
                for col_index, value in enumerate(row):
                    if value != "-1":
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == "boundary":
                            Tile((x,y), [self.obstacle_sprites], "invisible")

                        if style == "warps":
                            self.warp_zones[int(value)] = Warp_Zone((x,y), self.warp_dict[int(value)], [self.warp_sprites], "warp_zone")

                        if style == "grass":
                            random_grass_image = choice(graphics["grass"])
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites], "grass", random_grass_image)

                        if style == "object":
                            object_surface = graphics["objects"][int(value)]
                            if int(value) == 0 or int(value) == 1:
                                Tile((x,y), [self.visible_sprites, self.obstacle_sprites], "stump", object_surface)
                            elif int(value) == 15 or int(value) == 18:
                                Interactable((x,y),
                                            [self.visible_sprites, self.obstacle_sprites, self.interactable_sprites],
                                            "object",
                                            self.text_dict[f"m{ID}x{x}y{y}"],
                                            self.toggle_text_box,
                                            object_surface)
                            else:
                                Tile((x,y), [self.visible_sprites, self.obstacle_sprites], "object", object_surface)

                        if style == "entities":
                            if value == '394':
                                if self.create_player:
                                    self.player = Player((x,y),
                                                        [self.visible_sprites],
                                                        self.change_active_level)#,
                                                        # self.obstacle_sprites,
                                                        # self.interactable_sprites,
                                                        # self.create_attack,
                                                        # self.destroy_attack,
                                                        # self.create_magic,
                                                        # self.toggle_text_box)
                            else:
                                if value == "390": monster_name = 'bamboo'
                                elif value == "391": monster_name = "spirit"
                                elif value == "392": monster_name = "raccoon"
                                else: monster_name = "squid"
                                if not monster_name == "raccoon":
                                    Enemy(monster_name,
                                        (x,y),
                                        [self.visible_sprites, self.attackable_sprites],
                                        self.obstacle_sprites,
                                        self.damage_player,
                                        self.trigger_death_particles,
                                        self.add_exp)
                                else:
                                    Boss(monster_name,
                                        (x,y),
                                        [self.visible_sprites, self.attackable_sprites],
                                        self.obstacle_sprites,
                                        self.damage_player,
                                        self.trigger_death_particles,
                                        self.add_exp)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def create_magic(self, style, strength, cost):
        if style == "heal":
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])

        if style == "flame":
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
            self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == "grass":
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0,60)
                            for leave in range(randint(3,6)):
                                self.animation_player.create_grass_particles(pos - offset, [self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(particle_type, pos, [self.visible_sprites])

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hit_time = pygame.time.get_ticks()
            # Spawn particles
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

    def add_exp(self, amount):
        self.player.exp += amount

    def toggle_menu(self):

        self.game_paused = not self.game_paused

    def toggle_text_box(self, box = None):
        if self.can_toggle_text:
            self.game_paused = not self.game_paused
            self.text_on_screen = not self.text_on_screen
            self.toggle_text_time = pygame.time.get_ticks()
            self.can_toggle_text = False
            if self.text_on_screen:
                self.text_box = box


    def cooldowns(self):
        if not self.can_toggle_text:
            current_time = pygame.time.get_ticks()
            if current_time - self.toggle_text_time > self.toggle_text_cooldown:
                self.can_toggle_text = True
                self.toggle_text_time = None

    def reset_enemy_positions(self):
        for sprite in self.visible_sprites.sprites():
            if sprite.sprite_type == "enemy":
                sprite.rect.topleft = sprite.start_pos
                sprite.hitbox.center = sprite.rect.center



    def run(self):

        self.cooldowns()
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)

        if self.game_paused:
            # display upgrade menu
            if not self.text_on_screen:
                self.upgrade.display()
            else:
                self.text_box.update(pygame.display.get_surface())
        else:
            # Update and draw the game
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self, ID):

        # general setup
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.half_width = WIDTH // 2
        self.half_height = HEIGHT // 2
        self.offset = pygame.math.Vector2()

        # Creating the floor
        self.floor_surface = pygame.image.load(f"map/{ID}/ground.png").convert()
        self.floor_rect = self.floor_surface.get_rect(topleft = (0,0))

        self.offset_x_limit = self.floor_surface.get_width() - WIDTH
        self.offset_y_limit = self.floor_surface.get_height() - HEIGHT

    def custom_draw(self, player):

        # Getting offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        if self.offset.x < 0:
            self.offset.x = 0
        elif self.offset.x > self.offset_x_limit:
            self.offset.x = self.offset_x_limit

        if self.offset.y < 0:
            self.offset.y = 0
        elif self.offset.y > self.offset_y_limit:
            self.offset.y = self.offset_y_limit

        #for sprite in self.sprites():
        floor_pos = -self.offset
        self.screen.blit(self.floor_surface, floor_pos)

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.screen.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, "sprite_type") and sprite.sprite_type == "enemy"]
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
