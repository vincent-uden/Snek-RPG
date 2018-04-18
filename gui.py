import pygame as pg
import sys
import math
import random
from settings import *
from items import *

vec = pg.math.Vector2

def f():
    return None

class MenuText:

    def __init__(self, text, screen, size=16, AA=True):
        self.font = pg.font.Font("./resources/PressStart2P.ttf", size)
        if type(text) != type([]):
            self.screen_text = self.font.render(text, AA, BLACK)
        else:
            self.screen_text = [self.font.render(t, False, BLACK) for t in text]
        self.screen = screen
        self.anti_aliasing = AA

    def draw(self, x, y):
        if type(self.screen_text) == type([]):
            for i, t in enumerate(self.screen_text):
                self.screen.blit(t, (x, y + i * 18))
        else:
            self.screen.blit(self.screen_text, (x, y))

    def update(self, new_text):
        self.screen_text = self.font.render(new_text, self.anti_aliasing, BLACK)

class Gui_base:
    def __init__(self, screen, texture, x, y):
        self.screen = screen
        self.image = texture
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

class PauseMenu(Gui_base):
    def __init__(self, screen, texture, x, y, menus, game):
        super().__init__(screen, texture, x, y)
        self.pointer = pg.image.load("./gui_textures/selection.png")
        self.selected = 0
        self.menus = menus
        self.game = game

    def move_pointer(self, direction):
        self.selected += direction
        if self.selected < 0:
            self.selected = 0
        if self.selected >= len(self.menus):
            self.selected = len(self.menus) - 1

    def draw(self):
        self.game.draw_alt()
        super().draw()
        self.screen.blit(self.pointer, (self.x + 30, self.y + 62 + self.selected * 40))
        #self.menus[self.selected].draw()

    def execute(self):
        self.menus[self.selected].open()

class StatsMenu(Gui_base):
    def __init__(self, screen, texture, x, y, player):
        super().__init__(screen, texture, x, y)
        self.player = player
        self.hp_text    = MenuText(f"{self.player.get_stat(3)}/{self.player.get_stat(2)}", screen)
        self.level_text = MenuText(f"{self.player.get_stat(0)}", screen)
        self.xp_text    = MenuText(f"{self.player.get_stat(1)}", screen)
        self.name_text  = MenuText(f"{self.player.get_stat(4)}", screen)

    def draw(self):
        super().draw()
        self.hp_text.update(f"{self.player.get_stat(3)}/{self.player.get_stat(2)}")
        self.level_text.update(f"{self.player.get_stat(0)}")
        self.xp_text.update(f"{self.player.get_stat(1)}")
        self.name_text.update(f"{self.player.get_stat(4)}")
        self.hp_text.draw(445, 92)
        self.level_text.draw(380, 150)
        self.xp_text.draw(92, 150)
        self.name_text.draw(120, 92)

    def open(self):
        is_open = True
        while is_open:
            self.draw()
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_p or event.key == pg.K_TAB:
                        is_open = False

class InventoryMenu(Gui_base):

    def __init__(self, screen, texture, x, y, player):
        super().__init__(screen, texture, x, y)
        self.player = player
        self.pointer = pg.image.load("./gui_textures/selection.png")
        self.selected = 0
        try:
            self.current_f_text = MenuText(self.player.inventory[self.selected].get_flavor_text(), self.screen)
        except IndexError:
            self.current_f_text = MenuText("", self.screen)

    def draw(self):
        super().draw()
        self.current_f_text.draw(self.x + 30, self.y + 480)
        self.stacks = {}
        for item in self.player.inventory:
            if item.name in self.stacks:
                self.stacks[item.name].append(item)
            else:
                self.stacks[item.name] = [item]
        if self.selected > len(self.stacks) - 1:
            self.move_pointer(-1)
        if len(self.player.inventory) > 0:
            for index, name in enumerate(self.stacks.keys()):
                MenuText(f"{name} × {len(self.stacks[name])}", self.screen).draw(self.x + 63, self.y + 105 + index * 20)
                MenuText(f"{self.stacks[name][0].value}", self.screen).draw(self.x + 480, 105 + index * 20)
                if index == self.selected:
                    self.screen.blit(self.stacks[name][0].texture, (self.x + 456, self.y + 476))


    def move_pointer(self, direction):
        self.selected += direction
        if self.selected < 0:
            self.selected = 0
        if self.selected >= len(self.stacks):
            self.selected = len(self.stacks) - 1
        if len(self.player.inventory) == 0:
            self.selected = 0
        if self.player.inventory != []:
            self.current_f_text = MenuText(self.stacks[list(self.stacks.keys())[self.selected]][0].get_flavor_text(), self.screen)
        else:
            self.current_f_text = MenuText("", self.screen)

    def execute(self):
        if len(self.player.inventory) >= 0:
            self.player.inventory[self.selected].use()

    def open(self):
        is_open = True
        pg.key.set_repeat(100, 50)
        while is_open:
            self.draw()
            if len(self.player.inventory) >= 0:
                self.screen.blit(self.pointer, (self.x + 35, self.y + 99 + self.selected * 20))
            pg.display.flip()
            # Event loop which overrides all other controls
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_p or event.key == pg.K_TAB:
                        is_open = False
                    elif event.key == pg.K_s:
                        self.move_pointer(1)
                    elif event.key == pg.K_w:
                        self.move_pointer(-1)
                    elif event.key == pg.K_e or event.key == pg.K_RETURN:
                        self.move_pointer(0)
                        consumed = self.player.use_item(self.selected)
                        #if consumed:
                        #    if self.selected > 0:
                        #        self.selected -= 1
        pg.key.set_repeat()

