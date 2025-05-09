"""
Inventory
"""
import arcade
from arcade import Sprite
import pyglet
import json
from rpg.BattleAlly import BattleAlly
from rpg.sprites.character_sprite import CharacterSprite, SPRITE_INFO, Anim
from rpg.constants import (CHARACTER_SPRITE_SIZE, SCREEN_WIDTH, ally_x_positions, ally_y_positions,
                           CHARACTER_POINTER_SPEED, enemy_x_positions, enemy_y_positions)

class InventoryView(arcade.View):
    def __init__(self):
        super().__init__()
        self.character_sprite = None
        self.team_names = None
        self.player_sprites = arcade.SpriteList()
        self.started = False
        arcade.set_background_color(arcade.color.ALMOND)
        self.inventory = []
        self.sprite_path = "../resources/items/"
        self.sprite_list = []
        self.selected_item = 0
        self.player_team = []
        self.player_team_sheets = arcade.SpriteList()
        self.y = 250
        with open("../resources/data/battleCharacters_dictionary.json", "r") as file:
            self.team = json.load(file)

    def on_draw(self):
        arcade.start_render()
        self.sprite_list = []
        display = pyglet.canvas.get_display()
        screen = display.get_default_screen()
        is_fullscreen = (self.window.width, self.window.height) == (screen.width, screen.height)
        print(self.player_team)

        arcade.draw_text(
            "Inventory",
            self.window.width / 2,
            self.window.height - 50,
            arcade.color.ALLOY_ORANGE,
            44,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width,
        )

        margin = 20
        rect_width = self.window.width / 3.5
        rect_height = self.window.height * 3 / 4
        center_y = self.window.height / 2

        left_x = margin + rect_width / 2
        right_x = self.window.width - margin - rect_width / 2

        arcade.draw_rectangle_filled(left_x, center_y, rect_width, rect_height, arcade.color.LIGHT_CORAL)
        arcade.draw_rectangle_filled(right_x, center_y, rect_width, rect_height, arcade.color.LIGHT_CORAL)

        # Agrupar por sheet_name
        grouped_items = {}
        for item in self.inventory:
            key = item["sheet_name"]
            if key in grouped_items:
                grouped_items[key]["amount"] += item.get("amount", 1)
            else:
                grouped_items[key] = {
                    "name": item["name"],
                    "description": item.get("description", "Sin descripción"),
                    "sheet_name": key,
                    "amount": item.get("amount", 1)
                }

        # Está en fullscreen
        start_x = 100  # posición inicial X
        start_y = self.window.height - 150  # posición inicial Y
        spacing_x = 100  # espacio horizontal entre ítems
        spacing_y = 70  # espacio vertical entre ítems
        columns = 3

        self.sprite_list = []
        self.sprite_to_item_map = []

        for i, item in enumerate(grouped_items.values()):
            row = i // columns
            col = i % columns

            x = start_x + col * spacing_x
            y = start_y - row * spacing_y

            sprite = arcade.Sprite(self.sprite_path + item["sheet_name"], scale=2)
            sprite.center_x = x
            sprite.center_y = y
            sprite.draw()

            self.sprite_list.append(sprite)
            self.sprite_to_item_map.append(item)

            # Dibujar la cantidad encima a la derecha
            arcade.draw_text(f"x{item['amount']}", x + 12, y - 30, arcade.color.BLACK, 14)

        if self.selected_item:
            text_x = self.window.width / 2 - 200
            text_y = self.window.height - 150
            arcade.draw_text(
                f"Nombre: {self.selected_item['name']}",
                text_x, text_y,
                arcade.color.BLACK, 20
            )
            arcade.draw_text(
                f"Descripción: {self.selected_item['description']}",
                text_x, text_y - 30,
                arcade.color.BLACK, 16,
                multiline=True,
                width=300
            )
            arcade.draw_text(
                f"Cantidad: {self.selected_item['amount']}",
                text_x, text_y - 60,
                arcade.color.BLACK, 16
            )
        self.player_team_sheets.draw()
    def setup(self):
        pass
    def on_show_view(self):
        self.y = 250
        arcade.set_background_color(arcade.color.ALMOND)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
        self.team_names = self.window.views["game"].player_sprite.player_team

        for character in self.team_names:
            if character in self.team and 'sheet_name' in self.team[character]:
                sheet_name = self.team[character]['sheet_name']

                # Cargar las texturas desde el spritesheet
                textures = arcade.load_spritesheet(
                    f":characters:{sheet_name}",
                    sprite_width=128,
                    sprite_height=128,
                    columns=9,
                    count=36
                )

                # Crear un Sprite y asignarle una textura
                sprite = Sprite()
                sprite.texture = textures[9]  # Usa la primera textura o la que quieras
                sprite.center_x = 1050
                sprite.center_y = self.y
                self.y += 100
                self.player_team_sheets.append(sprite)

        # new_ally_x = [430, 180, 345, 280]
        # new_ally_y = [490, 430, 345, 565]
        
        # for character in self.team_names:
        #     ally_instance = BattleAlly(f":characters:{self.team[character]['sheet_name']}",
        #                              self.team[character]['name'],
        #                              self.team[character]['description'],
        #                              self.team[character]['type'],
        #                              self.team[character]['maxStamina'],
        #                              self.team[character]['maxHealth'],
        #                              self.team[character]['restoredStamina'],
        #                              self.team[character]['actions'],
        #                              self.team[character]['dialogueNoItem'],
        #                              self.team[character]['dialogueWithItem'],
        #                              self.team[character]['requirementItemKey'])
        #
        #     self.player_team.append(ally_instance)
        #
        #     for character in self.player_team:
        #         while len(new_ally_x) > 0:
        #             self.setup_team(character.sheetName, new_ally_x[0], new_ally_y[0])
        #             del new_ally_x[0]
        #             del new_ally_y[0]
        #             break
    def on_key_press(self, symbol: int, modifiers: int):
        close_inputs = [
            arcade.key.ESCAPE,
            arcade.key.I
        ]
        if symbol in close_inputs:
            self.window.show_view(self.window.views["game"])

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        for i, sprite in enumerate(self.sprite_list):
            if sprite.collides_with_point((x, y)):
                self.selected_item = self.sprite_to_item_map[i]
                break

    # def setup_team(self, sheet_name, x, y):
    #     self.character_sprite = CharacterSprite(sheet_name)
    #
    #     self.character_sprite.center_x = x
    #     self.character_sprite.center_y = y
    #
    #     self.character_sprite.scale = 2
    #
    #     self.character_sprite.textures = arcade.load_spritesheet(
    #         sheet_name,
    #         sprite_width = CHARACTER_SPRITE_SIZE,
    #         sprite_height = CHARACTER_SPRITE_SIZE,
    #         columns = 9,
    #         count = 36,
    #     )
    #     start_index = SPRITE_INFO[Direction.RIGHT][0]
    #     self.character_sprite.texture = self.character_sprite.textures[start_index]
    #
    #     self.player_sprites.append(self.character_sprite)
        
    def on_update(self, delta_time: float):
        self.inventory = self.window.views["game"].player_sprite.inventory
        # print(self.inventory)
