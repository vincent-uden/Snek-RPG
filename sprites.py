import pygame as pg
from settings import *
from random import randint, uniform
from attacks import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game   = game
        self.images = game.player_imgs
        self.image  = self.images[0]
        self.rect   = self.image.get_rect()
        self.vel    = vec(0, 0)
        self.pos    = vec(x, y)
        self.facing = vec(0, 1)
        self.stats  = {"level"     :1,           # 0
                       "xp"        :0,           # 1
                       "max_hp"    :10,          # 2
                       "current_hp":10,          # 3
                       "name"      :"Curtis",    # 4
                       "strength"  :1,           # 5
                       "speed"     :50,          # 6
                       "accuracy"  :1,           # 7
                       "defence"   :1}           # 8
        self.inventory = []
        self.attacks = [quick_attack1, power_attack1, special_attack1]
        self.equipped = [None]

    def get_texture(self, direction):
        return self.images[direction]

    def attack(self, target):
        if self.get_weapon() != None:
            dmg = randint(0, self.get_stat(5) + self.get_weapon().str_bonus)
        else:
            dmg = randint(0, self.get_stat(5))
        hit_chance = min(target.get_stat(7) / self.get_stat(8), 1) # Accuracy cannot be more than 100%
        hit_roll = uniform(0.0, 1.0)
        if hit_roll > 1 - hit_chance: # Inverse of hit_chance is chance of missing
            target.change_stat(3, -dmg)


    def get_stat(self, stat):
        mapping = [k for k in self.stats.keys()]
        return self.stats[mapping[stat]]

    def set_stat(self, stat, value):
        mapping = [k for k in self.stats.keys()]
        self.stats[mapping[stat]] = value

    def change_stat(self, stat, value):
        mapping = [k for k in self.stats.keys()]
        self.stats[mapping[stat]] += value

    def get_keys(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.vel.x    = -PLAYER_SPEED
            self.target   = (self.rect.x - 40, self.rect.y)
            self.facing.x = -1
            self.facing.y = 0
            self.image    = self.images[1]
        elif keys[pg.K_d]:
            self.vel.x    = PLAYER_SPEED
            self.target   = (self.rect.x + 40, self.rect.y)
            self.facing.x = 1
            self.facing.y = 0
            self.image    = self.images[2]
        elif keys[pg.K_w]:
            self.vel.y    = -PLAYER_SPEED
            self.target   = (self.rect.x, self.rect.y - 40)
            self.facing.x = 0
            self.facing.y = -1
            self.image    = self.images[3]
        elif keys[pg.K_s]:
            self.vel.y    = PLAYER_SPEED
            self.target   = (self.rect.x, self.rect.y + 40)
            self.facing.x = 0
            self.facing.y = 1
            self.image    = self.images[0]

    def collide_with_walls(self, dir):
        if dir == "x":
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == "y":
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    def update(self):
        if self.vel.x == 0 and self.vel.y == 0:
            self.get_keys()
        elif self.vel.x != 0:
            if abs(self.vel.x * self.game.dt) > abs(self.pos.x - self.target[0]):
                self.pos.x = self.target[0]
                self.vel.x = 0
        elif self.vel.y != 0:
            if abs(self.vel.y * self.game.dt) > abs(self.pos.y - self.target[1]):
                self.pos.y = self.target[1]
                self.vel.y = 0

        self.pos.x += self.vel.x * self.game.dt
        self.pos.y += self.vel.y * self.game.dt

        self.rect.x = self.pos.x
        self.collide_with_walls("x")
        self.rect.y = self.pos.y
        self.collide_with_walls("y")

    def use_item(self, index):
        if index < len(self.inventory):
            useing = getattr(self.inventory[index], "use", None)
            if callable(useing):
                self.inventory[index].use()
                if self.inventory[index].consumeable:
                    self.inventory.pop(index)
                    return True

    def get_weapon(self):
        return self.equipped[0]

    def equip_weapon(self, weapon):
        if self.get_weapon() != None:
            self.inventory.append(self.get_weapon())
        self.equipped[0] = weapon

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(LIGHTGREY)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Tile(pg.sprite.Sprite):
    def __init__(self, game, x, y, texture):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = texture
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class MapTexture(pg.sprite.Sprite):
    def __init__(self, game, x, y, texture):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = texture
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Grid(pg.sprite.Sprite):
    def __init__(self, game, x, y, texture):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = texture
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Npc(pg.sprite.Sprite):
    def __init__(self, game, x, y, texture):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = texture
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rect.x = x
        self.rect.y = y
        Obstacle(game, x, y, 40, 40)

    def update(self):
        pass

    def get_texture(self, direction):
        return self.image

class Enemy(Npc):
    def __init__(self, game, x ,y ,texture, name):
        super().__init__(game, x , y, texture)
        self.stats = {"level"     :1,
                      "xp"        :0,
                      "max_hp"    :10,
                      "current_hp":10,
                      "name"      :name,
                      "strength"  :1,
                      "speed"     :50,
                      "accuracy"  :1,
                      "defence"   :1}

    def get_stat(self, stat):
        mapping = [k for k in self.stats.keys()]
        return self.stats[mapping[stat]]

    def set_stat(self, stat, value):
        mapping = [k for k in self.stats.keys()]
        self.stats[mapping[stat]] = value

    def change_stat(self, stat, value):
        mapping = [k for k in self.stats.keys()]
        self.stats[mapping[stat]] += value

    def attack(self, target):
        dmg = randint(0, self.get_stat(5) + self.get_weapon().str_bonus)
        hit_chance = min(target.get_stat(7) / self.get_stat(8), 1) # Accuracy cannot be more than 100%
        hit_roll = uniform(0.0, 1.0)
        if hit_roll > 1 - hit_chance: # Inverse of hit_chance is chance of missing
            target.change_stat(-dmg)