class ShowEq:
    def __init__(self, player):
        self.player = player

    def open(self):
        for item in self.player.equipped:
            print(item)

    def draw(self):
        return None

class HpBar(Gui_base):
    def __init__(self, screen, x, y, entity):
        texture = pg.image.load("./gui_textures/hp_bar.png")
        super().__init__(screen, texture, x, y)
        self.entity = entity
        self.name_text = MenuText(self.entity.get_stat(4).upper(), self.screen, size=16, AA=False)
        self.hp_text = MenuText(f"HP:{self.entity.get_stat(3)}/{self.entity.get_stat(2)}", self.screen, size=16, AA=False)
        self.bar = pg.Surface((275, 8))
        self.bar.fill(GREEN)
    
    def draw(self):
        # TODO: Create function and update function
        super().draw()
        self.screen.blit(self.bar, (self.x + 13, self.y + 53))
        self.name_text.draw(self.x + 12, self.y + 20)
        self.hp_text.draw(self.x + 160, self.y + 20)
    
    def update(self):
        width = max(math.floor(275 * (self.entity.get_stat(3) / self.entity.get_stat(2))), 0)
        self.bar = pg.Surface((width, 8))
        if (self.entity.get_stat(3) / self.entity.get_stat(2)) > 0.3:
            self.bar.fill(GREEN)
        elif (self.entity.get_stat(3) / self.entity.get_stat(2)) > 0.15:
            self.bar.fill(YELLOW)
        else:
            self.bar.fill(RED)
        self.hp_text.update(f"HP:{self.entity.get_stat(3)}/{self.entity.get_stat(2)}")

