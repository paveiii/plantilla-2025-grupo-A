import arcade
import arcade.gui
import json

from rpg.BattleEnemy import BattleEnemy
from rpg.BattleAlly import BattleAlly
from rpg.sprites.character_sprite import CharacterSprite, SPRITE_INFO, Anim
from rpg.sprites.player_sprite import PlayerSprite
from rpg.Effect import Effect
from rpg.EnemyIA import EnemyIA
from rpg.Action import Action
from rpg.constants import (CHARACTER_SPRITE_SIZE, SCREEN_WIDTH, ally_x_positions, ally_y_positions,
                           CHARACTER_POINTER_SPEED, enemy_x_positions, enemy_y_positions)
import time

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

        #PROXIMAMENTE: CREAR METODOS QUE CARGUEN LOS INTEGRANTES DE AMBOS EQUIPOS EN BASE A INFORMACION
        #DEL JUGADOR Y DEL WORLD_ENEMY.

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

        self.allow_inputs = True
        self.player_turn = True

        self.action_buttons = []

        self.description_widget = None
        self.description_is_displayed = False

        self.stage = 1

        self.inventory = []

        self.x_positions = ally_x_positions.copy()
        self.y_positions = ally_y_positions.copy()

        self.pointer_x = self.x_positions[self.current_ally]
        self.pointer_y = self.y_positions[self.current_ally]

        self.pointer_is_up = False

        self.inventory = self.window.views["game"].player_sprite.inventory

        self.current_selected_enemy = 0
        self.turn_ended = False

        print("Inventario cargado:", self.inventory)

        self.ally_effects_list = []
        self.enemy_effects_list = []

        self.enemy_AI = None

    def on_show_view(self):
        self.inventory = self.window.views["game"].player_sprite.inventory

        self.manager.enable()
        self.main_buttons()
        arcade.set_background_color(arcade.color.GREEN)

        # Load allies

        new_ally_x = ally_x_positions.copy()
        new_ally_y = ally_y_positions.copy()

        self.team_names = self.window.views["game"].player_sprite.player_team

        for character in self.team_names:
            player_actions = []
            for action in self.team[character]['actions']:

                action_object = Action(self.actions[action]["name"],
                                       self.actions[action]["description"],
                                       self.actions[action]["actionType"],
                                       self.actions[action]["amount"],
                                       self.actions[action]["staminaExpense"],
                                       self.actions[action]["targetQuantity"],
                                       self.actions[action]["effectName"])

                player_actions.append(action_object)

            ally_object = BattleAlly(f":characters:{self.team[character]['sheet_name']}",
                                     self.team[character]['name'],
                                     self.team[character]['description'],
                                     self.team[character]['type'],
                                     self.team[character]['maxStamina'],
                                     self.team[character]['maxHealth'],
                                     self.team[character]['restoredStamina'],
                                     player_actions,
                                     self.team[character]['dialogueNoItem'],
                                     self.team[character]['dialogueWithItem'],
                                     self.team[character]['requirementItemKey'])

            self.player_team.append(ally_object)

        self.player_team_length = len(self.player_team)
        print(f"Player team length: {self.player_team_length}")

        for character in self.player_team:
            while len(new_ally_x) > 0:
                self.setup_team(character.sheetName, new_ally_x[0], new_ally_y[0])
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

            enemy_object = BattleEnemy(f":characters:{self.enemies[enemy]['sheet_name']}",
                                       self.enemies[enemy]['name'],
                                       self.enemies[enemy]['description'],
                                       self.enemies[enemy]['maxStamina'],
                                       self.enemies[enemy]['maxHealth'],
                                       self.enemies[enemy]['restoredStamina'],
                                       enemy_actions)


            self.enemy_team.append(enemy_object)

        for enemy in self.enemy_team:
            while len(new_enemy_x) > 0:
                self.setup_enemies(enemy.sheetName, new_enemy_x[0], new_enemy_y[0])
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

    def on_hide_view(self):
        self.manager.clear()
        self.manager.disable()

        self.player_sprites.clear()
        self.enemy_sprites.clear()

        self.player_team.clear()

    def on_draw(self):
        current_width = self.get_width()
        border_width = 10

        self.clear()
        arcade.draw_rectangle_filled(center_x = current_width / 2,
                                     center_y = 100,
                                     width = current_width,
                                     height = 200,
                                     color = arcade.color.NAVY_BLUE)

        arcade.draw_lrtb_rectangle_outline(left = 5,
                                           right = current_width - border_width / 2,
                                           top = 200,
                                           bottom = 5,
                                           border_width = border_width,
                                           color = arcade.color.WHITE)

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

        self.player_sprites.draw()
        self.enemy_sprites.draw()

        self.manager.draw()
        self.manager.enable()

    def on_update(self, delta_time: float):
        pointer_positions = self.get_pointer_positions()
        if not self.pointer_is_up:
            self.pointer_y += CHARACTER_POINTER_SPEED

            if self.pointer_y >= pointer_positions + 10:
                self.pointer_is_up = True

        else:
            self.pointer_y -= CHARACTER_POINTER_SPEED

            if self.pointer_y <= pointer_positions:
                self.pointer_is_up = False

    def on_click_attack(self, event):
        self.option = "attack"
        self.stage = 2
        self.change_buttons()

    def on_click_skill(self, event):
        self.option = "skill"
        self.stage = 2
        self.change_buttons()

    def on_click_item(self, event):
        self.option = "item"
        self.stage = 2
        self.change_buttons()

    def on_click_rest(self, event):
        self.option = "rest"
        if self.current_ally <= 2:
            self.current_ally += 1

            self.pointer_x = self.x_positions[self.current_ally]
            self.pointer_y = self.y_positions[self.current_ally]
        else:
            self.current_ally = 0
            self.player_turn = False

    def on_click_button(self, event):
        print(f"button clicked: {self.clicked_button_name}")
        self.previous_option = self.option

        self.manager.clear()
        self.manager.disable()
        self.action_buttons.clear()

        if self.option == "attack" or self.option == "skill":
            self.select_enemy_to_attack()
            self.manager.clear()
            self.manager.disable()

        if self.option == "item":
            self.perform_action()

    def setup_team(self, sheet_name, x, y):
        self.character_sprite = CharacterSprite(sheet_name)

        self.character_sprite.center_x = x
        self.character_sprite.center_y = y

        self.character_sprite.scale = 2

        self.character_sprite.textures = arcade.load_spritesheet(
            sheet_name,
            sprite_width = CHARACTER_SPRITE_SIZE,
            sprite_height = CHARACTER_SPRITE_SIZE,
            columns = 9,
            count = 36,
        )
        start_index = SPRITE_INFO[Anim.RIGHT][0]
        self.character_sprite.texture = self.character_sprite.textures[start_index]

        self.player_sprites.append(self.character_sprite)

    def setup_enemies(self, sheet_name, x, y):
        self.character_sprite = CharacterSprite(sheet_name)
        self.character_sprite.scale = 2

        self. character_sprite.center_x = x
        self.character_sprite.center_y = y

        self.character_sprite.textures = arcade.load_spritesheet(
            sheet_name,
            sprite_width = CHARACTER_SPRITE_SIZE,
            sprite_height= CHARACTER_SPRITE_SIZE,
            columns = 9,
            count = 36,
        )
        start_index = SPRITE_INFO[Anim.LEFT][0]
        self.character_sprite.texture = self.character_sprite.textures[start_index]

        self.enemy_sprites.append(self.character_sprite)


    def on_key_press(self, key, _modifiers):

        if self.allow_inputs:

            if self.option == "select_enemy":
                if key == arcade.key.RIGHT or key == arcade.key.D:
                    if self.current_selected_enemy < 3:
                        self.current_selected_enemy += 1
                    else:
                        self.current_selected_enemy = 0
                    self.select_enemy_to_attack()

                if key == arcade.key.LEFT or key == arcade.key.A:
                    if self.current_selected_enemy > 0:
                        self.current_selected_enemy -= 1
                    else:
                        self.current_selected_enemy = 3
                    self.select_enemy_to_attack()

                if key == arcade.key.ENTER:
                    self.perform_action()

            else:
                if key == arcade.key.P and self.activated == False:
                    print("pantalla de batalla")
                    self.window.show_view(self.window.views["in_battle"])
                    self.activated = True

                if key == arcade.key.P and self.activated == True:
                    print("show game view")
                    self.window.show_view(self.window.views["game"])

                if key == arcade.key.ESCAPE:
                    self.stage = 1
                    self.manager.remove(self.description_widget)
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

    def get_pointer_positions(self):
        if self.option == "select_enemy":
            return enemy_y_positions[self.current_selected_enemy]
        else:
            return self.y_positions[self.current_ally]

    def main_buttons(self):
        self.contenedor.clear()
        self.manager.clear()

        self.fila1 = arcade.gui.UIBoxLayout(vertical=False, space_between=20)
        self.fila2 = arcade.gui.UIBoxLayout(vertical=False, space_between=20)

        attack_button = arcade.gui.UIFlatButton(text="Attack", width=200)
        self.fila1.add(attack_button)
        attack_button.on_click = self.on_click_attack

        skill_button = arcade.gui.UIFlatButton(text="Skill", width=200)
        self.fila1.add(skill_button)
        skill_button.on_click = self.on_click_skill

        item_button = arcade.gui.UIFlatButton(text="Item", width=200)
        self.fila2.add(item_button)
        item_button.on_click = self.on_click_item

        rest_button = arcade.gui.UIFlatButton(text="Rest", width=200)
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
        self.manager.clear()
        self.contenedor.clear()
        num_buttons = 0
        button_width = 300

        if self.option == "attack" or self.option == "skill":

            # Transformar el diccionario en una lista (excluyendo el template) para poder acceder por índice
            characters = list(self.team.values())[1:] # ¡¡¡IMPORTANTE!!! Quitar el [1:] si se borra la template del JSON

            # Crear una lista con las acciones del personaje al que le toca el turno
            current_ally_actions = characters[self.current_ally]["actions"]

            # Crear el nuevo layout de botones a partir de la opción elegida en el menú principal de botones
            for current_action in current_ally_actions:
                for global_action in self.actions:
                    if current_action == global_action: # Compara los nombres de las acciones del personaje con los del JSON de acciones
                        action_data = self.actions[global_action] # Guarda los datos de la acción del JSON que se está mirando

                        if action_data["option"] == self.option: # Compara si la opción actual es igual que la de la acción del JSON
                            button_row = arcade.gui.UIBoxLayout(vertical = False, space_between = 10)

                            button = arcade.gui.UIFlatButton(
                                text = action_data["name"],
                                width = button_width,
                                height = 30)
                            self.contenedor.add(button.with_space_around(10))
                            button.on_click = self.on_click_button
                            self.action_buttons.append(button)
                            num_buttons += 1

        elif self.option == "item":
            for item in self.inventory:
                if item['type'] != "REQUIREMENT":
                    try:
                        button = arcade.gui.UIFlatButton(text = item["name"], width = button_width, height = 30)
                    except:
                        button = arcade.gui.UIFlatButton(text=item["short_name"], width=button_width, height=30)
                    self.contenedor.add(button.with_space_around(10))
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
                align_x = 30,
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
                                self.display_action_description(f'{action["description"]}\n\nStamina expense: {action["staminaExpense"]} sp')
                                self.clicked_button_name = button.text
                    elif self.option == "item":
                        print("Volver a hacer esta parte de código y no olvidar self.clicked_button_name")
                    #    for item in self.inventory:
                    #        try:
                    #            if item["short_name"] == button.text:
                    #                self.display_action_description(f'Heal amount: {item["heal_amount"]} lp')

    def display_action_description(self, text):
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
                anchor_x="center",
                anchor_y="bottom",
                align_y=40,
                child=label
            )

        self.manager.add(self.description_widget)
        self.description_is_displayed = True

    def select_enemy_to_attack(self):
        self.option = "select_enemy"
        self.pointer_x = enemy_x_positions[self.current_selected_enemy]
        self.pointer_y = enemy_y_positions[self.current_selected_enemy]
        self.manager.clear()
        self.manager.disable()

    def next_ally(self):
        if self.current_ally <= self.player_team_length - 2: # -1 Porque la listas empiezan en 0 y -1 más para que cuando el úlitmo aliado termine el cursor de batalla no se vaya al primero
            self.current_ally += 1
            self.allow_inputs = True
            self.manager.remove(self.contenedor)
            self.stage = 1
            self.action_buttons.clear()
            self.main_buttons()
            self.option = "menu"
            self.pointer_x = self.x_positions[self.current_ally]
            self.pointer_y = self.y_positions[self.current_ally]

        else:
            self.player_turn = False
            self.perform_action() # Como player turn se pone a False se ejecutarán los turnos del equipo enemigo.

            self.current_ally = 0
            self.pointer_x = self.x_positions[self.current_ally]

    def perform_action(self):
        if self.player_turn:
            if self.previous_option == "attack" or self.previous_option == "skill":

                for action in self.actions.values():
                    if action["name"] == self.clicked_button_name:
                        self.enemy_team[self.current_selected_enemy].changeHealth(action["amount"])

                        print(f"enemy index number: {self.current_selected_enemy} -{action['amount']} health")

                        if action["effectName"] != "":
                            applied_effect_name = self.effects[action["effectName"]]
                            applied_effect = Effect(applied_effect_name["name"],
                                                    applied_effect_name["description"],
                                                    applied_effect_name["effectType"],
                                                    applied_effect_name["amount"],
                                                    applied_effect_name["durationInTurns"],
                                                    None)

                            self.enemy_effects_list[self.current_selected_enemy].append(applied_effect)



                        self.player_team[self.current_ally].currentStamina -= action["staminaExpense"]
                        print(self.player_team[self.current_ally].currentStamina)

                self.next_ally()

            if self.previous_option == "item":
                print("CUANDO LOS ITEMS TENGAN SU FORMA DEFINITIVA HACER ESTA PARTE DE CÓDIGO PARA APLICAR LOS EFECTOS")
                self.next_ally()
                        # if item["heal_amount"] >= ¡¡¡HACER LA LISTA DE OBJETOS DE ALIADOS!!!
        else:
            self.pointer_x = 100000
            for i in range(len(self.enemy_team)):
                action_to_execute, ally_target = self.enemy_AI.returnTurnToExecute(
                    self.enemy_team[self.current_selected_enemy])

                ally_target_index = self.player_team.index(ally_target)

                self.player_team[ally_target_index].changeHealth(-(action_to_execute.amount))

                print(f"{self.player_team[ally_target_index].displayName} - {action_to_execute.amount} de vida")