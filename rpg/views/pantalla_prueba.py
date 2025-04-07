import arcade
import arcade.gui
from rpg.sprites.character_sprite import CharacterSprite, SPRITE_INFO, Direction
from rpg.constants import SPRITE_SIZE


class PantallaPrueba(arcade.View):
    def __init__(self):
        super().__init__()

        self.manager = arcade.gui.UIManager()
        self.activated = False

        self.player_sprites = arcade.SpriteList()
        self.enemy_sprites = arcade.SpriteList()

    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(arcade.color.GREEN)
        self.setup_team(":characters:Female/Female 18-4.png", 200, 200)
        self.setup_enemies(":characters:Female/Female 18-4.png", 1000, 200)

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        """
        Method that redraws the UI buttons each time we call the pause menu. See game_view.py for more.
        input: None
        output: None
        """
        self.clear()
        self.manager.draw()

        self.player_sprites.draw()
        self.enemy_sprites.draw()

    def setup_team(self, sheet_name, x, y):
        self.character_sprite = CharacterSprite(sheet_name)

        self.character_sprite.center_x = x
        self.character_sprite.center_y = y

        self.character_sprite.textures = arcade.load_spritesheet(
            sheet_name,
            sprite_width = SPRITE_SIZE + 32,
            sprite_height = SPRITE_SIZE + 32,
            columns = 3,
            count = 12,
        )
        start_index = SPRITE_INFO[Direction.RIGHT][0]
        self.character_sprite.texture = self.character_sprite.textures[start_index]

        self.player_sprites.append(self.character_sprite)

    def setup_enemies(self, sheet_name, x, y):
        self.character_sprite = CharacterSprite(sheet_name)

        self. character_sprite.center_x = x
        self.character_sprite.center_y = y

        self.character_sprite.textures = arcade.load_spritesheet(
            sheet_name,
            sprite_width = SPRITE_SIZE + 30,
            sprite_height= SPRITE_SIZE + 30,
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
            print("show game view")
            self.window.show_view(self.window.views["game"])

        if key == arcade.key.ENTER:
            print("battle pause menu")
            self.window.show_view(self.window.views["battle_pause"])