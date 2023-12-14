import pygame
from settings import *
from debug import debug
from support import import_folder
from entity import Entity

class Player(Entity):
    def __init__(self, pos, groups, change_active_level):#, obstacle_sprites, interactable_sprites, create_attack, destroy_attack, create_magic, toggle_text_box):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-6, -26)
        self.interaction_box = pygame.Rect(0,0,self.image.get_width() // 4, self.image.get_height() // 4)
        self.sprite_type = "player"

        # Graphics setup
        self.import_player_assets()
        self.status = "down"

        # Level functions
        self.level_funcs = {}
        self.change_active_level = change_active_level

        # Movement
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        # sprites
        self.level_sprites = {}
        #self.obstacle_sprites = obstacle_sprites
        #self.interactable_sprites = interactable_sprites

        # Weapon
        #self.create_attack = create_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        #self.destroy_attack = destroy_attack
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        # Magic
        #self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None


        # Stats
        self.stats = {'health':100, "energy":60, "attack":10, "magic":4, "speed":5}
        self.max_stats = {'health':300, "energy":140, "attack":20, "magic":10, "speed":10}
        self.upgrade_cost = {'health':100, "energy":100, "attack":100, "magic":100, "speed":100}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 5000
        self.speed = self.stats['speed']

        # Invincibility timer
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 500

        # import sound
        self.weapon_attack_sound = pygame.mixer.Sound('audio/sword.wav')
        self.weapon_attack_sound.set_volume(0.4)

        self.can_switch_level = True
        self.switch_level_time = None

        # toggle menu
        #self.toggle_text_box = toggle_text_box

    def import_player_assets(self):
        character_path = "graphics/player/"
        self.animations = {
            "up":[], "down":[], "left":[], "right":[],
            "right_idle":[], "left_idle":[], "up_idle":[], "down_idle":[],
            "right_attack":[], "left_attack":[], "up_attack":[], "down_attack":[]
        }

        for animation in self.animations.keys():
            full_path = character_path + "/" + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()

            # Movement import
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and not (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
                self.direction.x = -1
                self.status = "left"
            elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not (keys[pygame.K_LEFT] or keys[pygame.K_a]):
                self.direction.x = 1
                self.status = "right"
            else:
                self.direction.x = 0

            if (keys[pygame.K_UP] or keys[pygame.K_w]) and not (keys[pygame.K_DOWN] or keys[pygame.K_s]):
                self.direction.y = -1
                self.status = "up"
            elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and not (keys[pygame.K_UP] or keys[pygame.K_w]):
                self.direction.y = 1
                self.status = "down"
            else:
                self.direction.y = 0

            # Attack input
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.level_funcs[self.active_level]["create_attack"]()
                self.weapon_attack_sound.play()

            # Magic input
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = self.magic
                strength = magic_data[self.magic]["strength"] + self.stats['magic']
                cost = magic_data[self.magic]["cost"]
                self.level_funcs[self.active_level]["create_magic"](style, strength, cost)

            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                self.weapon_index += 1
                if self.weapon_index >= len(weapon_data.keys()):
                    self.weapon_index = 0
                self.weapon = list(weapon_data.keys())[self.weapon_index]

            if keys[pygame.K_e] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()
                self.magic_index += 1
                if self.magic_index >= len(magic_data.keys()):
                    self.magic_index = 0
                self.magic = list(magic_data.keys())[self.magic_index]

            if keys[pygame.K_RETURN]:
                if self.status.split("_")[0] == "up":
                    self.interaction_box.midbottom = self.rect.midtop
                elif self.status.split("_")[0] == "down":
                    self.interaction_box.midtop = self.rect.midbottom
                elif self.status.split("_")[0] == "left":
                    self.interaction_box.midright = self.rect.midleft
                elif self.status.split("_")[0] == "right":
                    self.interaction_box.midleft = self.rect.midright

                for sprite in self.level_sprites[self.active_level]["interactable_sprites"].sprites():
                    if sprite.interaction_box.colliderect(self.interaction_box):
                        self.level_funcs[self.active_level]["toggle_text_box"](sprite.text_box)
                        sprite.text_box.can_input = False
                        sprite.text_box.input_time = pygame.time.get_ticks()

            if keys[pygame.K_p] and self.can_switch_level:
                self.level_funcs[self.active_level]["reset_enemy_positions"]()
                if self.active_level == 1:
                    self.change_active_level(2)
                    self.active_level = 2

                elif self.active_level == 2:
                    self.change_active_level(1)
                    self.active_level = 1

                self.can_switch_level = False
                self.switch_level_time = pygame.time.get_ticks()

    def get_status(self):

        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not "attack" in self.status:
                self.status += "_idle"

        # Attack

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace("_idle", "_attack")
                else:
                    self.status += '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace("_attack", "")

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.level_funcs[self.active_level]["destroy_attack"]()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True
                self.hit_time = None

        if not self.can_switch_level:
            if current_time - self.switch_level_time >= 300:
                self.can_switch_level = True
                self.switch_level_time = None

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_full_weapon_damage(self):
        base_damage = self.stats["attack"]
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage

    def get_full_magic_damage(self):
        base_damage = self.stats["magic"]
        spell_damage = magic_data[self.magic]['strength']
        return base_damage + spell_damage

    def energy_recovery(self):
        if self.energy < self.stats['energy']:
            self.energy += 0.01 * self.stats['magic']
        else:
            self.energy = self.stats['energy']

    def get_value_by_index(self, index):
        return list(self.stats.values())[index]

    def get_cost_by_index(self, index):
        return list(self.upgrade_cost.values())[index]

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.stats['speed'])
        self.energy_recovery()
