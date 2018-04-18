import pygame as pg

class DropTable:
    def __init__(self, items):
        self.items = items

    def __str__(self):
        return f"DropTable:\nItems: {self.items}"


class StaticDropTable(DropTable):
    def __init__(self, items):
        super().__init__(items)

    def get_items(self):
        return self.items[::]

def create_drop_tables(items):
    tables = {}
    tables["static_test_table_1"] = StaticDropTable([items[0], items[5], items[5]])
    return tables

