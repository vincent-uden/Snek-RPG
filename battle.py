import pygame as pg
from os import path

class Battle:
    def __init__(self, player, enemies):
        self.player = player
        self.enemies = enemies
        self.turn = 0


    def start(self):
        done = False
        if player.get_stats[3] <= 0
            done = True
        for enemy in enemies:
            if enemy.get_stats[3] <= 0:
                done = True

        while not done:
            # gör en attack funktion hos både enemy och player objekten så att vi
            # kan på ett snyggt sätt göra det random vem som attackerar först
            # fråga mig på discord om du inte fattar