class BattleScreen(Gui_base):
    # The screen which show the players and opponents
    def __init__(self, screen, texture, x, y, player, enemies, invent):
        super().__init__(screen, texture, x, y)
        self.player = player
        self.enemies = enemies
        # Textures
        self.player_texture = self.player.get_texture(3)
        self.enemy_textures = [enemy.get_texture(0) for enemy in enemies]
        self.pointer = pg.image.load("./gui_textures/selection.png")
        self.vert_pointer = pg.image.load("./gui_textures/vert_selection.png")

        self.selected = 0
        self.actions = [self.player.attack, invent.open]
        self.player_bar = HpBar(self.screen, 60, 125, self.player)
        self.enemy_bars = [HpBar(self.screen, 500, 170 + 67 * index, enemy) for index, enemy in enumerate(self.enemies)]
        self.battle_invent = BattleInventory(self.screen, pg.image.load("./gui_textures/battle_inventory.png"), 0, 0, self.player)
        self.base_choices = [MenuText("Attack", self.screen), MenuText("Inventory", self.screen), MenuText("Run away", self.screen)]
        self.animating = False
        self.animated_enemy = None
        self.alive_enemies = [enemy.alive for enemy in self.enemies]
        # Optimizing drawing
        self.base_surface = pg.Surface((WIDTH, HEIGHT))
        self.base_surface.blit(self.image, (0, 0))
        self.base_surface.blit(self.player_bar.image, (self.player_bar.x, self.player_bar.y))
        self.base_surface.blit(self.player_bar.name_text.screen_text, (self.player_bar.x + 12, self.player_bar.y + 20))
        for bar in self.enemy_bars:
            self.base_surface.blit(bar.image, (bar.x, bar.y))
            self.base_surface.blit(bar.name_text.screen_text, (bar.x + 12, bar.y + 20))
        # Instructions
        self.instructions = [MenuText("Choose an action", self.screen, size=24, AA=False),
                             MenuText("Choose an attack", self.screen, size=24, AA=False),
                             MenuText("Choose an enemy", self.screen, size=24, AA=False)]

    def play_player_anim(self):
        self.animating = True
        pos = (135, 270)
        offset = (0, 0)
        while offset != (60, -30):
            offset = (offset[0] + 10, offset[1] - 5)
            self.draw()
            self.screen.blit(self.player_texture, (pos[0] + offset[0], pos[1] + offset[1]))
            pg.display.flip()
            self.player.game.clock.tick(FPS)
        while offset != (0, 0):
            offset = (offset[0] - 10, offset[1] + 5)
            self.draw()
            self.screen.blit(self.player_texture, (pos[0] + offset[0], pos[1] + offset[1]))
            pg.display.flip()
            self.player.game.clock.tick(FPS)
        self.animating = False
    
    def play_enemy_anim(self, enemy_id):
        self.animated_enemy = enemy_id
        two_positions = [(650, 65), (730, 87)]
        three_positions = [(650, 45), (690, 67), (730, 87)]
        if len(self.enemies) == 1:
            pos = (690, 67)
        if len(self.enemies) == 2:
            pos = two_positions[enemy_id]
        if len(self.enemies) == 3:
            pos = three_positions[enemy_id]
        offset = (0, 0)
        while offset != (-60, 30):
            offset = (offset[0] - 10, offset[1] + 5)
            self.draw()
            self.screen.blit(self.enemy_textures[enemy_id], (pos[0] + offset[0], pos[1] + offset[1]))
            pg.display.flip()
            self.player.game.clock.tick(FPS)
        while offset != (0, 0):
            offset = (offset[0] + 10, offset[1] - 5)
            self.draw()
            self.screen.blit(self.enemy_textures[enemy_id], (pos[0] + offset[0], pos[1] + offset[1]))
            pg.display.flip()
            self.player.game.clock.tick(FPS)
        self.animated_enemy = None
        

    def draw(self):
        self.screen.blit(self.base_surface, (self.x, self.y))
        #super().draw()
        if not self.animating:
            self.screen.blit(self.player_texture, (135, 270))
        if len(self.enemies) == 1:
            if self.animated_enemy != 0:
                self.screen.blit(self.enemy_textures[0], (690, 67))
        elif len(self.enemies) == 2:
            if self.animated_enemy != 0 and self.alive_enemies[0]:
                self.screen.blit(self.enemy_textures[0], (650, 65))
            if self.animated_enemy != 1 and self.alive_enemies[1]:
                self.screen.blit(self.enemy_textures[1], (730, 87))
        elif len(self.enemies) == 3:
            if self.animated_enemy != 0 and self.alive_enemies[0]:
                self.screen.blit(self.enemy_textures[0], (650, 45))
            if self.animated_enemy != 1 and self.alive_enemies[1]:
                self.screen.blit(self.enemy_textures[1], (690, 67))
            if self.animated_enemy != 2 and self.alive_enemies[2]:
                self.screen.blit(self.enemy_textures[2], (730, 87))
        #for index, enemy_text in enumerate(self.enemy_textures):
        #    self.screen.blit(enemy_text, (640 + index * 50, 55 + index * 17))
        #self.player_bar.draw()
        #for bar in self.enemy_bars:
        #    bar.draw()
        self.screen.blit(self.player_bar.hp_text.screen_text, (self.player_bar.x + 160, self.player_bar.y + 20))
        self.screen.blit(self.player_bar.bar, (self.player_bar.x + 13, self.player_bar.y + 53))
        for bar in self.enemy_bars:
            self.screen.blit(bar.hp_text.screen_text, (bar.x + 160, bar.y + 20))
            self.screen.blit(bar.bar, (bar.x + 13, bar.y + 53))

    def update_attacks(self):
        if self.player.get_weapon != None:
            self.base_choices = [MenuText(move.name, self.screen) for move in self.player.get_weapon().get_moveset()]
        else:
            self.base_choices = [MenuText("Attack", self.screen), MenuText("", self.screen), MenuText("Run away", self.screen)]

    def select_enemy(self, selected_enemy):
        selecting = True
        if not self.alive_enemies[selected_enemy]:
            availible_enemies = [i for i,x in enumerate(self.alive_enemies) if x]
            selected_enemy = availible_enemies[0]
        while selecting:
            self.draw()
            self.instructions[2].draw(100, 484)
            if len(self.enemies) == 3:
                self.screen.blit(self.vert_pointer, (660 + selected_enemy * 41, 20 + selected_enemy * 20))
            else:
                self.screen.blit(self.vert_pointer, (661 + selected_enemy * 80, 35 + selected_enemy * 22))
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_TAB:
                        selecting = False
                    elif event.key == pg.K_a:
                        selected_enemy = max(0, selected_enemy - 1)
                        if not self.enemies[selected_enemy].alive:
                            selected_enemy -= 1
                            if not self.enemies[selected_enemy].alive or selected_enemy == -1:
                                selected_enemy += 2
                    elif event.key == pg.K_d:
                        selected_enemy = min(len(self.enemies) - 1, selected_enemy + 1)
                        if not self.enemies[selected_enemy].alive:
                            selected_enemy += 1
                            try:
                                if not self.enemies[selected_enemy].alive:
                                    selected_enemy -= 2
                            except:
                                selected_enemy -= 2
                    elif event.key == pg.K_e:
                        return selected_enemy
    
    def select_attack(self):
        selecting = True
        selected_attack = 0
        attack_texts = [MenuText(attack.name, self.screen) for attack in self.player.get_moveset()]
        while selecting:
            # Draw interface
            self.draw()
            self.instructions[1].draw(100, 484)
            for index, attack in enumerate(attack_texts):
                attack.draw(668, 447 + index * 40)
            self.screen.blit(self.pointer, (640, 443 + selected_attack * 40))
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_TAB:
                        selecting = False
                    elif event.key == pg.K_w:
                        selected_attack = max(0, selected_attack - 1)
                    elif event.key == pg.K_s:
                        selected_attack = min(2, selected_attack + 1)
                    elif event.key == pg.K_e:
                        return selected_attack

    def draw_base_options(self):
        self.instructions[0].draw(100, 484)
        for index, text in enumerate(self.base_choices):
            text.draw(668, 447 + index * 40)

    def open(self):
        is_open = True
        selected_enemy = 0
        while is_open:
            self.alive_enemies = [enemy.alive for enemy in self.enemies]
            for bar in self.enemy_bars:
                bar.update()
            self.player_bar.update()
            self.draw()
            self.screen.blit(self.pointer, (640, 443 + self.selected * 40))
            self.draw_base_options()
            pg.display.flip()
            self.player.game.clock.tick()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_TAB:
                        is_open = False
                    elif event.key == pg.K_w:
                        self.selected = max(0, self.selected - 1)
                    elif event.key == pg.K_s:
                        self.selected = min(2, self.selected + 1)
                    elif event.key == pg.K_e:
                        if self.selected == 0:
                            selected_attack = self.select_attack()
                            if selected_attack is None:
                                continue
                            if len(self.enemies) == 1:
                                self.player.attack(self.enemies[0], selected_attack)
                                if self.enemies[0].stats["current_hp"] <= 0:
                                    self.enemies[0].alive = False
                            else:
                                selected_enemy = self.select_enemy(selected_enemy)
                                if selected_enemy is not None:
                                    self.player.attack(self.enemies[selected_enemy], selected_attack)
                                    if self.enemies[selected_enemy].stats["current_hp"] <= 0:
                                        self.enemies[selected_enemy].alive = False
                                else:
                                    continue
                            self.play_player_anim()
                            self.alive_enemies = [enemy.alive for enemy in self.enemies]
                            for bar in self.enemy_bars:
                                bar.update()
                            self.player_bar.update()
                            self.draw()
                            pg.display.flip()
                            for i in range(30):
                                self.draw()
                            self.end_turn()
                            continue
                        elif self.selected == 1:
                            only_action = self.battle_invent.open()
                            if only_action:
                                self.end_turn()
    
    def end_turn(self):
        for index, enemy in enumerate(self.enemies):
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            if not enemy.alive:
                continue
            enemy.attack(self.player)
            self.play_enemy_anim(index)
            for bar in self.enemy_bars:
                bar.update()
            self.player_bar.update()
            self.draw()
            pg.display.flip()
            for i in range(30):
                self.draw()

