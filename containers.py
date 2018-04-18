class Container:
    def __init__(self, size, items, interface, player):
        self.size = size
        self.items = items[:self.size]
        self.interface = interface
        self.player = player
    
    def interact(self):
        for item in self.items:
            self.player.inventory.append(item)
        #self.interface.open()
        #TODO: Fix
