import pygame as pg
from settings import *

def start_battle_anim1(game, screen):
    vert_bar = pg.Surface((40, 600))
    dec_bars = pg.Surface((840, 600), flags=pg.SRCALPHA)
    asc_bars = pg.Surface((840, 600), flags=pg.SRCALPHA)
    for i in range(11):
        dec_bars.blit(vert_bar, (i * 80, 0))
    for i in range(10):
        asc_bars.blit(vert_bar, (40 + i * 80, 0))
    y_offset = 0
    speed = 1000
    while y_offset < 600:
        game.draw_alt()
        y_offset = y_offset + speed * game.dt
        screen.blit(dec_bars, (0, -600 + y_offset))
        screen.blit(asc_bars, (0, 600 - y_offset))
        pg.display.flip()
        game.clock.tick()
    while y_offset > 0:
        y_offset = y_offset - speed * game.dt
        screen.fill(BLACK)
        pg.display.flip()
        game.clock.tick()