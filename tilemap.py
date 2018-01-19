import pygame as pg
import zipfile
import pytmx
from settings import *

class Map:
    def __init__(self, filename):
        self.collision_data = []
        self.texture_data = []
        with zipfile.ZipFile(filename) as z:
        # Gathering collision data
            with z.open("map.txt", "r") as f:
                for line in f:
                    self.collision_data.append(line.strip().decode("UTF-8"))
        # Gathering Texture Data
            with z.open("tiles.txt", "r") as t:
                for line in t:
                    self.texture_data.append(line.strip().decode("UTF-8").split(" "))
        self.tilewidth = len(self.collision_data[0])
        self.tileheight = len(self.collision_data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0,0, width, height)
        self.width = width
        self.height = height
    
    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.pos.x + int(WIDTH / 2)
        y = -target.pos.y + int(HEIGHT / 2)
        # limit scrolling
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - WIDTH), x)
        y = max(-(self.height - HEIGHT), y)
        self.camera = pg.Rect(x, y, self.width, self.height)

class TileMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm
    
    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface
