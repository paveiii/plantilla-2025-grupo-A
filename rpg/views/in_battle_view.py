from time import sleep

import arcade
import arcade.gui
from rpg.sprites.character_sprite import CharacterSprite, SPRITE_INFO, Direction
from rpg.constants import SPRITE_SIZE, SCREEN_WIDTH
from rpg.views.game_view import GameView


class InBattleView(arcade.View):
    def __init__(self):
        super().__init__()
        self.action = "menu"

        self.player_sprites = arcade.SpriteList()
        self.enemy_sprites = arcade.SpriteList()

        self.manager = arcade.gui.UIManager()
        self.activated = False

        self.fila1 = arcade.gui.UIBoxLayout(vertical = False, space_between = 20)
        self.fila2 = arcade.gui.UIBoxLayout(vertical = False, space_between = 20)

        attack_button = arcade.gui.UIFlatButton(text = "Attack", width = 200)
        self.fila1.add(attack_button)
        attack_button.on_click = self.on_click_attack

        skill_button = arcade.gui.UIFlatButton(text = "Skill", width = 200)
        self.fila1.add(skill_button)
        skill_button.on_click = self.on_click_skill

        item_button = arcade.gui.UIFlatButton(text = "Item", width = 200)
        self.fila2.add(item_button)
        item_button.on_click = self.on_click_item

        rest_button = arcade.gui.UIFlatButton(text = "Rest", width = 200)
        self.fila2.add(rest_button)
        rest_button.on_click = self.on_click_rest

        self.contenedor = arcade.gui.UIBoxLayout()
        self.contenedor.add(self.fila1.with_space_around(bottom = 20))
        self.contenedor.add(self.fila2)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x = "center",
                anchor_y = "bottom",
                align_y = 35,
                child = self.contenedor
            )
        )

    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(arcade.color.GREEN)

        self.setup_team(":characters:Female/Female 18-4.png", 345, 345)
        self.setup_team(":characters:Male/Male 01-1.png", 180, 430)
        self.setup_team(":characters:Male/Male 08-1.png", 280, 565)
        self.setup_team(":characters:Soldier/Soldier 03-1.png", 430, 490)
        self.setup_enemies(":characters:Boss/Boss 01.png", 1000, 430)

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        """
        Method that redraws the UI buttons each time we call the pause menu. See game_view.py for more.
        input: None
        output: None
        """
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



        self.player_sprites.draw()
        self.enemy_sprites.draw()

        if self.action == "menu":
            self.manager.draw()
            self.manager.enable()


    def on_click_attack(self, event):
        self.on_hide_view()
        self.action = "attack"

    def on_click_skill(self, event):
        self.on_hide_view()
        self.action = "skill"

    def on_click_item(self, event):
        self.on_hide_view()
        self.action = "item"

    def on_click_rest(self, event):
        self.on_hide_view()
        self.action = "rest"


    def setup_team(self, sheet_name, x, y):
        self.character_sprite = CharacterSprite(sheet_name)

        self.character_sprite.center_x = x
        self.character_sprite.center_y = y

        self.character_sprite.scale = 2

        self.character_sprite.textures = arcade.load_spritesheet(
            sheet_name,
            sprite_width = SPRITE_SIZE,
            sprite_height = SPRITE_SIZE,
            columns = 3,
            count = 12,
        )
        start_index = SPRITE_INFO[Direction.RIGHT][0]
        self.character_sprite.texture = self.character_sprite.textures[start_index]

        self.player_sprites.append(self.character_sprite)

    def setup_enemies(self, sheet_name, x, y):
        self.character_sprite = CharacterSprite(sheet_name)
        self.character_sprite.scale = 2

        self. character_sprite.center_x = x
        self.character_sprite.center_y = y

        self.character_sprite.textures = arcade.load_spritesheet(
            sheet_name,
            sprite_width = 96,
            sprite_height= 96,
            columns = 3,
            count = 12,
        )
        start_index = SPRITE_INFO[Direction.LEFT][0]
        self.character_sprite.texture = self.character_sprite.textures[start_index]

        self.enemy_sprites.append(self.character_sprite)


    def on_key_press(self, key, _modifiers):

        if key == arcade.key.P and self.activated == False:
            print("pantalla de prueba")
            self.window.show_view(self.window.views["prueba"])
            self.activated = True

        if key == arcade.key.P and self.activated == True:
            print("show game view")
            self.window.show_view(self.window.views["game"])

        if key == arcade.key.ESCAPE:
            self.action = "menu"

        if key == arcade.key.ENTER:
            print("battle pause menu")
            self.window.show_view(self.window.views["battle_pause"])

    def get_width(self):
        window_size = self.window.get_size()
        current_width = window_size[0]
        return current_width

    def get_height(self):
        window_size = self.window.get_size()
        current_height = window_size[1]
        return current_height