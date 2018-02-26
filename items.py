import pygame as pg
from attacks import *

# Abstract class
class Item:
    def __init__(self, name, value, consumeable, texture, flavor_text):
        self.name  = name
        self.value = value
        self.consumeable = consumeable
        self.texture = texture
        self.flavor_text = flavor_text

    def get_flavor_text(self):
        return self.flavor_text

class Food(Item):
    def __init__(self, name, value, player, healing, texture, flavor_text):
        super().__init__(name, value, True, texture, flavor_text)
        self.player = player
        self.healing = healing
    
    def use(self):
        self.player.stats["current_hp"] += self.healing

class Weapons(Item):
    def __init__(self, name, value, player, str_bonus, acc_bonus, moveset, texture, flavor_text):
        super().__init__(name, value, True, texture, flavor_text)
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

    def get_flavor_text(self):
        return [self.flavor_text, f"Strength: {self.str_bonus}", f"Accuracy: {self.acc_bonus}"]

class Misc(Item):
    def __init__(self, name, value, texture, flavor_text):
        super().__init__(name, value, False, texture, flavor_text)