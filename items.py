class Item:
    def __init__(self, name, value):
        self.name  = name
        self.value = value

class Food(Item):
    def __init__(self, name, value, player, healing):
        super().__init__(name, value)
        self.player = player
        self.healing = healing
    
    def use(self):
        self.player.stats["current_hp"] += self.healing


def create_items(player):
    items = []
    items.append(Food("Bad Potato", 1, player, -1))
    items.append(Food("Potato", 1, player, 1))
    return items





# TODO: Fix items and inventory