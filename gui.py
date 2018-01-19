import pygame as pg
import sys
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
    def __init__(self, screen, texture, x, y, actions):
        super().__init__(screen, texture, x, y)
        self.pointer = pg.image.load("./gui_textures/selection.png")
        self.selected = 0
        self.actions = actions
    
    def move_pointer(self, direction):
        self.selected += direction
        if self.selected < 0:
            self.selected = 0
        if self.selected >= len(self.actions):
            self.selected = len(self.actions) - 1
    
    def draw(self):
        super().draw()
        self.screen.blit(self.pointer, (self.x + 30, self.y + 62 + self.selected * 40))
        self.execute()
    
    def execute(self):
        self.actions[self.selected]()

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

    def draw(self):
        super().draw()
        for index, item in enumerate(self.player.inventory):
            MenuText(f"{item.name}", self.screen).draw(83, 125 + index * 20)
            MenuText(f"{item.value}", self.screen).draw(500, 125 + index * 20)
    
    def open(self):
        self.draw()
        pg.display.flip()