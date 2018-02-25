class Container:
    def __init__(self, size, items, interface):
        self.size = size
        self.items = items[:self.size]
        self.interface = interface
    
    def interact(self):
        self.interface.open()
        #TODO: Fix