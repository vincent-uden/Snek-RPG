import pygame as pg
import sys
from os import path
# Other files from project
from settings import *
from sprites import *
from tilemap import *
from gui import *
from items import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
    
    def load_data(self):
        # Getting important directories
        game_folder = path.dirname(__file__)
        char_folder = path.join(game_folder, "characters")
        map_folder  = path.join(game_folder, "maps")
        gui_folder  = path.join(game_folder, "gui_textures")
        # Loading Textures
        self.map = TileMap(path.join(map_folder, "testmap2.tmx"))
        self.map_img  = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_imgs = [pg.image.load(path.join(char_folder, filename)) for filename in PLAYER_IMGS]
        self.npc1_img = pg.image.load(path.join(char_folder, "npc1.png"))

    def new(self):
        game_folder = path.dirname(__file__)
        gui_folder  = path.join(game_folder, "gui_textures")
        # Initializing sprite groups + sprites and texts
        self.fps_counter = Screen_text(str(self.clock.get_fps()), self.screen)
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        # Reading map data
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == "player":
                self.player = Player(self, tile_object.x, tile_object.y)
            elif tile_object.name == "wall":
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            elif tile_object.name == "npc1":
                Npc(self, tile_object.x, tile_object.y, self.npc1_img)
                print(tile_object.x, tile_object.y)
        if GRID_ON:
           self.grid = Grid(self, 0, 0, pg.image.load("grid.png"))
        # Creating viewport
        self.camera = Camera(self.map.width, self.map.height)
        self.inven_menu = InventoryMenu(self.screen, pg.image.load(path.join(gui_folder, "inventory_menu.png")), 10, 10, self.player)
        self.stats_menu = StatsMenu(self.screen, pg.image.load(path.join(gui_folder, "stats_menu.png")), 10, 10, self.player)
        self.pause_menu = PauseMenu(self.screen, pg.image.load(path.join(gui_folder, "pause_menu.png")), 580, 10, [self.inven_menu.open, self.stats_menu.open])
        self.items = create_items(self.player)
        for x in range(2):
            self.player.inventory.append(self.items[0])
        self.player.inventory.append(self.items[1])
    
    def run(self):
        # Mainloop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
    
    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # Updating everything
        self.all_sprites.update()
        self.camera.update(self.player)
        self.fps_counter.update(str(self.clock.get_fps()))

    def draw(self):
        # Draws everything during gameplay (not while in GUI menus)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        self.fps_counter.draw((5,5))
        pg.display.flip()

    def events(self):
        # Event loop for keys thats not player movement
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                elif event.key == pg.K_p or event.key == pg.K_TAB:
                    self.pause()
    
    def pause(self):
        # Pausing
        paused = True
        while paused:
            # Event loop which overrides all other controls
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_p or event.key == pg.K_TAB:
                        paused = False
                    elif event.key == pg.K_s:
                        self.pause_menu.move_pointer(1)
                    elif event.key == pg.K_w:
                        self.pause_menu.move_pointer(-1)
            self.pause_menu.draw()
            pg.display.flip()
            self.clock.tick()
    
    def show_start_screen(self):
        pass
    
    def show_go_screen(self):
        pass

class Screen_text(object):
    
    def __init__(self, text, screen):
        self.font = pg.font.SysFont("Verdana", 11, True, False)
        self.screen_text = self.font.render(text, True, BLACK)
        self.screen = screen

    def draw(self, pos):
        self.screen.blit(self.screen_text, pos)

    def update(self, new_text):
        self.screen_text = self.font.render(new_text, True, BLACK)


# Initializing game
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()