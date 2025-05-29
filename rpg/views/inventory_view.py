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
        self.hover_item = None
        self.hover_index = None
        self.item_list = arcade.SpriteList()
        self.characters = []
        self.player = None
        self.marco = None
        self.character_sprite = None
        self.team_names = None
        self.player_sprites = arcade.SpriteList()
        self.started = False
        arcade.set_background_color(arcade.color.BISQUE)
        self.inventory = []
        self.sprite_path = "../resources/items/"
        self.sprite_list = []
        self.selected_item = 0
        self.player_team = []
        self.player_team_sheets = arcade.SpriteList()
        self.y = 250
        self.changed = False
        self.captainIcon = None
        self.medicIcon = None
        self.fighterIcon = None
        self.icon = None
        self.scale = 1.40
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

        arcade.draw_rectangle_filled(left_x, center_y, rect_width, rect_height, arcade.color.BURLYWOOD)
        arcade.draw_rectangle_filled(right_x, center_y, rect_width, rect_height, arcade.color.SANDY_BROWN)

        # self.player.draw()
        # Agrupar por sheet_name
        grouped_items = {}
        for item in self.inventory:
            key = item["sheet_name"]
            if key in grouped_items:
                grouped_items[key]["quantity"] += item.get("quantity", 1)
            else:
                grouped_items[key] = {
                    "name": item["name"],
                    "description": item.get("description", "Sin descripción"),
                    "sheet_name": key,
                    "quantity": item.get("quantity", 1)
                }

        start_x = 100  # posición inicial X
        start_y = self.window.height - 150  # posición inicial Y
        spacing_x = 100  # espacio horizontal entre ítems
        spacing_y = 70  # espacio vertical entre ítems
        columns = 3

        self.sprite_list = []
        self.sprite_to_item_map = []

        # Dibujar cuadrícula vacía
        total_slots = 21
        columns = 3
        rows = total_slots // columns
        slot_size = 64

        for i in range(total_slots):
            row = i // columns
            col = i % columns
            x = start_x + col * spacing_x
            y = start_y - row * spacing_y

            # Fondo del slot
            if self.marco:
                self.marco.center_x = x
                self.marco.center_y = y
                self.marco.draw()
            # arcade.draw_rectangle_filled(x, y, slot_size, slot_size, arcade.color.BONE)
            # arcade.draw_rectangle_outline(x, y, slot_size, slot_size, arcade.color.DARK_BROWN, 2)

        self.item_list = []

        for i, item in enumerate(grouped_items.values()):
            row = i // columns
            col = i % columns
            x = start_x + col * spacing_x
            y = start_y - row * spacing_y

            sprite = arcade.Sprite(self.sprite_path + item["sheet_name"], scale=1.4)
            if self.hover_index == i:
                sprite.scale = 1.6
            else:
                sprite.scale = 1.4
            sprite.center_x = x
            sprite.center_y = y
            sprite.draw()

            self.item_list.append(sprite)
            self.sprite_list.append(sprite)
            self.sprite_to_item_map.append(item)

            # Dibujar la cantidad encima a la derecha
            arcade.draw_text(f"x{item['quantity']}", x + 12, y - 30, arcade.color.BLACK, 14)

        if self.selected_item:
            # Si el selected_item es un item
            if self.selected_item in self.sprite_to_item_map:
                self.dibujar_info_item()

            # Si el selected_item es un aliado
            if self.selected_item in self.characters:
                self.dibujar_info_personaje()
        self.player_team_sheets.draw()
    def setup(self):
        self.marco = arcade.Sprite("../resources/UIThings/marco.png", scale = 0.5)
        sheet_name = "Test/testWalk2.png"

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
        sprite.texture = textures[9]
        sprite.center_x = 1200
        sprite.center_y = 550
        self.player = sprite

        self.captainIcon = arcade.Sprite("../resources/UIThings/captainIcon.png")
        self.medicIcon = arcade.Sprite("../resources/UIThings/medicIcon.png")
        self.fighterIcon = arcade.Sprite("../resources/UIThings/fighterIcon.png")


    def on_show_view(self):
        self.y = 250
        arcade.set_background_color(arcade.color.BISQUE)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
        self.team_sprites = self.window.views["game"].player_sprite.player_team
        self.player_team_sheets = arcade.SpriteList()
        self.characters = []

        for character in self.team_sprites:
            # Crear un Sprite y asignarle una textura
            sprite = character
            sprite.texture = character.textures[9]
            sprite.center_x = 1075
            sprite.center_y = self.y
            sprite.scale = 2
            self.y += 130
            self.characters.append(character)
            self.player_team_sheets.append(sprite)

    def dibujar_info_personaje(self):
        # Hecho con arcade.Text para poder ajustar los textos en base a la altura del anterior
        if self.selected_item not in self.characters:
            return

        text_x = self.window.width / 2 - 200
        current_y = self.window.height - 150
        width = 300
        spacing = 10  # Espaciado vertical entre textos

        # Nombre
        name_text = arcade.Text(
            f"Nombre: {self.selected_item.displayName}",
            text_x, current_y,
            arcade.color.BLACK, 20,
            font_name="calibri",
            multiline=True,
            width=350
        )
        name_text.draw()
        current_y -= name_text.content_height + spacing

        # Tipo
        tipo_text = arcade.Text(
            f"Tipo: {self.selected_item.type}",
            text_x, current_y,
            arcade.color.BLACK, 16,
            width=width,
            multiline=True,
            font_name="calibri"
        )
        tipo_text.draw()
        current_y -= tipo_text.content_height + spacing

        # Icono
        if self.icon:
            self.icon.center_x = text_x + 160
            self.icon.center_y = current_y + tipo_text.content_height + 20
            self.icon.scale = 0.5
            self.icon.draw()

        # Vida
        vida_text = arcade.Text(
            f"Vida: {self.selected_item.currentHealth}",
            text_x, current_y,
            arcade.color.BLACK, 16,
            width=width,
            multiline=True,
            font_name="calibri"
        )
        vida_text.draw()
        current_y -= vida_text.content_height + spacing

        # Acciones
        acciones_str = ", ".join(action.displayName for action in self.selected_item.actions)
        acciones_text = arcade.Text(
            f"Acciones: {acciones_str}",
            text_x, current_y,
            arcade.color.BLACK, 16,
            width=width,
            multiline=True,
            font_name="calibri"
        )
        acciones_text.draw()

    def dibujar_info_item(self):
        # Hecho con arcade.Text para poder ajustar los textos en base a la altura del anterior
        if not self.selected_item or self.selected_item not in self.sprite_to_item_map:
            return

        text_x = self.window.width / 2 - 200
        current_y = self.window.height - 150
        width = 300
        spacing = 10

        # Nombre
        name_text = arcade.Text(
            f"Nombre: {self.selected_item['name']}",
            text_x, current_y,
            arcade.color.BLACK, 20,
            width=width,
            multiline=True,
            font_name="calibri"
        )
        name_text.draw()
        current_y -= name_text.content_height + spacing

        # Descripción
        desc_text = arcade.Text(
            f"Descripción: {self.selected_item['description']}",
            text_x, current_y,
            arcade.color.BLACK, 16,
            width=width,
            multiline=True,
            font_name="calibri"
        )
        desc_text.draw()
        current_y -= desc_text.content_height + spacing

        # Cantidad
        amount_text = arcade.Text(
            f"Cantidad: {self.selected_item['quantity']}",
            text_x, current_y,
            arcade.color.BLACK, 16,
            font_name="calibri"
        )
        amount_text.draw()

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
        for i, sprite in enumerate(self.player_team_sheets):
            if sprite.collides_with_point((x, y)):
                self.selected_item = self.characters[i]
                break
    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        # Resetear escala de sprites de equipo
        for sprite in self.player_team_sheets:
            sprite.scale = 2
        # Cambiar escala al hacer hover
        for i, sprite in enumerate(self.player_team_sheets):
            if sprite.collides_with_point((x, y)):
                sprite.scale = 2.1
                break

        self.hover_index = None
        for i, sprite in enumerate(self.item_list):
            if sprite.collides_with_point((x, y)):
                self.hover_index = i
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

        if self.selected_item in self.characters:
            if self.selected_item.type == "Captain" or self.selected_item.type == "Tank":
                self.icon = self.captainIcon
            elif self.selected_item.type == "Medic":
                self.icon = self.medicIcon
            elif self.selected_item.type == "Fighter":
                self.icon = self.fighterIcon
        # print(self.inventory)