class BattleInventory(InventoryMenu):
    def __init__(self, screen, texture, x, y, player):
        super().__init__(screen, texture, x, y, player)
    
    def open(self):
        is_open = True
        pg.key.set_repeat(100, 50)
        while is_open:
            self.draw()
            if len(self.player.inventory) >= 0:
                self.screen.blit(self.pointer, (self.x + 35, self.y + 99 + self.selected * 20))
            pg.display.flip()
            # Event loop which overrides all other controls
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_p or event.key == pg.K_TAB:
                        is_open = False
                    elif event.key == pg.K_s:
                        self.move_pointer(1)
                    elif event.key == pg.K_w:
                        self.move_pointer(-1)
                    elif event.key == pg.K_e or event.key == pg.K_RETURN:
                        if isinstance(self.player.inventory[self.selected], Food):
                            only_action = True
                        else:
                            only_action = False
                        consumed = self.player.use_item(self.selected)
                        if consumed:
                            if self.selected > 0:
                                self.selected -= 1
                        if only_action:
                            return True

    def draw(self):
        Gui_base.draw(self)
        self.screen.blit(self.player.inventory[self.selected].texture, (self.x + 456, self.y + 494))
        self.current_f_text.draw(self.x + 30, self.y + 502)
        for index, item in enumerate(self.player.inventory):
            MenuText(f"{item.name}", self.screen).draw(self.x + 63, self.y + 105 + index * 20)
            MenuText(f"{item.value}", self.screen).draw(self.x + 480, 105 + index * 20)

