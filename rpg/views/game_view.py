"""
Main game view
"""
import datetime
import json
from functools import partial
from typing import Callable

import arcade
import arcade.gui
from arcade import SpriteList, Sprite, get_image
from arcade.gui import UIFlatButton

import rpg.constants as constants
from arcade.experimental.lights import Light
from pyglet.math import Vec2

from rpg.load_game_map import load_map
from rpg.message_box import MessageBox
from rpg.sprites.WorldAlly import WorldAlly
from rpg.sprites.WorldItem import WorldItem


class DebugMenu(arcade.gui.UIBorder, arcade.gui.UIWindowLikeMixin):
    def __init__(
        self,
        *,
        width: float,
        height: float,
        noclip_callback: Callable,
        hyper_callback: Callable,
    ):

        self.off_style = {
            "bg_color": arcade.color.BLACK,
        }

        self.on_style = {
            "bg_color": arcade.color.REDWOOD,
        }

        self.setup_noclip(noclip_callback)
        self.setup_hyper(hyper_callback)

        space = 10

        self._title = arcade.gui.UITextArea(
            text="DEBUG MENU",
            width=width - space,
            height=height - space,
            font_size=14,
            text_color=arcade.color.BLACK,
        )

        group = arcade.gui.UIPadding(
            bg_color=(255, 255, 255, 255),
            child=arcade.gui.UILayout(
                width=width,
                height=height,
                children=[
                    arcade.gui.UIAnchorWidget(
                        child=self._title,
                        anchor_x="left",
                        anchor_y="top",
                        align_x=10,
                        align_y=-10,
                    ),
                    arcade.gui.UIAnchorWidget(
                        child=arcade.gui.UIBoxLayout(
                            x=0,
                            y=0,
                            children=[
                                arcade.gui.UIPadding(
                                    child=self.noclip_button, pading=(5, 5, 5, 5)
                                ),
                                arcade.gui.UIPadding(
                                    child=self.hyper_button, padding=(5, 5, 5, 5)
                                ),
                            ],
                            vertical=False,
                        ),
                        anchor_x="left",
                        anchor_y="bottom",
                        align_x=5,
                    ),
                ],
            ),
        )

        # x and y don't seem to actually change where this is created. bug?
        # TODO: make this not appear at the complete bottom left (top left would be better?)
        super().__init__(border_width=5, child=group)

    def setup_noclip(self, callback: Callable):
        # disable player collision

        def toggle(*args):
            # toggle state on click
            self.noclip_status = True if not self.noclip_status else False
            self.noclip_button._style = (
                self.off_style if not self.noclip_status else self.on_style
            )
            self.noclip_button.clear()

            callback(status=self.noclip_status)

        self.noclip_status = False
        self.noclip_button = arcade.gui.UIFlatButton(
            text="noclip", style=self.off_style
        )
        self.noclip_button.on_click = toggle  # type: ignore

    def setup_hyper(self, callback: Callable):
        # increase player speed

        def toggle(*args):
            # toggle state on click
            self.hyper_status = True if not self.hyper_status else False
            self.hyper_button._style = (
                self.off_style if not self.hyper_status else self.on_style
            )
            self.hyper_button.clear()

            callback(status=self.hyper_status)

        self.hyper_status = False

        self.hyper_button = arcade.gui.UIFlatButton(text="hyper", style=self.off_style)
        self.hyper_button.on_click = toggle  # type: ignore


