# Abstract class
class Item:
    def __init__(self, name, value, consumeable):
        self.name  = name
        self.value = value
        self.consumeable = consumeable

class Food(Item):
    def __init__(self, name, value, player, healing):
        super().__init__(name, value, True)
        self.player = player
        self.healing = healing
    
    def use(self):
        self.player.stats["current_hp"] += self.healing

class Weapons(Item):
    def __init__(self, name, value, player, str_bonus, acc_bonus):
        super().__init__(name, value, True)
        self.player = player
        self.str_bonus = str_bonus
        self.acc_bonus = acc_bonus
    
    def __str__(self):
        return f"{self.name} Strength bonus {self.str_bonus} Accuracy bonus {self.acc_bonus}"
    
    def use(self):
        self.player.equip_weapon(self)

class Misc(Item):
    def __init__(self, name, value):
        super().__init__(name, value, False)

def create_items(player):
    items = []
    items.append(Food("Bad Potato", 1, player, -1))
    items.append(Food("Potato", 1, player, 1))
    items.append(Misc("Pebble", 0))
    items.append(Weapons("Wooden Sword", 10, player, 1, 1))
    items.append(Weapons("Iron sword", 15, player, 2, 2))
    return items