class ContainerMenu(Gui_base):
    def __init__(self, screen, container):
        super().__init__(screen, pg.image.load("./gui_textures/container_menu.png"), WIDTH / 2 - 280, HEIGHT / 2 - 290)
        self.container = container
        self.pointer = pg.image.load("./gui_textures/selection.png")
        self.selected = 0
        try:
            self.current_f_text = MenuText(self.container.items[self.selected].get_flavor_text(), self.screen)
        except IndexError:
            self.current_f_text = MenuText("", self.screen)
        self.current_item_list = self.container.items

    def draw(self):
        super().draw()
        self.current_f_text.draw(self.x + 30, self.y + 480)
        self.stacks = {}
        for item in self.current_item_list:
            if item.name in self.stacks:
                self.stacks[item.name].append(item)
            else:
                self.stacks[item.name] = [item]
        if self.selected > len(self.stacks) - 1:
            self.move_pointer(-1)
        for index, name in enumerate(self.stacks.keys()):
            MenuText(f"{name} × {len(self.stacks[name])}", self.screen).draw(self.x + 63, self.y + 105 + index * 20)
            MenuText(f"{self.stacks[name][0].value}", self.screen).draw(self.x + 480, 105 + index * 20)
            if index == self.selected:
                self.screen.blit(self.stacks[name][0].texture, (self.x + 456, self.y + 476))

    def move_pointer(self, direction):
        self.selected += direction
        if self.selected < 0:
            self.selected = 0
        if self.selected >= len(self.stacks):
            self.selected = len(self.stacks) - 1
        if len(self.current_item_list) == 0:
            self.selected = 0
        self.current_f_text = MenuText(self.stacks[list(self.stacks.keys())[self.selected]][0].get_flavor_text(), self.screen)

    def open(self, player):
        is_open = True
        while is_open:
            self.draw()
            if len(self.current_item_list) >= 0:
                self.screen.blit(self.pointer, (self.x + 35, self.y + 99 + self.selected * 20))
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_TAB:
                        is_open = False
                        print("closed")
                    elif event.key == pg.K_w:
                        print("w")
                        self.move_pointer(-1)
                    elif event.key == pg.K_s:
                        self.move_pointer(1)
                    elif event.key == pg.K_e:
                        item = self.stacks[list(self.stacks.keys())[self.selected]][0]
                        self.current_item_list.remove(item)
                        player.inventory.append(item)
                        print(item)
                        print(player.inventory)
