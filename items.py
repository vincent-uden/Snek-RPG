import pygame as pg
from attacks import *

# Abstract class
class Item:
    def __init__(self, name, value, consumeable, texture):
        self.name  = name
        self.value = value
        self.consumeable = consumeable
        self.texture = texture

class Food(Item):
    def __init__(self, name, value, player, healing, texture):
        super().__init__(name, value, True, texture)
        self.player = player
        self.healing = healing
    
    def use(self):
        self.player.stats["current_hp"] += self.healing

class Weapons(Item):
    def __init__(self, name, value, player, str_bonus, acc_bonus, moveset, texture):
        super().__init__(name, value, True, texture)
        self.player = player
        self.str_bonus = str_bonus
        self.acc_bonus = acc_bonus
        self.moveset = moveset
    
    def __str__(self):
        return f"{self.name} Strength bonus {self.str_bonus} Accuracy bonus {self.acc_bonus}"
    
    def use(self):
        self.player.equip_weapon(self)
    
    def get_moveset(self):
        return self.moveset
    
    def get_move(self, index):
        return self.moveset[index]

class Misc(Item):
    def __init__(self, name, value, texture):
        super().__init__(name, value, False, texture)

def create_items(player):
    items = []
    items.append(Weapons("Iron sword", 15, player, 200, 100, [stab, slash, lunge], pg.image.load("./items/iron_sword.png")))
    items.append(Food("Bad Potato", 1, player, -1, pg.image.load("./items/bad_potato.png")))
    items.append(Food("Potato", 1, player, 1, pg.image.load("./items/potato.png")))
    items.append(Misc("Pebble", 0, pg.Surface((80, 80))))
    items.append(Weapons("Wooden Sword", 10, player, 1, 1, [], pg.image.load("./items/wood_sword.png")))

    return items
