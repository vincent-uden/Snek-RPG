import pygame as pg
import sys
import math
from settings import *

def f():
    return None

class MenuText:

    def __init__(self, text, screen):
        self.font = pg.font.Font("./resources/PressStart2P.ttf", 16)
        self.screen_text = self.font.render(text, True, BLACK)
        self.screen = screen

    def draw(self, x, y):
        self.screen.blit(self.screen_text, (x, y))

    def update(self, new_text):
        self.screen_text = self.font.render(new_text, True, BLACK)

class Gui_base:
    def __init__(self, screen, texture, x, y):
        self.screen = screen
        self.image = texture
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

class PauseMenu(Gui_base):
    def __init__(self, screen, texture, x, y, menus):
        super().__init__(screen, texture, x, y)
        self.pointer = pg.image.load("./gui_textures/selection.png")
        self.selected = 0
        self.menus = menus

    def move_pointer(self, direction):
        self.selected += direction
        if self.selected < 0:
            self.selected = 0
        if self.selected >= len(self.menus):
            self.selected = len(self.menus) - 1

    def draw(self):
        super().draw()
        self.screen.blit(self.pointer, (self.x + 30, self.y + 62 + self.selected * 40))
        self.menus[self.selected].draw()

    def execute(self):
        self.menus[self.selected].open()

class StatsMenu(Gui_base):
    def __init__(self, screen, texture, x, y, player):
        super().__init__(screen, texture, x, y)
        self.player = player
        self.hp_text    = MenuText(f"{self.player.get_stat(3)}/{self.player.get_stat(2)}", screen)
        self.level_text = MenuText(f"{self.player.get_stat(0)}", screen)
        self.xp_text    = MenuText(f"{self.player.get_stat(1)}", screen)
        self.name_text  = MenuText(f"{self.player.get_stat(4)}", screen)

    def draw(self):
        super().draw()
        self.hp_text.update(f"{self.player.get_stat(3)}/{self.player.get_stat(2)}")
        self.level_text.update(f"{self.player.get_stat(0)}")
        self.xp_text.update(f"{self.player.get_stat(1)}")
        self.name_text.update(f"{self.player.get_stat(4)}")
        self.hp_text.draw(445, 92)
        self.level_text.draw(380, 150)
        self.xp_text.draw(92, 150)
        self.name_text.draw(120, 92)

    def open(self):
            self.draw()
            pg.display.flip()

class InventoryMenu(Gui_base):
    def __init__(self, screen, texture, x, y, player):
        super().__init__(screen, texture, x, y)
        self.player = player
        self.pointer = pg.image.load("./gui_textures/selection.png")
        self.selected = 0

    def draw(self):
        super().draw()
        for index, item in enumerate(self.player.inventory):
            MenuText(f"{item.name}", self.screen).draw(83, 125 + index * 20)
            MenuText(f"{item.value}", self.screen).draw(500, 125 + index * 20)

    def move_pointer(self, direction):
        self.selected += direction
        if self.selected < 0:
            self.selected = 0
        if self.selected >= len(self.player.inventory):
            self.selected = len(self.player.inventory) - 1
        if len(self.player.inventory) == 0:
            self.selected = 0

    def execute(self):
        if len(self.player.inventory) >= 0:
            self.player.inventory[self.selected].use()

    def open(self):
        is_open = True
        while is_open:
            self.draw()
            if len(self.player.inventory) >= 0:
                self.screen.blit(self.pointer, (self.x + 50, self.y + 108 + self.selected * 20))
            pg.display.flip()
            # Event loop which overrides all other controls
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_p or event.key == pg.K_TAB:
                        is_open = False
                    elif event.key == pg.K_s:
                        self.move_pointer(1)
                    elif event.key == pg.K_w:
                        self.move_pointer(-1)
                    elif event.key == pg.K_e or event.key == pg.K_RETURN:
                        consumed = self.player.use_item(self.selected)
                        if consumed:
                            if self.selected > 0:
                                self.selected -= 1

class ShowEq:
    def __init__(self, player):
        self.player = player

    def open(self):
        for item in self.player.equipped:
            print(item)

    def draw(self):
        return None

class HpBar(Gui_base):
    def __init__(self, screen, x, y, entity):
        texture = pg.image.load("./gui_textures/hp_bar.png")
        super().__init__(screen, texture, x, y)
        self.entity = entity
        self.bar = pg.Surface((168, 8))
        self.bar.fill(GREEN)
    
    def draw(self):
        # TODO: Create function and update function
        super().draw()
        self.screen.blit(self.bar, (self.x + 16, self.y + 51))
    
    def update(self):
        width = max(math.floor(168 * (self.entity.get_stat(3) / self.entity.get_stat(2))), 0)
        self.bar = pg.Surface((width, 8))
        if (self.entity.get_stat(3) / self.entity.get_stat(2)) > 0.3:
            self.bar.fill(GREEN)
        elif (self.entity.get_stat(3) / self.entity.get_stat(2)) > 0.15:
            self.bar.fill(YELLOW)
        else:
            self.bar.fill(RED)

class BattleScreen(Gui_base):
    # The screen which show the players and opponents
    def __init__(self, screen, texture, x, y, player, enemies, invent):
        super().__init__(screen, texture, x, y)
        self.player = player
        self.enemies = enemies
        self.player_texture = self.player.get_texture(3)
        self.enemy_textures = [enemy.get_texture(0) for enemy in enemies]
        self.pointer = pg.image.load("./gui_textures/selection.png")
        self.selected = 0
        self.actions = [self.player.attack, invent.open]
        self.player_bar = HpBar(self.screen, 60, 125, self.player)
        self.enemy_bars = [HpBar(self.screen, 600, 170 + 67 * index, enemy) for index, enemy in enumerate(self.enemies)]

    def draw(self):
        super().draw()
        self.screen.blit(self.player_texture, (135, 270))
        for index, enemy_text in enumerate(self.enemy_textures):
            self.screen.blit(enemy_text, (640 + index * 50, 55 + index * 17))
        self.screen.blit(self.pointer, (640, 443 + self.selected * 40))
        self.player_bar.draw()
        for bar in self.enemy_bars:
            bar.draw()

    def open(self):
        is_open = True
        while is_open:
            for bar in self.enemy_bars:
                bar.update()
            self.player_bar.update()
            self.draw()
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_TAB:
                        is_open = False
                    elif event.key == pg.K_w:
                        self.selected = max(0, self.selected - 1)
                    elif event.key == pg.K_s:
                        self.selected = min(2, self.selected + 1)
                    elif event.key == pg.K_e:
                        if self.selected == 0:
                            if len(self.enemies):
                                self.player.attack(self.enemies[0])
