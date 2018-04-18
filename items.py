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

class Weapon(Item):
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

def create_items(player):
    items = []
    # Create items
    items.append(Weapon("Iron sword", 15, player, 200, 100, [stab, slash, lunge], pg.image.load("./items/iron_sword.png"), "Just an average sword."))
    items.append(Food("Bad Potato", 1, player, -1, pg.image.load("./items/bad_potato.png"), ["A bad potato, probably ", "not good for your body."]))
    items.append(Food("Potato", 1, player, 1, pg.image.load("./items/potato.png"), "A potato, heals 1 hp."))
    items.append(Misc("Pebble", 0, pg.Surface((80, 80)), ""))
    items.append(Weapon("Wooden Sword", 10, player, 1, 1, [], pg.image.load("./items/wood_sword.png"), "A bad sword."))
    items.append(Food("Health Potion", 100, player, 10, pg.image.load("./items/health_pot.png"), "Heals 10 hp."))
    return items