class GameView(arcade.View):
    """
    Main application class.
    """

    def __init__(self, map_list, player, saveFileData):
        super().__init__()

        self.saveFile = None
        if (saveFileData != None):
            self.saveFile = saveFileData

        self.item_nuevo = None
        self.old_ally_battle = None
        self.button_clicked = False
        self.E_pressed = None
        self.dialogue_list = None
        self.other_dialogue = None
        self.dialogues_length = None
        self.current_dialog = 0
        self.dialogue_background = None
        self.main_buttons_widget = None
        self.anchor_widget = None
        self.selected_ally = None
        self.y = 200
        self.ally_colliding = None
        self.item = False
        self.dialogue = None
        arcade.set_background_color(arcade.color.AMAZON)

        self.setup_debug_menu()

        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()

        # Player sprite
        self.player_sprite = player
        self.player_sprite_list = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Physics engine
        self.physics_engine = None

        # Maps
        self.map_list = map_list

        # Name of map we are on
        self.cur_map_name = None

        self.message_box = None

        # Selected Items Hotbar
        self.hotbar_sprite_list = None
        self.selected_item = 1

        self.dialogues_active = False
        self.allys_colliding = SpriteList()
        self.letraE = None
        self.team_names = ""
        self.player_team_sheets = arcade.SpriteList()
        self.team_sprites = arcade.SpriteList()
        self.x = 1000

        # Cargamos el sonido al abrir y cerrar diálogos
        # self.pergamino_sound = arcade.load_sound("../resources/sounds/pergamino.wav")
        # Temporizador para saber cuando reproducir el sonido
        # self.grass_sound_timer = 0
        # self.grass_sound = arcade.load_sound("../resources/sounds/grass_sound.wav")
        # --- Required for all code that uses UI element, a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        x = self.player_sprite.center_x
        y = self.player_sprite.center_y
        start_game_button = arcade.gui.UIFlatButton(x = x + 234, y = y, text="1", width=50)
        self.v_box.add(start_game_button.with_space_around(bottom=20))
        # start_game_button.on_click = self.on_click_start_game_button

        load_game_button = arcade.gui.UIFlatButton(x = x, y = y, text="2", width=50)
        self.v_box.add(load_game_button.with_space_around(bottom=20))
        # load_game_button.on_click = self.on_click_load_game_button

        exit_button = arcade.gui.UIFlatButton(x = x, y = y, text="3", width=50)
        self.v_box.add(exit_button.with_space_around(bottom=20))
        # exit_button.on_click = self.on_click_exit_button

        exit_button = arcade.gui.UIFlatButton(x = x, y = y, text="4", width=50)
        self.v_box.add(exit_button.with_space_around(bottom=20))
        # exit_button.on_click = self.on_click_exit_button

        self.contenedor = arcade.gui.UIBoxLayout()
        # Flag para controlar la creacion de los botones
        self.buttons_visible = False

        self.team_buttons = []

        f = open("../resources/data/worldItem_dictionary.json")
        self.worldItem_dictionary = json.load(f)

        f = open("../resources/data/battleCharacters_dictionary.json")
        self.team = json.load(f)

        f = open("../resources/data/item_dictionary.json")
        self.item_dictionary = json.load(f)

        f = open("../resources/data/characters_dictionary.json")
        self.enemy_dictionary = json.load(f)

        # Cameras
        self.camera_sprites = arcade.Camera(self.window.width, self.window.height)
        self.camera_gui = arcade.Camera(self.window.width, self.window.height)

        # Create a small white light
        x = 100
        y = 200
        radius = 150
        mode = "soft"
        color = arcade.csscolor.WHITE
        self.player_light = Light(x, y, radius, color, mode)

    def switch_map(self, map_name,start_x,start_y, wipePreviousMaps):
        """
        Switch the current map
        :param map_name: Name of map to switch to
        :param start_x: Grid x location to spawn at
        :param start_y: Grid y location to spawn at
        """

        if(map_name not in self.map_list):
            if(wipePreviousMaps): self.map_list.clear()
            self.map_list[map_name] = load_map(f"../resources/maps/{map_name}.json",self.player_sprite)

        self.cur_map_name = map_name

        try:
            self.my_map = self.map_list[self.cur_map_name]
        except KeyError:
            raise KeyError(f"Unable to find map named '{map_name}'.")
        if self.my_map.background_color:
            arcade.set_background_color(self.my_map.background_color)

        map_height = self.my_map.map_size[1]

        self.player_sprite.center_x = start_x * constants.MAP_TILE_SIZE + constants.MAP_TILE_SIZE/2 #* constants.SPRITE_SIZE + constants.SPRITE_SIZE / 2
        self.player_sprite.center_y = (map_height - start_y) * constants.MAP_TILE_SIZE - constants.MAP_TILE_SIZE/2 #* constants.SPRITE_SIZE - constants.SPRITE_SIZE / 2
        self.scroll_to_player(1.0)
        self.player_sprite_list = arcade.SpriteList()
        self.player_sprite_list.append(self.player_sprite)

        self.setup_physics()

        if self.my_map.light_layer:
            self.my_map.light_layer.resize(self.window.width, self.window.height)

    def setup_physics(self):
        if self.noclip_status:
            # make an empty spritelist so the character does not collide with anyting
            self.physics_engine = arcade.PhysicsEngineSimple(
                self.player_sprite, arcade.SpriteList()
            )
        else:
            # use the walls as normal
            self.physics_engine = arcade.PhysicsEngineSimple(
                self.player_sprite, self.my_map.scene["wall_list"]
            )

    def setup(self):
        """Set up the game variables. Call to re-start the game."""

        #Spawn player
        print(self.map_list)

        if(self.saveFile != None):
            print(self.saveFile)
            start_x = self.saveFile[1][0]
            start_y = self.saveFile[1][1]
            print(start_x, start_y)
        else:
            try:
                start_x = self.map_list[constants.STARTING_MAP].properties.get("start_x")
                start_y = self.map_list[constants.STARTING_MAP].properties.get("start_y")
            except KeyError:
                    raise KeyError(f"Unable to find map named '{constants.STARTING_MAP}'.")


        if(self.saveFile != None):
            self.switch_map(self.saveFile[0], start_x, start_y, False)
            self.cur_map_name = self.saveFile[0]
        else:
            self.switch_map(constants.STARTING_MAP, start_x, start_y, False)
            self.cur_map_name = constants.STARTING_MAP


        self.dialogue_background = arcade.Sprite("../resources/UIThings/dialogoFondo.png")
        self.dialogue_background.center_x = self.player_sprite.center_x + 450
        self.dialogue_background.center_y = self.player_sprite.center_y - 450
        # Set up the hotbar
        self.load_hotbar_sprites()

    def load_hotbar_sprites(self):
        """Load the sprites for the hotbar at the bottom of the screen.

        Loads the controls sprite tileset and selects only the number pad button sprites.
        These will be visual representations of number keypads (1️⃣, 2️⃣, 3️⃣, ..., 0️⃣)
        to clarify that the hotkey bar can be accessed through these keypresses.
        """

        first_number_pad_sprite_index = 51
        last_number_pad_sprite_index = 61

        self.hotbar_sprite_list = arcade.load_spritesheet(
            file_name="../resources/tilesets/input_prompts_kenney.png",
            sprite_width=16,
            sprite_height=16,
            columns=34,
            count=816,
            margin=1,
        )[first_number_pad_sprite_index:last_number_pad_sprite_index]

    def setup_debug_menu(self):
        self.debug = False

        self.debug_menu = DebugMenu(
            width=450,
            height=200,
            noclip_callback=self.noclip,
            hyper_callback=self.hyper,
        )

        self.original_movement_speed = constants.MOVEMENT_SPEED
        self.noclip_status = False

    def enable_debug_menu(self):
        self.ui_manager.add(self.debug_menu)

    def disable_debug_menu(self):
        self.ui_manager.remove(self.debug_menu)

    def noclip(self, *args, status: bool):
        self.noclip_status = status

        self.setup_physics()

    def hyper(self, *args, status: bool):
        constants.MOVEMENT_SPEED = (
            int(self.original_movement_speed * 3.5)
            if status
            else self.original_movement_speed
        )

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()
        cur_map = self.map_list[self.cur_map_name]

        # --- Light related ---
        # Everything that should be affected by lights gets rendered inside this
        # 'with' statement. Nothing is rendered to the screen yet, just the light
        # layer.
        with cur_map.light_layer:
            arcade.set_background_color(cur_map.background_color)

            # Antes del cambio
            # # Grab each tile layer from the map
            # map_layers = cur_map.map_layers
            #
            # # Draw scene
            # cur_map.scene.draw()

            # Use the scrolling camera for sprites
            self.camera_sprites.use()
            map_layers = cur_map.map_layers
            for layer_name, sprite_list in cur_map.scene.name_mapping.items():
                if layer_name == "top" or layer_name == "shadows_top":
                    continue  # saltamos la capa

                sprite_list.draw()

            shadows_top = cur_map.scene.name_mapping.get("shadows_top")
            if shadows_top:
                shadows_top.draw()
            # Dibujamos al jugador
            self.player_sprite_list.draw()

            # Dibujamos la capa restante
            top = cur_map.scene.name_mapping.get("top")
            if top:
                top.draw()



            for item in map_layers.get("searchable", []):
                arcade.Sprite(
                    filename=":misc:shiny-stars.png",
                    center_x=item.center_x,
                    center_y=item.center_y,
                    scale=0.8,
                ).draw()

            # Draw the player
            # self.player_sprite_list.draw()

            sprites_in_range = []
            if "searchable" in map_layers:
                searchable_sprites = map_layers["searchable"]
                sprites_in_range = arcade.check_for_collision_with_list(
                    self.player_sprite, searchable_sprites
                )
            sprite = None
            for sprites in sprites_in_range:
                sprite = arcade.Sprite("../resources/UIThings/letraE.png", scale = 1.5)
                sprite.center_x = sprites.center_x + 30
                sprite.center_y = sprites.center_y

            if sprite:
                sprite.draw()
                arcade.draw_text("Recoger", sprite.center_x + 10, sprite.center_y - 5, arcade.color.BLACK)

            if self.letraE:
                self.letraE.draw()
                arcade.draw_text("Reclutar", self.letraE.center_x + 10, self.letraE.center_y - 5, arcade.color.BLACK)

            for ally in self.map_list[self.cur_map_name].worldAllyList:
                if ally.checkPlayer():
                    if self.dialogues_active:
                        # arcade.draw_rectangle_filled(self.player_sprite.center_x, self.player_sprite.center_y - 275, self.window.width, 175, arcade.color.LIGHT_CORAL)
                        # self.dialogue_background.center_x = self.player_sprite.center_x
                        # self.dialogue_background.center_y = self.player_sprite.center_y - 450
                        # self.dialogue_background.draw()
                        arcade.draw_rectangle_filled(self.player_sprite.center_x, self.player_sprite.center_y - 300, self.window.width + 200, 250, arcade.color.BURLYWOOD),
                        if not self.buttons_visible:
                            arcade.draw_text("E para pasar los diálogos", self.player_sprite.center_x + 300, self.player_sprite.center_y - 350, arcade.color.BLACK, bold=True)
                        dialogue, item_bool = ally.get_interaction_dialogue()
                        self.dialogues_length = len(dialogue)
                        if type(dialogue) == list:
                                arcade.draw_text(dialogue[self.current_dialog - 1], self.player_sprite.center_x - 550, self.player_sprite.center_y - 225, arcade.color.BLACK, font_size=15, width=self.window.width - 150, align="left", multiline=True)
                        else:
                                arcade.draw_text(dialogue, self.player_sprite.center_x - 550, self.player_sprite.center_y - 225, arcade.color.BLACK)
                        if dialogue == ally.dialogueFullTeam:
                                # x = self.player_sprite.center_x + 200
                                # y = self.player_sprite.center_y - 250
                                # i = 0
                                # j = 1
                                # for names in self.player_sprite.player_team:
                                #     if i == 2:
                                #         y -= 30
                                #         x = self.player_sprite.center_x +  200
                                #         i = -1
                                #     arcade.draw_rectangle_filled(x, y, 40, 20, arcade.color.LIGHT_CYAN)
                                #     arcade.draw_text(str(j), x - 3, y - 5, arcade.color.BLACK)
                                #     x += 50
                                #     i += 1
                                #     j += 1

                                if not self.buttons_visible:
                                    self.main_buttons(self.player_sprite.player_team[1:])
                                    self.buttons_visible = True
        if self.dialogues_active is False:
            self.hide_main_buttons()
            self.buttons_visible = False
        if cur_map.light_layer:
            # Draw the light layer to the screen.
            # This fills the entire screen with the lit version
            # of what we drew into the light layer above.
            if cur_map.properties and "ambient_color" in cur_map.properties:
                ambient_color = cur_map.properties["ambient_color"]
                # ambient_color = (ambient_color.green, ambient_color.blue, ambient_color.alpha, ambient_color.red)
            else:
                ambient_color = arcade.color.WHITE
            cur_map.light_layer.draw(ambient_color=ambient_color)

        if self.other_dialogue:
            self.show_different_dialogue(self.dialogue_list)

        # Use the non-scrolled GUI camera
        self.camera_gui.use()

        # Draw the inventory
        # self.draw_inventory()

        # Draw any message boxes
        if self.message_box:
            self.message_box.on_draw()
        # draw GUI
        self.manager.draw()

    def scroll_to_player(self, speed=constants.CAMERA_SPEED):
        """Manage Scrolling"""

        vector = Vec2(
            self.player_sprite.center_x - self.window.width / 2,
            self.player_sprite.center_y - self.window.height / 2,
        )
        self.camera_sprites.move_to(vector, speed)

    def show_different_dialogue(self, dialogue):
        print(f"coords: {self.player_sprite.center_x} {self.player_sprite.center_y}")
        self.dialogue_background.center_x = self.player_sprite.center_x
        self.dialogue_background.center_y = self.player_sprite.center_y - 450
        self.dialogue_background.draw()
        arcade.draw_text("E para pasar los diálogos", self.player_sprite.center_x + 300,
                         self.player_sprite.center_y - 350, arcade.color.BLACK, bold=True)

        if type(dialogue) == list:
            self.dialogues_length = len(dialogue)
            print("Mostrando diálogo:", dialogue[self.current_dialog])
            arcade.draw_text(dialogue[self.current_dialog], self.player_sprite.center_x - 550, self.player_sprite.center_y - 225, arcade.color.BLACK)

    # Función que creará lo botones cuando se active el diálogo de equipo lleno
    def main_buttons(self, lista_nombres: list):
        self.contenedor.clear()
        self.manager.clear()

        self.fila1 = arcade.gui.UIBoxLayout(vertical=False, space_between=20)
        self.fila2 = arcade.gui.UIBoxLayout(vertical=False, space_between=20)

        ally1_button = arcade.gui.UIFlatButton(text=lista_nombres[0].displayName, width=210)
        self.fila1.add(ally1_button)
        ally1_button.on_click = self.ally1

        ally2_button = arcade.gui.UIFlatButton(text=lista_nombres[1].displayName, width=210)
        self.fila1.add(ally2_button)
        ally2_button.on_click = self.ally2

        ally3_button = arcade.gui.UIFlatButton(text=lista_nombres[2].displayName, width=210)
        self.fila2.add(ally3_button)
        ally3_button.on_click = self.ally3

        # ally4_button = arcade.gui.UIFlatButton(text=lista_nombres[3].displayName, width=150)
        # self.fila2.add(ally4_button)
        # ally4_button.on_click = self.ally4

        self.contenedor.add(self.fila1.with_space_around(bottom=20))
        self.contenedor.add(self.fila2)

        # Aquí guardas el widget para poder eliminarlo luego
        self.main_buttons_widget = arcade.gui.UIAnchorWidget(
            anchor_x="right",
            anchor_y="bottom",
            align_x=-100,
            align_y=10,
            child=self.contenedor
        )
        self.manager.add(self.main_buttons_widget)

    def hide_main_buttons(self):
        if self.main_buttons_widget:
            self.manager.remove(self.main_buttons_widget)
            self.main_buttons_widget = None

    def on_show_view(self):
        # Set background color
        my_map = self.map_list[self.cur_map_name]
        if my_map.background_color:
            arcade.set_background_color(my_map.background_color)

    # Funciones para cada uno de los botones. Cada una selecciona a un aliado a reemplazar
    def ally1(self, event):
        self.button_clicked = True
        self.selected_ally = 1
    def ally2(self, event):
        self.button_clicked = True
        self.selected_ally = 2
    def ally3(self, event):
        self.button_clicked = True
        self.selected_ally = 3
    # def ally4(self, event):
    #     self.button_clicked = True
    #     self.selected_ally = 3

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        """

        self.letraE = None
        # self.allys.clear()
        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        # print(self.player_sprite.allys_on_map)
        # for characters in self.player_sprite.allys_on_map:
        #     self.allys.append(characters)
        #     print(characters.get_interaction_dialogue())

        MOVING_UP = (
            self.up_pressed
            and not self.down_pressed
            and not self.right_pressed
            and not self.left_pressed
        )

        MOVING_DOWN = (
            self.down_pressed
            and not self.up_pressed
            and not self.right_pressed
            and not self.left_pressed
        )

        MOVING_RIGHT = (
            self.right_pressed
            and not self.left_pressed
            and not self.up_pressed
            and not self.down_pressed
        )

        MOVING_LEFT = (
            self.left_pressed
            and not self.right_pressed
            and not self.up_pressed
            and not self.down_pressed
        )

        MOVING_UP_LEFT = (
            self.up_pressed
            and self.left_pressed
            and not self.down_pressed
            and not self.right_pressed
        )

        MOVING_DOWN_LEFT = (
            self.down_pressed
            and self.left_pressed
            and not self.up_pressed
            and not self.right_pressed
        )

        MOVING_UP_RIGHT = (
            self.up_pressed
            and self.right_pressed
            and not self.down_pressed
            and not self.left_pressed
        )

        MOVING_DOWN_RIGHT = (
            self.down_pressed
            and self.right_pressed
            and not self.up_pressed
            and not self.left_pressed
        )
        if self.dialogues_active or self.other_dialogue:
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0
        else:
            if MOVING_UP:
                self.player_sprite.change_y = constants.MOVEMENT_SPEED

            if MOVING_DOWN:
                self.player_sprite.change_y = -constants.MOVEMENT_SPEED

            if MOVING_LEFT:
                self.player_sprite.change_x = -constants.MOVEMENT_SPEED

            if MOVING_RIGHT:
                self.player_sprite.change_x = constants.MOVEMENT_SPEED

            if MOVING_UP_LEFT:
                self.player_sprite.change_y = constants.MOVEMENT_SPEED / 1.5
                self.player_sprite.change_x = -constants.MOVEMENT_SPEED / 1.5

            if MOVING_UP_RIGHT:
                self.player_sprite.change_y = constants.MOVEMENT_SPEED / 1.5
                self.player_sprite.change_x = constants.MOVEMENT_SPEED / 1.5

            if MOVING_DOWN_LEFT:
                self.player_sprite.change_y = -constants.MOVEMENT_SPEED / 1.5
                self.player_sprite.change_x = -constants.MOVEMENT_SPEED / 1.5

            if MOVING_DOWN_RIGHT:
                self.player_sprite.change_y = -constants.MOVEMENT_SPEED / 1.5
                self.player_sprite.change_x = constants.MOVEMENT_SPEED / 1.5


        #print(self.player_sprite.player_team)
        # Si hay slowdown_list en la scene, la velocidad del jugador se reduce al pasar por encima
        slowdown_hit = arcade.check_for_collision_with_list(self.player_sprite, self.my_map.scene["slowdown_list"])
        for things in slowdown_hit:
            self.player_sprite.change_y *= 0.8
            self.player_sprite.change_x *= 0.8

        self.ally_names = ""
        for ally in self.map_list[self.cur_map_name].worldAllyList:
            if ally.checkPlayer():
                self.letraE = arcade.Sprite("../resources/UIThings/letraE.png", scale = 1.5)
                self.letraE.center_x = ally.center_x + 30
                self.letraE.center_y = ally.center_y
                dialogue, item_bool = ally.get_interaction_dialogue()
                if dialogue == ally.dialogueFullTeam and self.dialogues_active:
                    if self.selected_ally != None:
                        # Guardamos el aliado a reemplazar
                        old_ally = self.player_sprite.player_team[self.selected_ally]
                        # Quitamos del equipo del jugador al aliado seleccionado
                        self.player_sprite.player_team.remove(self.player_sprite.player_team[self.selected_ally])
                        # Añadimos al equipo del jugador al aliado con el que estabamos dialogando
                        self.player_sprite.player_team.append(ally.aliadoBatalla)
                        # Desactivamos los dialogos
                        self.dialogues_active = False
                        self.current_dialog = 0
                        sheet_name = old_ally.sheetName
                        # arcade.play_sound(self.pergamino_sound, volume=1)
                        # Creamos otro WorldAlly con la información del battleAlly quitado del player_team
                        print(sheet_name)
                        key = ""
                        for i in self.team:
                            if self.team[i]['sheet_name'] in sheet_name:
                                key = i
                                requirementItem = self.team[i]['requirementItemKey']
                                requirementItemName = self.item
                        if key != "" and old_ally:
                            self.old_ally_battle = WorldAlly(sheet_name, self.my_map.scene, self.player_sprite, old_ally, self.item_dictionary[self.team[key]['requirementItemKey']]['name'],
                                                             self.team[key]["dialogueNoItem"], self.team[key]["dialogueWithItem"])
                            self.old_ally_battle.center_x = self.player_sprite.center_x
                            self.old_ally_battle.center_y = self.player_sprite.center_y
                            # Creamos otro item
                            self.item_nuevo = WorldItem(f":items:{self.item_dictionary[self.team[key]['requirementItemKey']]['sheet_name']}", self.team[key]['requirementItemKey'])
                            self.item_nuevo.center_x = self.player_sprite.center_x + 50
                            self.item_nuevo.center_y = self.player_sprite.center_y
                            self.my_map.scene.add_sprite("searchable", self.item_nuevo)
                            self.my_map.scene.add_sprite("characters", self.old_ally_battle)
                            self.my_map.worldAllyList.append(self.old_ally_battle)
                            self.my_map.worldItemList.append(self.item_nuevo)
                            # quitar al aliado del mapa
                            ally.remove_from_sprite_lists()
                            # quitar su item del inventario
                            for item in self.player_sprite.inventory:
                                if item['name'] == ally.requirementItemName:
                                    self.player_sprite.inventory.remove(item)
                            self.selected_ally = None



        self.team_sprites = arcade.SpriteList()
        x = 200
        for ally in self.player_sprite.player_team:
            sprite = arcade.Sprite(ally.sheetName)
            sprite.center_x = x
            sprite.center_y = 200
            self.team_sprites.append(sprite)
            x += 50
        self.y = 250
        arcade.set_background_color(arcade.color.ALMOND)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
        self.team_names = self.window.views["game"].player_sprite.player_team
        self.player_team_sheets = arcade.SpriteList()
        self.characters = []

        self.x = self.player_sprite.center_x
        for character in self.player_sprite.player_team:
            if character in self.team and 'sheet_name' in self.team[character]:
                sheet_name = self.team[character]['sheet_name']

                # Cargar las texturas desde el spritesheet
                textures = arcade.load_spritesheet(
                    f":characters:{sheet_name}",
                    sprite_width=64,
                    sprite_height=64,
                    columns=9,
                    count=36
                )

                # Crear un Sprite y asignarle una textura
                sprite = Sprite()
                sprite.texture = textures[9]
                sprite.center_x = self.x
                sprite.center_y = self.player_sprite.center_y - 275
                self.x += 50
                self.characters.append(character)
                self.player_team_sheets.append(sprite)
        #print(self.selected_ally)
        # team = SpriteList()
        # for character in self.team_sprites:
        #     team.append(character)
        # self.allys_colliding = arcade.check_for_collision_with_list(self.player_sprite, team)
        # if self.allys_colliding:
        #     self.dialogues_active = True

        # Call update to move the sprite
        self.physics_engine.update()

        # Update player animation
        self.player_sprite_list.on_update(delta_time)

        self.player_light.position = self.player_sprite.position

        # Update the characters
        try:
            self.map_list[self.cur_map_name].scene["characters"].on_update(delta_time)
        except KeyError:
            # no characters on map
            pass

        # --- Manage doors ---
        map_layers = self.map_list[self.cur_map_name].map_layers

        # Is there as layer named 'doors'?
        if "doors" in map_layers:
            # Did we hit a door?
            doors_hit = arcade.check_for_collision_with_list(
                self.player_sprite, map_layers["doors"]
            )
            # We did!
            if len(doors_hit) > 0:
                try:
                    # Grab the info we need
                    map_name = doors_hit[0].properties["map_name"]
                    start_x = doors_hit[0].properties["start_x"]
                    start_y = doors_hit[0].properties["start_y"]
                    wipe = doors_hit[0].properties["wipePreviousMaps"]
                except KeyError:
                    raise KeyError(
                        "Door objects must have 'map_name', 'start_x', 'start_y' and 'wipePreviousMaps' properties defined."
                    )

                # Swap to the new map
                self.switch_map(map_name, start_x, start_y, wipe)
            else:
                # We didn't hit a door, scroll normally
                self.scroll_to_player()
        else:
            # No doors, scroll normally
            self.scroll_to_player()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if self.message_box:
            self.message_box.on_key_press(key, modifiers)
            return

        if key in constants.KEY_UP:
            self.up_pressed = True
        elif key in constants.KEY_DOWN:
            self.down_pressed = True
        elif key in constants.KEY_LEFT:
            self.left_pressed = True
        elif key in constants.KEY_RIGHT:
            self.right_pressed = True
        elif key in constants.INVENTORY:
            self.window.show_view(self.window.views["inventory"])
        elif key == arcade.key.ESCAPE:
            if self.dialogues_active or self.other_dialogue:
                self.dialogues_active = False
                self.other_dialogue = False
                self.current_dialog = 0
            else:
                self.window.show_view(self.window.views["main_menu"])
        elif key == arcade.key.P:
            self.window.show_view(self.window.views["in_battle"])
        elif key == arcade.key.M:
            self.window.show_view(self.window.views["menu"])
        elif key in constants.SEARCH:
            self.ally_colliding = None
            for ally in self.map_list[self.cur_map_name].worldAllyList:
                for item in self.player_sprite.inventory:
                    if self.dialogues_active and ally.requirementItemName == item['name'] and ally.checkPlayer() and not self.buttons_visible and self.current_dialog == self.dialogues_length:
                        self.ally_colliding = ally
                        ally.remove_from_sprite_lists()
                        self.player_sprite.inventory.remove(item)
                        self.dialogues_active = False
                        self.current_dialog = 0
                        # arcade.play_sound(self.pergamino_sound, volume=1)
            if self.ally_colliding and len(self.player_sprite.player_team) < 4:
                self.player_sprite.player_team.append(self.ally_colliding.aliadoBatalla)
            if self.buttons_visible:
                self.dialogues_active = False
            if self.other_dialogue:
                if self.current_dialog == self.dialogues_length - 1:
                    self.current_dialog = 0
                    self.other_dialogue = False
                else:
                    self.other_dialogue = True
                    self.current_dialog += 1
            self.search()
        #DEBUG -----
        elif key == arcade.key.B:
            self.dialogue_list = ["dial1", "dial2", "dial3", "dial4"]
            self.other_dialogue = True if not self.other_dialogue else False

        elif key == arcade.key.Z:
            self.player_sprite.debugAnim()
        elif key == arcade.key.X:
            self.save_game()
        #DEBUG -----
        elif key == arcade.key.L:
            cur_map = self.map_list[self.cur_map_name]
            if self.player_light in cur_map.light_layer:
                cur_map.light_layer.remove(self.player_light)
            else:
                cur_map.light_layer.add(self.player_light)
        elif key == arcade.key.G:  # G
            # toggle debug
            self.debug = True if not self.debug else False
            if self.debug:
                self.enable_debug_menu()
            else:
                self.disable_debug_menu()

    def close_message_box(self):
        self.message_box = None

    def search(self):
        """Search for things"""
        for ally in self.map_list[self.cur_map_name].worldAllyList:
            if ally.checkPlayer():
                if self.dialogues_active and self.current_dialog == self.dialogues_length:
                    self.dialogues_active = False
                    self.current_dialog = 0
                    # arcade.play_sound(self.pergamino_sound, volume=1)

                else:
                    self.dialogues_active = True
                    self.current_dialog += 1

                    # arcade.play_sound(self.pergamino_sound, volume=1)
        self.allys_colliding.clear()
        map_layers = self.map_list[self.cur_map_name].map_layers
        print(map_layers)

        if "searchable" not in map_layers:
            print(f"No searchable sprites on {self.cur_map_name} map layer.")
            return
        searchable_sprites = map_layers["searchable"]
        # if self.item_nuevo and not self.added:
        #     searchable_sprites.append(self.item_nuevo)
        #     self.added = True
        sprites_in_range = arcade.check_for_collision_with_list(
            self.player_sprite, searchable_sprites
        )
        print(f"Found {len(sprites_in_range)} searchable sprite(s) in range.")
        # Funcion para Sprites puestos en el nivel por medio de puntos.
        for sprite in sprites_in_range:
            if sprite.__class__ == WorldItem:
                lookup_item = self.item_dictionary[sprite.itemKey]

                self.message_box = MessageBox(
                    self, f"Found: {lookup_item['name']}"
                )
                sprite.remove_from_sprite_lists()
                self.player_sprite.inventory.append(lookup_item)
                print(self.player_sprite.inventory)
                continue
            print(self.map_list[self.cur_map_name].worldAllyList)
        for character in self.map_list[self.cur_map_name].worldAllyList:
            # self.dialogue, self.item = character.get_interaction_dialogue()
            print(character)
    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key in constants.KEY_UP:
            self.up_pressed = False
        elif key in constants.KEY_DOWN:
            self.down_pressed = False
        elif key in constants.KEY_LEFT:
            self.left_pressed = False
        elif key in constants.KEY_RIGHT:
            self.right_pressed = False

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """Called whenever the mouse moves."""
        self.manager.on_mouse_motion(x, y, delta_x, delta_y)

    def on_mouse_press(self, x, y, button, key_modifiers):
        """Called when the user presses a mouse button."""
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.player_sprite.destination_point = x, y
        for i, sprite in enumerate(self.player_team_sheets):
            if sprite.collides_with_point((x, y)):
                print(123445643213453323)
        # self.manager.on_mouse_press(x, y, button, key_modifiers)


    def on_mouse_release(self, x, y, button, key_modifiers):
        """Called when a user releases a mouse button."""
        pass

    def on_resize(self, width, height):
        """
        Resize window
        Handle the user grabbing the edge and resizing the window.
        """
        self.camera_sprites.resize(width, height)
        self.camera_gui.resize(width, height)
        cur_map = self.map_list[self.cur_map_name]
        if cur_map.light_layer:
            cur_map.light_layer.resize(width, height)

    def inventory_add(self, object_name):
        with open("../resources/data/item_dictionary.json", "r") as file:
            items = json.load(file)
        for item in items.values():
                if object_name in items.keys():
                    self.player_sprite.inventory.append(items[object_name])
                else:
                    with open("../resources/data/worldItem_dictionary.json", "r") as file:
                        items = json.load(file)
                    if object_name == item["name"]:
                        self.player_sprite.inventory.append(item)
    def save_game(self):
        print("Guardando partida")
        #USAR EVENTUALMENTE PARA GUARDAR SAVEFILES DISTINTOS
        date = datetime.datetime.now().strftime("%d%m%Y%H%M%S")

        saveDict = {}
        saveDict["currentMapName"] = self.cur_map_name

        map_height = self.my_map.map_size[1]
        x_relativePosition= self.player_sprite.center_x / constants.MAP_TILE_SIZE #* constants.SPRITE_SIZE + constants.SPRITE_SIZE / 2
        y_relativePosition = map_height - ((map_height + self.player_sprite.center_y) / (constants.MAP_TILE_SIZE)) + 2 #* constants.SPRITE_SIZE - constants.SPRITE_SIZE / 2

        saveDict["playerPosition"] = (x_relativePosition, y_relativePosition)

        #Informacion individual del jugador.
        playerItems = []
        for item in self.player_sprite.inventory:
            playerItems.append({item["name"] : item["amount"]})
        saveDict["playerInventory"] = playerItems

        playerAllies = []
        for ally in self.player_sprite.player_team:
            playerAllies.append({ally.characterKey : ally.currentHealth})
        saveDict["playerTeam"] = playerAllies

        #Informacion de los mapas.
        saveDict["maps"] = {}
        print(self.map_list)
        for mapKey in list(self.map_list.keys()):
            saveDict["maps"][mapKey] = {}

            saveDict["maps"][mapKey]["worldAllies"] = []
            for worldAlly in self.map_list[mapKey].worldAllyList:
                print(mapKey)
                print(worldAlly.aliadoBatalla.characterKey)
                saveDict["maps"][mapKey]["worldAllies"].append({worldAlly.aliadoBatalla.characterKey : (worldAlly.center_x, worldAlly.center_y)})

            saveDict["maps"][mapKey]["worldEnemies"] = []
            for worldEnemy in self.map_list[mapKey].worldEnemyList:
                enemyDict = {}
                enemyDict["sheetName"] = worldEnemy.sheetName
                enemyDict["position"] = worldEnemy.position
                enemyDict["battleEnemies"] = worldEnemy.enemigos_batalla
                enemyDict["speed"] = worldEnemy.speed
                enemyDict["detectionRadius"] = worldEnemy.radio_deteccion

                saveDict["maps"][mapKey]["worldEnemies"].append(enemyDict)

            saveDict["maps"][mapKey]["worldItems"] = []
            for worldItem in self.map_list[mapKey].worldItemList:
                saveDict["maps"][mapKey]["worldItems"].append({worldItem.itemKey : (worldItem.center_x, worldItem.center_y)})
        with open(f"saveGame{date}.json", "w") as f:
            json.dump(saveDict,f, indent=4)

        print("Terminado")