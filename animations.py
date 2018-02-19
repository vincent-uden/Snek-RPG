import pygame as pg
import sys
from settings import *

def start_battle_anim1(game, screen, battle):
    # First animation for starting battles
    vert_bar = pg.Surface((40, 600))
    dec_bars = pg.Surface((840, 600), flags=pg.SRCALPHA)
    asc_bars = pg.Surface((840, 600), flags=pg.SRCALPHA)
    for i in range(11):
        dec_bars.blit(vert_bar, (i * 80, 0))
    for i in range(10):
        asc_bars.blit(vert_bar, (40 + i * 80, 0))
    y_offset = 0
    speed = 2000
    while y_offset < 600:
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
        game.draw_alt()
        y_offset = y_offset + speed * game.dt
        screen.blit(dec_bars, (0, -600 + y_offset))
        screen.blit(asc_bars, (0, 600 - y_offset))
        pg.display.flip()
        game.clock.tick(FPS)
    while y_offset < 1200:
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
        battle.draw()
        y_offset = y_offset + speed * game.dt
        screen.blit(dec_bars, (0, -600 + y_offset))
        screen.blit(asc_bars, (0, 600 - y_offset))
        pg.display.flip()
        game.clock.tick(FPS)

def cell_transition(game, screen):
    fader = pg.Surface((WIDTH, HEIGHT), flags=pg.SRCALPHA)
    curr_fade = (0,0,0,0)
    for i in range(255):
        game.draw_alt()
        curr_fade = (curr_fade[0], curr_fade[1], curr_fade[2], i)
        fader.fill(curr_fade)
        screen.blit(fader, (0,0))
        pg.display.flip()
        game.clock.tick(FPS)