import time
from functools import wraps

import arcade
import arcade.gui
import json

import pygame

from rpg.BattleEnemy import BattleEnemy
from rpg.BattleAlly import BattleAlly
from rpg.BattleBuddy import *
from rpg.sprites.character_sprite import CharacterSprite, SPRITE_INFO, Anim
from rpg.sprites.player_sprite import PlayerSprite
from rpg.Effect import Effect
from rpg.EnemyIA import EnemyIA
from rpg.Action import Action
from rpg.constants import (CHARACTER_SPRITE_SIZE, SCREEN_WIDTH, ally_x_positions, ally_y_positions,
                           CHARACTER_POINTER_SPEED, enemy_x_positions, enemy_y_positions)

# Para probar
from rpg.views.game_view import GameView

class InBattleView(arcade.View):
    def __init__(self):
        super().__init__()
        self.option = "menu"
        self.previous_option = ""
        self.clicked_button_name = ""

        self.player_sprites = arcade.SpriteList()
        self.enemy_sprites = arcade.SpriteList()

        self.manager = arcade.gui.UIManager()
        self.activated = False
        self.contenedor = arcade.gui.UIBoxLayout()

        self.player_team = []
        self.player_team_length = 0
        self.team_names = []

        with open("../resources/data/battleCharacters_dictionary.json", "r") as file:
            self.team = json.load(file)

        with open("../resources/data/actions_dictionary.json", "r") as file:
            self.actions = json.load(file)

        with open("../resources/data/worldItem_dictionary.json", "r") as file:
            self.items = json.load(file)

        self.enemy_collision_list = []
        self.enemy_team = []

        with open("../resources/data/battleCharacters_dictionary.json", "r") as file:
            self.enemies = json.load(file)

        with open("../resources/data/effects_dictionary.json", "r") as file:
            self.effects = json.load(file)

        self.current_ally = 0
        self.current_ally_index = 0

        self.allow_inputs = True
        self.player_turn = True

        self.action_buttons = []

        self.description_widget = None
        self.description_is_displayed = False

        self.stage = 1

        self.current_width = self.get_width()
        self.width_scaling_factor = self.current_width / 1280

        self.current_height = self.get_height()
        self.height_scaling_factor = self.current_height / 720

        self.x_positions = ally_x_positions.copy()
        self.y_positions = ally_y_positions.copy()

        self.enemy_x_positions = enemy_x_positions.copy()
        self.enemy_y_positions = enemy_y_positions.copy()

        for i in range(len(self.x_positions)):
            self.x_positions[i] *= self.width_scaling_factor

        self.pointer_height_offset = 30
        self.pointer_x = self.x_positions[self.current_ally]
        self.pointer_y = self.y_positions[self.current_ally] + self.pointer_height_offset

        self.pointer_is_up = False

        self.inventory = self.window.views["game"].player_sprite.inventory

        self.current_selected_enemy = 0
        self.turn_ended = False

        print("Inventario cargado:", self.inventory)

        self.ally_effects_list = []
        self.enemy_effects_list = []

        self.enemy_AI = None

        self.defeated_enemies = []
        self.remaining_enemies = []

        self.defeated_allies = []
        self.remaining_allies = []
        self.ally_rotation = []

        self.round = 1
        self.r_done = False

        self.player_attacks = 1

        self.ally_health_bars = []
        self.ally_sta_bars = []

        self.enemy_health_bars = []
        self.enemy_sta_bars = []

        self.bar_width = 0

        self.initial_player_team_indexes = []
        self.initial_enemy_team_indexes = []

        self.elapsed_time = 0
        self.enemy_elapsed_time = 0
        self.interval = 0.3
        self.enemy_interval = 0.3

        self.attack_time = 0
        self.attack_duration = 1
        self.skill_duration = 1

        self.waiting_for_action = False

        self.time = 0

        self.dead_allies = []
        self.initial_team = []

        self.hurt = False

        self.enemy_attacking = None
        self.enemy_waiting_for_action = False
        self.enemy_action_performed = None
        self.enemy_turn_index = 0
        self.enemy_attack_time = 0
        self.ally_hurt_time = 0

        self.attack_anim_done = False
        self.hurt_anim_done = False

        self.item_used = None

        # Sprites de información sobre los controles
        self.sprites_controles = arcade.SpriteList()

        self.key_height_sub = 595

        self.flechaD = arcade.Sprite("../resources/UIThings/flechaD.png", scale=1.5)
        self.flechaD.center_x = self.current_width - 250
        self.flechaD.center_y = self.current_height - self.key_height_sub
        self.sprites_controles.append(self.flechaD)

        self.flechaI = arcade.Sprite("../resources/UIThings/flechaI.png", scale=1.5)
        self.flechaI.center_x = self.current_width - 280
        self.flechaI.center_y = self.current_height - self.key_height_sub
        self.sprites_controles.append(self.flechaI)

        x_enter = self.current_width - 268
        y_enter = self.current_height - self.key_height_sub - 40

        self.teclaEnter1 = arcade.Sprite("../resources/UIThings/teclaEnter1.png", scale=1.5)
        self.teclaEnter1.center_x = x_enter
        self.teclaEnter1.center_y = y_enter
        self.sprites_controles.append(self.teclaEnter1)

        self.teclaEnter2 = arcade.Sprite("../resources/UIThings/teclaEnter2.png", scale=1.5)
        self.teclaEnter2.center_x = x_enter + 16
        self.teclaEnter2.center_y = y_enter
        self.sprites_controles.append(self.teclaEnter2)

        self.teclaEsc = arcade.Sprite("../resources/UIThings/teclaEsc.png", scale=1.5)
        self.teclaEsc.center_x = self.current_width - 252
        self.teclaEsc.center_y = self.current_height - self.key_height_sub - 80
        self.sprites_controles.append(self.teclaEsc)

        self.key_controls_options = ["attack", "skill", "select_enemy"]

        self.inventory_empty = False

        self.sta_message = False

        cyberpunk_maps_list = ["mapa_cyberpunk", "power_plant_interior", "submapa_alcantarillado",
                                    "time_company_interior"]

        if self.window.views["game"].cur_map_name in cyberpunk_maps_list:
            self.fondo = arcade.Sprite("../resources/UIThings/fondoCyber.png", scale=1.2)

            self.fondo.center_x = self.current_width / 2
            self.fondo.center_y = self.current_height / 2 + 400
        else:
            self.fondo = arcade.Sprite("../resources/UIThings/fondo.png", scale=1.5)

            self.fondo.center_x = self.current_width / 2
            self.fondo.center_y = self.current_height / 2

        self.att_sta_message = False

        self.target_ally_selected = False

        self.enemy_chosen_action = None
        self.enemy_chosen_target = None



    def on_show_view(self):
        musicaBatalla = self.window.views['game'].my_map.battleMusicName
        pygame.mixer.music.load(f"../resources/sounds/{musicaBatalla}")
        pygame.mixer.music.play(-1)  # bucle infinito


        self.activated = True
        self.option = "menu"
        self.previous_option = ""
        self.clicked_button_name = ""
        self.player_turn = True

        self.player_sprites = arcade.SpriteList()
        self.enemy_sprites = arcade.SpriteList()

        self.enemy_team.clear()
        self.player_team.clear()
        self.remaining_enemies.clear()
        self.remaining_allies.clear()
        self.defeated_enemies.clear()
        self.defeated_allies.clear()
        self.ally_rotation.clear()
        self.ally_effects_list.clear()
        self.enemy_effects_list.clear()
        self.action_buttons.clear()

        self.player_attacks = 1
        self.stage = 1
        self.round = 1
        self.r_done = False
        self.waiting_for_action = False
        self.allow_inputs = True
        self.clicked_button_name = ""
        self.hurt = False
        self.current_selected_enemy = 0
        self.current_ally = 0

        self.inventory = self.window.views["game"].player_sprite.inventory

        self.manager.enable()
        self.main_buttons()

        # Load allies

        new_ally_x = ally_x_positions.copy()
        new_ally_y = ally_y_positions.copy()

        self.player_team = self.window.views["game"].player_sprite.player_team
        self.initial_team = self.player_team.copy()

        self.player_team_length = len(self.player_team)
        print(f"Player team length: {self.player_team_length}")

        for character in self.player_team:
            while len(new_ally_x) > 0:
                self.setup_team(character, new_ally_x[0], new_ally_y[0])
                del new_ally_x[0]
                del new_ally_y[0]
                break

        # Load enemies

        new_enemy_x = enemy_x_positions.copy()
        new_enemy_y = enemy_y_positions.copy()

        for enemy in self.enemy_collision_list:
            enemy_actions = []
            for action in self.team[enemy]['actions']:

                action_object = Action(self.actions[action]["name"],
                                       self.actions[action]["description"],
                                       self.actions[action]["actionType"],
                                       self.actions[action]["amount"],
                                       self.actions[action]["staminaExpense"],
                                       self.actions[action]["targetQuantity"],
                                       self.actions[action]["effectName"])

                enemy_actions.append(action_object)

            enemy_object = BattleEnemy(enemy,
                                       f":characters:{self.enemies[enemy]['sheet_name']}",
                                       self.enemies[enemy]['name'],
                                       self.enemies[enemy]['description'],
                                       self.enemies[enemy]['maxHealth'],
                                       self.enemies[enemy]['maxStamina'],
                                       self.enemies[enemy]['restoredStamina'],
                                       enemy_actions)


            self.enemy_team.append(enemy_object)

        self.enemy_attacking = self.enemy_team[0]

        self.remaining_enemy_objects = self.enemy_team.copy()

        self.initial_enemy_team_length = len(self.enemy_team)
        self.initial_player_team_length = len(self.player_team)

        for i in range(len(self.player_team)):
            self.initial_player_team_indexes.append(i)

        for i in range(len(self.enemy_team)):
            self.initial_enemy_team_indexes.append(i)

        print(self.initial_enemy_team_indexes)
        print(self.initial_player_team_indexes)

        for enemy in self.enemy_team:
            while len(new_enemy_x) > 0:
                self.setup_enemies(enemy, new_enemy_x[0], new_enemy_y[0])
                del new_enemy_x[0]
                del new_enemy_y[0]
                break

        # LLenar con listas vacias las listas de efectos aplicados a enemigos y aliados en función de su número,
        # por si llegan a tener más de un efecto aplicado a la vez

        for i in range(self.player_team_length):
            self.ally_effects_list.append([])

        for i in range(len(self.enemy_team)):
            self.enemy_effects_list.append([])

        self.enemy_AI = EnemyIA(self.enemy_team, self.player_team)

        for i in range(len(self.enemy_team)):
            self.remaining_enemies.append(i)

        for i in range(len(self.player_team)):
            self.remaining_allies.append(i)
            self.ally_rotation.append(i)

        for ally in self.player_team:
            health_width = ally.currentHealth * 100 / ally.maxHealth
            self.ally_health_bars.append(health_width)

        for ally in self.player_team:
            sta_width = ally.currentStamina * 100 / ally.maxStamina
            self.ally_sta_bars.append(sta_width)

        for enemy in self.enemy_team:
            health_width = enemy.currentHealth * 100 / enemy.maxHealth
            self.enemy_health_bars.append(health_width)

        for enemy in self.enemy_team:
            sta_width = enemy.currentStamina * 100 / enemy.maxStamina
            self.enemy_sta_bars.append(sta_width)

        self.pointer_x = self.x_positions[self.current_ally]
        self.pointer_y = self.y_positions[self.current_ally] + self.pointer_height_offset

        print("AQUIIIIIIIIIIIIIIIII")
        print(f"ally {self.remaining_allies}")
        print(f"enemy {self.remaining_enemies}")

    def on_hide_view(self):
        pygame.mixer.music.load(f"../resources/sounds/{self.window.views['game'].my_map.backgroundMusicName}")

        self.activated = False
        self.manager.clear()
        self.manager.disable()

        self.player_sprites.clear()
        self.enemy_sprites.clear()

    def on_draw(self):
        arcade.start_render() # Para que cada vez que se pinte un frame se limpie el de antes
        self.fondo.draw()

        current_width = self.get_width()
        border_width = 15

        # Actualizar posiciones de los aliados en cada momento para poder reescalarlos
        for i in range(len(self.player_sprites)):
            pos_inx = self.remaining_allies[i]
            self.player_sprites[i].center_x = self.x_positions[pos_inx]

        for i in range(len(self.player_sprites)):
            pos_inx = self.remaining_allies[i]
            self.player_sprites[i].center_y = self.y_positions[pos_inx]

        # Actualizar posiciones de los enemigos para lo mismo
        for i in range(len(self.enemy_sprites)):
            pos_inx = self.remaining_enemies[i]
            self.enemy_sprites[i].center_x = self.enemy_x_positions[pos_inx]

        for i in range(len(self.enemy_sprites)):
            pos_inx = self.remaining_enemies[i]
            self.enemy_sprites[i].center_y = self.enemy_y_positions[pos_inx]

        arcade.draw_rectangle_filled(center_x=current_width / 2,
                                     center_y=100,
                                     width=current_width,
                                     height=200,
                                     color=(16, 60, 131))

        arcade.draw_rectangle_filled(center_x=current_width / 2,
                                     center_y=61,
                                     width=current_width,
                                     height=200,
                                     color=(16, 52, 112))

        arcade.draw_rectangle_filled(center_x=current_width / 2,
                                     center_y=22,
                                     width=current_width,
                                     height=200,
                                     color=(17, 50, 104))

        arcade.draw_rectangle_filled(center_x=current_width / 2,
                                     center_y=-17,
                                     width=current_width,
                                     height=200,
                                     color=(17, 47, 101))

        arcade.draw_rectangle_filled(center_x=current_width / 2,
                                     center_y=-56,
                                     width=current_width,
                                     height=200,
                                     color=(17, 45, 95))

        # Bordes de fuera
        arcade.draw_lrtb_rectangle_outline(left = 5,
                                           right = current_width - border_width / 2,
                                           top = 202,
                                           bottom = 5,
                                           border_width = border_width,
                                           color = (88, 64, 52))

        arcade.draw_lrtb_rectangle_outline(left=5,
                                           right=current_width - border_width / 2,
                                           top=200,
                                           bottom=5,
                                           border_width=border_width - 4,
                                           color=(158, 118, 106))

        # Brillos y sombras
        arcade.draw_line(0, 206, current_width, 206, (222, 180, 138), 2)
        arcade.draw_line(2, 204, current_width - 2, 204, (241, 221, 192), 2)

        arcade.draw_line(10, 10, current_width - 13, 10, (222, 180, 138), 2)
        arcade.draw_line(10, 8, current_width - 13, 8, (241, 221, 192), 2)

        arcade.draw_line(2, 0, 2, 204, (222, 180, 138), 2)

        arcade.draw_line(12, 194, current_width - 15, 194, (88, 64, 52), 2)

        # Sombra azul
        # Horizontal
        arcade.draw_line(12, 192, current_width - 14, 192, (20, 32, 72), 2)
        arcade.draw_line(12, 15, current_width - 14, 15, (20, 32, 72), 2)

        # Vetical
        arcade.draw_line(13, 15, 13, 192, (20, 32, 72), 2)
        arcade.draw_line(current_width - 15, 15, current_width - 15, 192, (20, 32, 72), 2)

        arcade.draw_triangle_filled(x1=self.pointer_x - 2,
                                    y1=self.pointer_y + 64,
                                    x2=self.pointer_x - 9,
                                    y2=self.pointer_y + 92,
                                    x3=self.pointer_x + 5,
                                    y3=self.pointer_y + 92,
                                    color=arcade.color.BLACK)

        arcade.draw_triangle_filled(x1=self.pointer_x - 2,
                                    y1=self.pointer_y + 70,
                                    x2=self.pointer_x - 7,
                                    y2=self.pointer_y + 90,
                                    x3=self.pointer_x + 3,
                                    y3=self.pointer_y + 90,
                                    color=arcade.color.WHITE)

        # Barras de vida y de stamina de aliados

        health_height_dif = 80
        sta_height_dif = 90
        self.bar_width = 100
        bar_height = 5

        if self.bar_width > 0:

            for index in self.remaining_allies:
                center_x = self.x_positions[index]
                h_center_y = self.y_positions[index] - health_height_dif
                s_center_y = self.y_positions[index] - sta_height_dif
                n_center_y = h_center_y + 150
                name_x_offset = 67

                y_fix = bar_height / 2

                bar_pos = self.remaining_allies.index(index)

                remaining_list_index = self.remaining_allies.index(index)

                # Nombre
                self.draw_text_with_outline(
                    text=self.player_team[remaining_list_index].displayName,
                    x=center_x,
                    y=n_center_y,
                    text_color=arcade.color.WHITE,
                    outline_color=arcade.color.BLACK,
                    font_size=14,
                    border=1,
                    anchor_x="center"
                )

                # Vida
                arcade.draw_rectangle_filled(center_x,
                                             h_center_y,
                                             self.bar_width + 5,
                                             bar_height + 5,
                                             arcade.color.WHITE)

                arcade.draw_rectangle_filled(center_x,
                                             h_center_y,
                                             self.bar_width,
                                             bar_height,
                                             arcade.color.BLACK)

                arcade.draw_lrtb_rectangle_filled(center_x - self.bar_width / 2,
                                                   center_x - self.bar_width / 2 + self.ally_health_bars[bar_pos],
                                                   h_center_y + y_fix,
                                                   h_center_y - y_fix,
                                                   arcade.color.GREEN)

                # Stamina
                arcade.draw_rectangle_filled(center_x,
                                             s_center_y,
                                             self.bar_width + 5,
                                             bar_height + 5,
                                             arcade.color.WHITE)

                arcade.draw_rectangle_filled(center_x,
                                             s_center_y,
                                             self.bar_width,
                                             bar_height,
                                             arcade.color.BLACK)

                arcade.draw_lrtb_rectangle_filled(center_x - self.bar_width / 2,
                                                   center_x - self.bar_width / 2 + self.ally_sta_bars[bar_pos],
                                                   s_center_y + y_fix,
                                                   s_center_y - y_fix,
                                                   arcade.color.AZURE)

            # Barras de vida y stamina de los enemigos

            for index in self.remaining_enemies:
                center_x = self.enemy_x_positions[index]
                h_center_y = self.enemy_y_positions[index] - health_height_dif
                s_center_y = self.enemy_y_positions[index] - sta_height_dif
                enemy_h_center_y = self.enemy_y_positions[index] - health_height_dif
                enemy_s_center_y = self.enemy_y_positions[index] - sta_height_dif
                n_center_y = h_center_y + 120
                enemy_n_center_y = h_center_y + 150
                name_x_offset = 67

                y_fix = bar_height / 2

                bar_pos = self.remaining_enemies.index(index)

                remaining_list_index = self.remaining_enemies.index(index)

                # Nombre
                self.draw_text_with_outline(
                    text=self.enemy_team[remaining_list_index].displayName,
                    x=center_x,
                    y=enemy_n_center_y,
                    text_color=arcade.color.PERSIAN_RED,
                    outline_color=arcade.color.BLACK,
                    font_size=14,
                    border=1,
                    anchor_x="center"
                )

                # Vida
                arcade.draw_rectangle_filled(center_x,
                                             h_center_y,
                                             self.bar_width + 5,
                                             bar_height + 5,
                                             arcade.color.WHITE)

                arcade.draw_rectangle_filled(center_x,
                                             h_center_y,
                                             self.bar_width,
                                             bar_height,
                                             arcade.color.BLACK)

                arcade.draw_lrtb_rectangle_filled(center_x - self.bar_width / 2,
                                                   center_x - self.bar_width / 2 + self.enemy_health_bars[bar_pos],
                                                   h_center_y + y_fix,
                                                   h_center_y - y_fix,
                                                   arcade.color.OLD_MAUVE)

                # Stamina
                arcade.draw_rectangle_filled(center_x,
                                             s_center_y,
                                             self.bar_width + 5,
                                             bar_height + 5,
                                             arcade.color.WHITE)

                arcade.draw_rectangle_filled(center_x,
                                             s_center_y,
                                             self.bar_width,
                                             bar_height,
                                             arcade.color.BLACK)

                arcade.draw_lrtb_rectangle_filled(center_x - self.bar_width / 2,
                                                   center_x - self.bar_width / 2 + self.enemy_sta_bars[bar_pos],
                                                   s_center_y + y_fix,
                                                   s_center_y - y_fix,
                                                   arcade.color.MIDNIGHT_BLUE)

            else:
                pass

        if self.inventory_empty and self.option == "item":
            arcade.draw_text("El inventario esta vacio", start_y=100, start_x=self.current_width/2 - 100)

        if self.option == "menu" and self.sta_message:
            arcade.draw_text("La stamina ya esta al maximo", start_y=53, start_x=870)

        if self.att_sta_message:
            arcade.draw_text("No hay suficiente stamina", start_y=125, start_x=220)

        if self.option in self.key_controls_options:
            self.sprites_controles.draw()

            self.draw_text_with_outline("Controles", self.current_width - 291, 155, arcade.color.WHITE, arcade.color.BLACK, font_size=14)

            arcade.draw_text("Cambiar enemigo al atacar",
                             self.current_width - 220,
                             120,
                             font_size=10)

            arcade.draw_text("Confirmar accion",
                             self.current_width - 220,
                             80,
                             font_size=10)

            arcade.draw_text("Volver al menú anterior",
                             self.current_width - 220,
                             40,
                             font_size=10)

        self.player_sprites.draw()
        self.enemy_sprites.draw()

        self.manager.draw()
        self.manager.enable()

    def draw_text_with_outline(self, text, x, y, text_color, outline_color, font_size=12, font_name=None, border=1,
                               anchor_x="left"):
        for dx in (-border, 0, border):
            for dy in (-border, 0, border):
                if dx != 0 or dy != 0:
                    arcade.draw_text(text, x + dx, y + dy, outline_color, font_size, font_name=font_name,
                                     anchor_x=anchor_x)

        arcade.draw_text(text, x, y, text_color, font_size, font_name=font_name, anchor_x=anchor_x)

    def on_update(self, delta_time: float):
        pointer_positions = self.get_pointer_positions()

        self.flechaD.center_x = self.current_width - 250
        self.flechaI.center_x = self.current_width - 280
        self.teclaEnter1.center_x = self.current_width - 268
        self.teclaEnter2.center_x = self.current_width - 252
        self.teclaEsc.center_x = self.current_width - 252

        if self.option != "select_enemy":
            self.pointer_x = self.x_positions[self.current_ally]
        else:
            self.pointer_x = self.enemy_x_positions[self.current_selected_enemy]

        if not self.pointer_is_up:
            self.pointer_y += CHARACTER_POINTER_SPEED

            if self.pointer_y >= pointer_positions + 10:
                self.pointer_y = pointer_positions + 10
                self.pointer_is_up = True

        else:
            self.pointer_y -= CHARACTER_POINTER_SPEED

            if self.pointer_y <= pointer_positions:
                self.pointer_y = pointer_positions
                self.pointer_is_up = False

        self.ally_health_bars.clear()
        for ally in self.player_team:
            health_width = ally.currentHealth * self.bar_width / ally.maxHealth
            self.ally_health_bars.append(health_width)

        self.ally_sta_bars.clear()
        for ally in self.player_team:
            sta_width = ally.currentStamina * self.bar_width / ally.maxStamina
            self.ally_sta_bars.append(sta_width)

        self.enemy_health_bars.clear()
        for enemy in self.enemy_team:
            health_width = enemy.currentHealth * self.bar_width / enemy.maxHealth
            self.enemy_health_bars.append(health_width)

        self.enemy_sta_bars.clear()
        for enemy in self.enemy_team:
            sta_width = enemy.currentStamina * self.bar_width / enemy.maxStamina
            self.enemy_sta_bars.append(sta_width)

        self.current_width = self.get_width()
        self.width_scaling_factor = self.current_width / 1280

        self.current_height = self.get_height()
        self.height_scaling_factor = self.current_height / 720

        self.x_positions = ally_x_positions.copy()
        self.y_positions = ally_y_positions.copy()

        self.enemy_x_positions = enemy_x_positions.copy()
        self.enemy_y_positions = enemy_y_positions.copy()

        for i in range(len(self.x_positions)):
            self.x_positions[i] *= self.width_scaling_factor

        for i in range(len(self.y_positions)):
            self.y_positions[i] *= self.height_scaling_factor

        for i in range(len(self.enemy_x_positions)):
            self.enemy_x_positions[i] *= self.width_scaling_factor

        for i in range(len(self.enemy_y_positions)):
            self.enemy_y_positions[i] *= self.height_scaling_factor

        self.player_sprites.on_update(delta_time)
        self.enemy_sprites.on_update(delta_time)

        self.elapsed_time += delta_time
        self.attack_time += delta_time

        self.enemy_elapsed_time += delta_time

        if self.player_team[self.remaining_allies.index(self.current_ally)].currentAnimation == Anim.BATTLEIDLE:
            if self.elapsed_time >= self.interval:
                for player in self.player_team:
                    player.setPulseAnim(Anim.BATTLEIDLE)

                self.elapsed_time = 0

        if self.enemy_attacking.currentAnimation == Anim.BATTLEIDLE:
            if self.enemy_elapsed_time >= self.enemy_interval:
                for enemy in self.enemy_team:
                    enemy.setPulseAnim(Anim.BATTLEIDLE)

                self.enemy_elapsed_time = 0


        if self.waiting_for_action:
            if self.previous_option == "attack":
                self.time = self.attack_duration
            elif self.previous_option == "skill":
                self.time = self.skill_duration

            self.attack_time += delta_time
            if self.attack_time >= self.time:
                if not self.hurt:
                    self.enemy_team[self.remaining_enemies.index(self.current_selected_enemy)].setPulseAnim(Anim.HURT)
                    self.hurt = True

                if self.attack_time >= 2 * self.time:
                    self.waiting_for_action = False
                    self.attack_time = 0
                    self.hurt = False
                    self.perform_action()

        self.attack_anim_done = False
        self.hurt_anim_done = False

        self.ally_hurt_time += delta_time

        if self.enemy_waiting_for_action:
            self.player_turn = False
            self.enemy_attack_time += delta_time

            self.pointer_x = 100000

            if self.enemy_attack_time >= self.attack_duration:

                enemy = self.enemy_team[self.enemy_turn_index]
                self.enemy_attacking = enemy

                if self.enemy_chosen_action is None or self.enemy_chosen_target is None:
                    self.enemy_chosen_action, self.enemy_chosen_target = self.enemy_AI.returnTurnToExecute(enemy)
                    self.enemy_action_performed = self.enemy_chosen_action

                self.enemy_action_performed = self.enemy_chosen_action

                if not self.attack_anim_done:
                    self.enemy_attacking.setPulseAnim(Anim.ATTACK)
                    self.attack_anim_done = True

                if self.enemy_attack_time >= 1.5 * self.attack_duration:
                    if not self.hurt_anim_done:
                        self.enemy_chosen_target.setPulseAnim(Anim.HURT)
                        self.hurt_anim_done = True

                    if self.enemy_attack_time >= 3 * self.attack_duration:
                        idx_ally = self.player_team.index(self.enemy_chosen_target)
                        self.player_team[idx_ally].changeHealth(-self.enemy_chosen_action.amount)

                        print(f"{enemy.displayName} gasta {self.enemy_chosen_action.staminaExpense} de stamina")
                        print(f"{self.enemy_chosen_target.displayName} recibe {self.enemy_chosen_action.amount} de daño")

                        self.check_health_status()

                        self.enemy_attack_time = 0
                        self.enemy_chosen_action = None
                        self.enemy_chosen_target = None
                        self.enemy_turn_index += 1
                        print(f"eti {self.enemy_turn_index}")

                        if not self.player_team:
                            self.enemy_waiting_for_action = False
                            return

                        if self.enemy_turn_index >= len(self.enemy_team):
                            print("hola")
                            self.enemy_waiting_for_action = False
                            self.attack_anim_done = False
                            self.hurt_anim_done = False
                            self.enemy_chosen_action = None
                            self.enemy_chosen_target = None
                            self.enemy_attacking = self.enemy_team[0]
                            for enemy in self.enemy_team:
                                enemy.setPulseAnim(Anim.BATTLEIDLE)
                            self.round_end()
                            return
        else:
            if len(self.player_team) == 1:
                self.player_turn = True

    def get_pointer_positions(self):
        if self.option == "select_enemy":
            return self.enemy_y_positions[self.current_selected_enemy] + self.pointer_height_offset
        else:
            return self.y_positions[self.current_ally] + self.pointer_height_offset

    def on_click_attack(self, event):
        self.option = "attack"
        self.stage = 2
        self.change_buttons()
        self.sta_message = False
        self.att_sta_message = False
        self.item_used = None

    def on_click_skill(self, event):
        self.option = "skill"
        self.stage = 2
        self.change_buttons()
        self.sta_message = False
        self.att_sta_message = False
        self.item_used = None

    def on_click_item(self, event):
        self.manager.clear()
        self.inventory_empty = False
        self.sta_message = False
        self.att_sta_message = False

        self.option = "item"
        self.stage = 2

        if not self.inventory:
            self.manager.clear()
            self.inventory_empty = True

            return

        self.change_buttons()

    def on_click_rest(self, event):
        self.option = "rest"
        self.item_used = None

        print(f"current {self.player_team[self.current_ally_index].currentStamina}")
        print(f"max {self.player_team[self.current_ally_index].maxStamina}")

        if self.player_team[self.current_ally_index].currentStamina == self.player_team[self.current_ally_index].maxStamina:
            print("ESTE PERSONAJE YA TIENE LA STAMINA AL MÁXIMO")
            self.main_buttons()
            self.option = "menu"
            self.sta_message = True
        else:
            self.manager.clear()
            self.player_team[self.current_ally_index].changeStamina(self.player_team[self.current_ally_index].restoredStamina * 2)

            print(f"aliado {self.player_team[self.current_ally_index].displayName} gana"
                  f" {self.player_team[self.current_ally_index].restoredStamina * 2} de stamina")

            if self.player_team[self.current_ally_index].currentStamina > self.player_team[self.current_ally_index].maxStamina:
                self.player_team[self.current_ally_index].currentStamina = self.player_team[self.current_ally_index].maxStamina

            self.manager.clear()
            self.next_ally()

    def on_click_button(self, event):
        self.clicked_button_name = event.source.text
        print(f"button clicked: {self.clicked_button_name}")
        self.previous_option = self.option

        self.manager.clear()
        self.manager.disable()
        self.action_buttons.clear()

        if self.option == "attack" or self.option == "skill":
            for action in self.actions.values():
                if action["name"] == self.clicked_button_name:
                    print(f"stamina gastada {action['staminaExpense']}")

                    if self.player_team[self.current_ally_index].currentStamina >= action["staminaExpense"]:
                        if self.option == "skill":
                            for key, effect in self.effects.items():
                                effect = self.effects[key]
                                print("ULTIMO EMPUJON")
                                print(effect.get("effectType"))
                                if effect.get("effectType") == "Heal":
                                    print(effect)
                                    print(action["effectName"])
                                    if key == action["effectName"]:
                                        efecto = Effect(effect["name"],
                                                effect["description"],
                                                effect["effectType"],
                                                effect["amount"],
                                                effect["durationInTurns"],
                                                effect["statAffected"])

                                        self.ally_effects_list[self.current_ally].append(efecto)

                            self.next_ally()

                        else:
                            self.manager.clear()
                            self.manager.disable()
                            self.select_enemy_to_attack()

                    else:
                        print("NO TIENES SUFICIENTE STAMINA")
                        print(f"STAMINA ACTUAL {self.player_team[self.current_ally_index].currentStamina}")
                        self.main_buttons()
                        self.att_sta_message = True

            self.manager.clear()
            self.manager.disable()
            self.action_buttons.clear()

        elif self.previous_option == "item":
            for item in self.inventory:
                if self.clicked_button_name == item["name"]:
                    self.item_used = item

            self.perform_action()

        elif self.option == "revive_ally":
            for ally in self.dead_allies:
                if ally.displayName == self.clicked_button_name:
                    index = self.dead_allies.index(ally)

                    # Restaurar salud y estado
                    ally.setHealth(ally.maxHealth // 2)
                    ally.setPulseAnim(Anim.BATTLEIDLE)
                    ally.currentStamina = ally.restoredStamina

                    # Añadir a listas activas
                    self.player_team.append(ally)
                    self.player_sprites.append(ally)
                    revived_index = self.defeated_allies.pop(index)
                    self.remaining_allies.append(revived_index)

                    # Regenerar completamente la rotación de aliados
                    self.ally_rotation = self.remaining_allies.copy()

                    # Añadir sus barras de salud
                    self.ally_health_bars.append(ally.currentHealth * self.bar_width / ally.maxHealth)
                    self.ally_sta_bars.append(ally.currentStamina * self.bar_width / ally.maxStamina)

                    # Consumir ítem
                    if self.item_used in self.inventory:
                        self.inventory.remove(self.item_used)

                    self.current_ally = revived_index  # Usar el índice revivido
                    self.current_ally_index = self.remaining_allies.index(revived_index)
                    self.pointer_x = self.x_positions[self.current_ally]
                    self.pointer_y = self.y_positions[self.current_ally] + self.pointer_height_offset

                    # Restablecer estados
                    self.option = "menu"
                    self.allow_inputs = True
                    self.player_turn = True

                    self.dead_allies.remove(ally)

                    self.item_used = None

                    break

            self.next_ally()

    def setup_team(self, ally, x, y):
        character_sprite = ally
        character_sprite.center_x = x
        character_sprite.center_y = y

        character_sprite.scale = 2

        character_sprite.setPulseAnim(Anim.BATTLEIDLE)

        self.player_sprites.append(character_sprite)

    def setup_enemies(self, enemy, x, y):
        character_sprite = enemy
        character_sprite.scale = 2

        character_sprite.center_x = x
        character_sprite.center_y = y

        self.enemy_sprites.append(character_sprite)

    def on_key_press(self, key, _modifiers):
        if self.allow_inputs:

            if self.option == "select_enemy":
                if key == arcade.key.RIGHT or key == arcade.key.D:
                    while True:
                        if self.current_selected_enemy < self.initial_enemy_team_length - 1:
                            self.current_selected_enemy += 1

                        else:
                            self.current_selected_enemy = 0

                            if self.current_selected_enemy in self.defeated_enemies:
                                self.current_selected_enemy += 1
                        if self.current_selected_enemy in self.remaining_enemies:
                            break
                    self.select_enemy_to_attack()

                if key == arcade.key.LEFT or key == arcade.key.A:
                    while True:
                        if self.current_selected_enemy > 0:
                            self.current_selected_enemy -= 1

                        else:
                            self.current_selected_enemy = self.initial_enemy_team_length - 1

                            if self.current_selected_enemy in self.defeated_enemies:
                                self.current_selected_enemy -= 1
                        if self.current_selected_enemy in self.remaining_enemies:
                            break
                    self.select_enemy_to_attack()

                if self.item_used is not None:
                    if self.item_used["type"] == "DAMAGE":
                        if key == arcade.key.ENTER:
                            self.enemy_team[self.remaining_enemies.index(self.current_selected_enemy)].changeHealth(-self.item_used["amount"])
                            self.item_used = None
                            self.option = "menu"
                            self.check_health_status()
                            self.next_ally()

                else:
                    if key == arcade.key.ENTER:
                        if self.previous_option == "attack":
                            self.player_team[self.remaining_allies.index(self.current_ally)].setPulseAnim(Anim.ATTACK)
                        elif self.previous_option == "skill":
                            self.player_team[self.remaining_allies.index(self.current_ally)].setPulseAnim(Anim.SKILL)

                        #self.player_team[self.current_ally].setPulseAnim(Anim.ATTACK)
                        self.attack_time = 0
                        self.waiting_for_action = True
                        self.allow_inputs = False

            elif self.option == "revive_ally":
                if key == arcade.key.ENTER:
                    self.next_ally()

            else:
                if key == arcade.key.ESCAPE:
                    self.stage = 1
                    self.manager.clear()
                    self.action_buttons.clear()
                    self.main_buttons()
                    self.option = "menu"


    def get_width(self):
        window_size = self.window.get_size()
        current_width = window_size[0]
        return current_width

    def get_height(self):
        window_size = self.window.get_size()
        current_height = window_size[1]
        return current_height

    def main_buttons(self):
        self.contenedor.clear()
        self.manager.clear()

        self.fila1 = arcade.gui.UIBoxLayout(vertical=False, space_between=20)
        self.fila2 = arcade.gui.UIBoxLayout(vertical=False, space_between=20)

        attack_button = arcade.gui.UIFlatButton(text="Ataque", width=200)
        self.fila1.add(attack_button)
        attack_button.on_click = self.on_click_attack

        skill_button = arcade.gui.UIFlatButton(text="Habilidad", width=200)
        self.fila1.add(skill_button)
        skill_button.on_click = self.on_click_skill

        item_button = arcade.gui.UIFlatButton(text="Objeto", width=200)
        self.fila2.add(item_button)
        item_button.on_click = self.on_click_item

        rest_button = arcade.gui.UIFlatButton(text="Descansar", width=200)
        self.fila2.add(rest_button)
        rest_button.on_click = self.on_click_rest

        self.contenedor.add(self.fila1.with_space_around(bottom=20))
        self.contenedor.add(self.fila2)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center",
                anchor_y="bottom",
                align_y=35,
                child=self.contenedor
            )
        )

    def change_buttons(self):
        print(f"cb {self.dead_allies}")

        self.manager.clear()
        self.contenedor.clear()

        num_buttons = 0
        button_width = 300

        print(f"option en change_buttons {self.option}")
        if self.option == "attack" or self.option == "skill":

            # Transformar el diccionario en una lista (excluyendo el template) para poder acceder por índice
            characters = list(self.team.values())[1:] # ¡¡¡IMPORTANTE!!! Quitar el [1:] si se borra la template del JSON

            # Crear una lista con las acciones del personaje al que le toca el turno
            current_ally_actions = self.player_team[self.remaining_allies.index(self.current_ally)].actions

            # Crear el nuevo layout de botones a partir de la opción elegida en el menú principal de botones

            for action in current_ally_actions:
                action_category = None
                for global_action in self.actions.values():
                    if action.displayName == global_action["name"]:
                        action_category = global_action["option"]

                        if action_category == self.option:
                            button = arcade.gui.UIFlatButton(
                                text=action.displayName,
                                width=button_width,
                                height=30)
                            self.contenedor.add(button.with_space_around(10))
                            self.manager.add(self.contenedor)
                            button.on_click = self.on_click_button
                            self.action_buttons.append(button)
                            num_buttons += 1
                        else:
                            pass

            y_pos = 0
            if num_buttons == 4:
                y_pos = 25
            if num_buttons == 3:
                y_pos = 65
            if num_buttons == 2:
                y_pos = 105
            if num_buttons == 1:
                y_pos = 145

            self.manager.add(
                arcade.gui.UIAnchorWidget(
                    anchor_x="left",
                    anchor_y="bottom",
                    align_x=30,
                    align_y=y_pos,
                    child=self.contenedor
                )
            )

        elif self.option == "item":
            columns = []
            lengths_list = []
            contenedor = []

            column_width = button_width + 20  # espacio entre columnas
            item_counter = 0

            num_buttons = 0

            for item in self.inventory:
                if item['type'] != "REQUIREMENT":
                    if item_counter >= 12:
                        break

                    if item_counter % 4 == 0:
                        contenedor = arcade.gui.UIBoxLayout(vertical=True, space_between=10)
                        columns.append(contenedor)
                        lengths_list.append(0)

                    try:
                        button = arcade.gui.UIFlatButton(text = item["name"], width = button_width, height = 30)
                    except:
                        button = arcade.gui.UIFlatButton(text=item["short_name"], width=button_width, height=30)

                    contenedor.add(button)

                    button.on_click = self.on_click_button
                    self.action_buttons.append(button)

                    lengths_list[-1] += 1
                    num_buttons += 1
                    item_counter += 1

            while num_buttons % 4 == 0:
                print(num_buttons)
                lengths_list.append(4)
                num_buttons -= 4

                if num_buttons < 0:
                    break

            lengths_list.append(num_buttons)

            y_pos = 0

            for index, column in enumerate(columns):
                if lengths_list[index] == 4:
                    y_pos = 25
                if lengths_list[index] == 3:
                    y_pos = 65
                if lengths_list[index] == 2:
                    y_pos = 105
                if lengths_list[index] == 1:
                    y_pos = 145

                x_offset = 30 + (index * column_width)

                self.manager.add(
                    arcade.gui.UIAnchorWidget(
                        anchor_x="left",
                        anchor_y="bottom",
                        align_x=x_offset,
                        align_y=y_pos,
                        child=column
                    )
                )

        elif self.option == "revive_ally":
            print("si bro no te rayes")
            for ally in self.dead_allies:
                button = arcade.gui.UIFlatButton(
                    text=ally.displayName,
                    width=300,
                    height=30)
                self.contenedor.add(button.with_space_around(10))
                self.manager.add(self.contenedor)
                button.on_click = self.on_click_button
                self.action_buttons.append(button)
                num_buttons += 1

            y_pos = 0
            if num_buttons == 4:
                y_pos = 25
            if num_buttons == 3:
                y_pos = 65
            if num_buttons == 2:
                y_pos = 105
            if num_buttons == 1:
                y_pos = 145

            self.manager.add(
                arcade.gui.UIAnchorWidget(
                    anchor_x="left",
                    anchor_y="bottom",
                    align_x=30,
                    align_y=y_pos,
                    child=self.contenedor
                )
            )

        self.manager.enable()
        self.manager.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        if self.stage == 2:
            for button in self.action_buttons:
                if button.rect.collide_with_point(x, y):
                    if self.option == "attack" or self.option == "skill":
                        for action in self.actions.values():
                            if action["name"] == button.text:
                                print(button.text)
                                self.display_action_description(f'{action["description"]}\n\nCoste de stamina: {action["staminaExpense"]} sp')
                                self.clicked_button_name = button.text
                    elif self.option == "item":
                        for item in self.inventory:
                            try:
                                if item["name"] == button.text:
                                    if item["type"] == "HEAL":
                                        self.display_action_description_right(f'{item["description"]}\n\n Heal amount: {item["amount"]} lp')

                                    if item["type"] == "REVIVE" or item["type"] == "DAMAGE":
                                        self.display_action_description_right(item["description"])

                            except:
                                if item["short_name"] == button.text:
                                    self.display_action_description_right(f'Heal amount: {item["heal_amount"]} lp')

    def display_action_description_right(self, text):
        if self.description_is_displayed and self.description_widget.child.text == text:
            return

        if self.description_is_displayed:
            self.manager.remove(self.description_widget)

        label = arcade.gui.UITextArea(
            text = text,
            text_color = arcade.color.WHITE,
            font_size = 12,
            height = 100,
            width = 300
        )

        self.description_widget = arcade.gui.UIAnchorWidget(
                anchor_x="right",
                anchor_y="bottom",
                align_y=40,
                child=label
            )

        self.manager.add(self.description_widget)
        self.description_is_displayed = True

    def display_action_description(self, text):
        if self.description_is_displayed and self.description_widget.child.text == text:
            return

        if self.description_is_displayed:
            self.manager.remove(self.description_widget)

        label = arcade.gui.UITextArea(
            text=text,
            text_color=arcade.color.WHITE,
            font_size=12,
            height=100,
            width=300
        )

        self.description_widget = arcade.gui.UIAnchorWidget(
            anchor_x="center",
            anchor_y="bottom",
            align_y=40,
            child=label
        )

        self.manager.add(self.description_widget)
        self.description_is_displayed = True

    def select_enemy_to_attack(self):
        print(self.current_selected_enemy)
        self.option = "select_enemy"
        while True:
            if self.current_selected_enemy in self.remaining_enemies:
                self.pointer_x = self.enemy_x_positions[self.current_selected_enemy]
                self.pointer_y = self.get_pointer_positions()
                break
            else:
                self.current_selected_enemy = self.remaining_enemies[0]

    def next_ally(self):
        self.player_attacks += 1

        self.main_buttons()

        self.ally_rotation.append(self.ally_rotation.pop(0))

        if (self.ally_rotation != self.remaining_allies and len(self.player_team) > 1) or (
                len(self.player_team) == 1 and self.player_attacks <= 1):
            if self.r_done:
                self.ally_rotation = self.remaining_allies.copy()
                self.r_done = False

            # Obtener el índice válido en remaining_allies
            self.current_ally = self.ally_rotation[0]
            self.current_ally_index = self.remaining_allies.index(self.current_ally)

            # Actualizar posiciones del cursor usando current_ally_index
            self.pointer_x = self.x_positions[self.current_ally]
            self.pointer_y = self.y_positions[self.current_ally] + self.pointer_height_offset

            print(f"ALIADO ACTUAL: {self.current_ally} (Índice válido: {self.current_ally_index})")

            self.allow_inputs = True
            self.stage = 1
            self.action_buttons.clear()

            self.option = "menu"

        elif self.player_attacks >= len(self.player_team):
            print("ACABADO TURNO JUGADOR")
            self.player_turn = False
            self.perform_action()
            self.player_attacks = 0

    def perform_action(self):
        if self.player_turn:
            print("TURNO JUGADOR")
            if self.previous_option == "attack" or self.previous_option == "skill":

                for action in self.actions.values():
                    if action["name"] == self.clicked_button_name:
                        target = self.remaining_enemies.index(self.current_selected_enemy)

                        multiplier = 1
                        for effect in self.ally_effects_list[self.current_ally]:
                            if effect.effectType == "Multiplier":
                                multiplier = effect.amount

                        self.enemy_team[target].changeHealth(-(action["amount"]) * multiplier)

                        print(f"enemy index number: {self.current_selected_enemy} -{action['amount']} health")
                        for enemy in self.enemy_team:
                            print(f"ATTACKED ENEMY HEALTH: {enemy.currentHealth}")

                        if action["effectName"] != "":
                            applied_effect_name = self.effects[action["effectName"]]
                            applied_effect = Effect(applied_effect_name["name"],
                                                    applied_effect_name["description"],
                                                    applied_effect_name["effectType"],
                                                    applied_effect_name["amount"],
                                                    applied_effect_name["durationInTurns"],
                                                    None)

                            self.enemy_effects_list[self.current_selected_enemy].append(applied_effect)



                        self.player_team[self.current_ally_index].currentStamina -= action["staminaExpense"]
                        print(self.player_team[self.current_ally_index].currentStamina)

                if len(self.player_team) == 1:
                    self.main_buttons()
                    self.option = "menu"

                self.pointer_x = self.x_positions[self.current_ally]
                self.pointer_y = self.y_positions[self.current_ally]

                self.check_health_status()

            elif self.previous_option == "item":
                if self.item_used["type"] == "HEAL":
                    self.player_team[self.current_ally].changeHealth(self.item_used["amount"])
                    self.next_ally()
                    self.option = "menu"
                    self.stage = 1

                    self.inventory.remove(self.item_used)
                    self.item_used = None

                    return

                elif self.item_used["type"] == "MULTIPLIER":
                    for effect in self.effects:
                        if self.item_used["amount"] == self.effects["name"]:
                            efecto = Effect(effect["name"], effect["description"], effect["effectType"], effect["amount"], effect["durationInTurns"], None)

                            self.ally_effects_list[self.current_ally].append(efecto)

                    self.inventory.remove(self.item_used)
                    self.item_used = None

                    return

                elif self.item_used["type"] == "REVIVE":
                    self.option = "revive_ally"

                    if self.defeated_allies:
                        print("entra?")
                        self.manager.clear()

                        self.change_buttons()
                        self.display_action_description("Elige un jugador para revivir")

                        self.inventory.remove(self.item_used)
                        self.item_used = None

                    return

                elif self.item_used["type"] == "DAMAGE":
                    self.manager.clear()
                    self.manager.disable()
                    self.select_enemy_to_attack()

                    self.inventory.remove(self.item_used)

                    return

        else:
            self.manager.clear()
            self.manager.disable()
            self.enemy_chosen_action = None
            self.enemy_chosen_target = None
            self.enemy_waiting_for_action = True
            self.enemy_turn_index = 0
            self.enemy_attack_time = 0
            self.allow_inputs = False

    def round_end(self):
        print("entré")
        self.r_done = True

        self.player_turn = True

        self.round += 1

        # Reseteo del cursor
        self.pointer_x = self.x_positions[self.current_ally]
        self.pointer_y = self.y_positions[self.current_ally]

        # Para que aparezca el menu
        self.main_buttons()
        self.option = "menu"

        # Para aplicar los efectos
        # En aliados

        for unique_list in self.ally_effects_list:
            for effect in unique_list:
                print(effect.displayName)
                print(effect.effectType)
                try:
                    effect.duration -= 1
                    if effect.duration > 0:
                        target_ally_index = self.ally_effects_list.index(unique_list)
                        if effect.effectType == "Damage":
                            self.player_team[target_ally_index].changeHealth(-(effect.amount))
                        elif effect.effectType == "Heal":
                            print("llega")
                            self.player_team[target_ally_index].changeHealth(effect.amount)
                    else:
                        unique_list.remove(effect)
                except:
                    pass

        # En enemigos

        for unique_list in self.enemy_effects_list:
            for effect in unique_list:
                try:
                    effect.duration -= 1
                    if effect.duration > 0:
                        target_enemy_index = self.enemy_effects_list.index(unique_list)
                        if effect.effectType == "Damage":
                            self.enemy_team[target_enemy_index].changeHealth(-(effect.amount))
                            print(f"{self.enemy_team[target_enemy_index]} -{effect.amount} health")
                            print(self.enemy_team[target_enemy_index].currentHealth)
                        elif effect.effectType == "Heal":
                            self.enemy_team[target_enemy_index].changeHealth(effect.amount)
                            print(f"{effect} ended")
                    else:
                        unique_list.remove(effect)
                except:
                    pass

        self.check_health_status()

        for enemy in self.enemy_team:
            enemy.changeStamina(enemy.restoredStamina)
            if enemy.currentStamina > enemy.maxStamina:
                enemy.currentStamina = enemy.maxStamina

        for ally in self.player_team:
            ally.changeStamina(ally.restoredStamina)
            if ally.currentStamina > ally.maxStamina:
                ally.currentStamina = ally.maxStamina

        self.enemy_waiting_for_action = False
        self.enemy_attack_time = 0
        self.enemy_turn_index = 0
        self.attack_anim_done = False
        self.hurt_anim_done = False

        self.allow_inputs = True

    def check_health_status(self):
        print("NO NEGATIVO PLSSSSSS")
        print(self.player_team[0].currentHealth)

        for ally in self.player_team:
            if ally.currentHealth <= 0:
                removed_sprite_index = self.player_team.index(ally)

                self.dead_allies.append(self.player_team.pop(removed_sprite_index))
                self.player_sprites.pop(removed_sprite_index)

                popped_index = self.remaining_allies.pop(removed_sprite_index)
                self.ally_rotation = self.remaining_allies.copy()

                print(f"CUANDO MUERE REMAINING ES {self.remaining_allies}")
                print(f"CUANDO MUERE ROTATION ES {self.remaining_allies}")

                self.defeated_allies.append(popped_index)

                print(f"ELIMINADO {popped_index}")

        for enemy in self.enemy_team:
            if enemy.currentHealth <= 0:
                removed_sprite_index = self.enemy_team.index(enemy)
                #actual_removed_sprite_index = self.remaining_enemies.index(removed_sprite_index)

                self.enemy_team.pop(removed_sprite_index)
                self.enemy_sprites.pop(removed_sprite_index)

                #popped_index_index = self.remaining_positions.index(actual_removed_sprite_index)
                popped_index = self.remaining_enemies.pop(removed_sprite_index)

                #self.remaining_positions.pop(removed_sprite_index)
                #self.remaining_positions.insert(removed_sprite_index, None)

                self.defeated_enemies.append(popped_index)

                #self.remaining_enemy_objects.pop()

                print(self.remaining_enemies)
                print(self.defeated_enemies)
                print(f"removed sprite index: {removed_sprite_index}")
                #print(f"actual removed aprite index: {actual_removed_sprite_index}")

        if self.player_team:  # Si aún hay aliados vivos
            # Reasignar current_ally al primer aliado disponible
            self.current_ally = self.remaining_allies[0] if self.remaining_allies else 0
            self.current_ally_index = 0  # Índice en remaining_allies
            self.pointer_x = self.x_positions[self.current_ally]
            self.pointer_y = self.y_positions[self.current_ally]

        if not self.enemy_team:
            self.game_win()
            return

        if not self.player_team:
            self.game_over()
            return

        # Para que vuelva al turno del jugador y aparezca el menu
        if self.player_turn:
            self.player_turn = True
            self.main_buttons()
            self.option = "menu"
            self.next_ally()

    def game_over(self):
        self.window.show_view(self.window.views["gameOver"])

    def game_win(self):
        for ally in self.dead_allies:
            ally.setHealth(10)
            self.player_team.append(ally)

        battle_end_list = []

        for i in range(len(self.initial_team)):
            battle_end_list.append(None)

        for ally in self.player_team:
            ally_init_index = self.initial_team.index(ally)

            battle_end_list.pop(ally_init_index)
            battle_end_list.insert(ally_init_index, ally)

        for ally in self.player_team:
            ally.changeHealth((ally.currentHealth + ally.maxHealth) * 0.6)
            ally.changeStamina((ally.currentStamina + ally.maxStamina) * 0.6)

        self.window.views["game"].player_sprite.player_team = battle_end_list

        self.window.show_view(self.window.views["game"])
