# Abstract class
class Item:
    def __init__(self, name, value, useable, consumeable):
        self.name  = name
        self.value = value
        self.useable = useable
        self.consumeable = consumeable

class Food(Item):
    def __init__(self, name, value, useable, player, healing):
        super().__init__(name, value, useable, True)
        self.player = player
        self.healing = healing
    
    def use(self):
        self.player.stats["current_hp"] += self.healing

class Misc(Item):
    def __init__(self, name, value, useable):
        super().__init__(name, value, False, False)

def create_items(player):
    items = []
    items.append(Food("Bad Potato", 1, True, player, -1))
    items.append(Food("Potato", 1, True, player, 1))
    items.append(Misc("Pebble", 0, False))
    return items





# TODO: Fix items and inventory