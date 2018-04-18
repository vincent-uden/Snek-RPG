from gui import ContainerMenu
from copy import copy

class Container:
    def __init__(self, size, items, screen, player):
        self.size = size
        self.items = items[:self.size]
        self.player = player
        self.interface = ContainerMenu(screen, self)
    
    def interact(self):
        self.interface.open(self.player)

    def take(self, item):
        print("kek")
        print(item.get_flavor_text())
        self.player.inventory.append(copy(item))
        self.items.remove(item)
