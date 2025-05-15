"""
Loading screen
"""
import arcade

from rpg import constants
from rpg.draw_bar import draw_bar
from rpg.load_game_map import load_maps
from rpg.sprites.player_sprite import PlayerSprite
from rpg.views.battle_view import BattleView
from rpg.views.dialogues_view import DialogueView
from rpg.views.game_view import GameView
from rpg.views.inventory_view import InventoryView
from rpg.views.load_game_view import LoadGameView
from rpg.views.main_menu_view import MainMenuView
from rpg.views.in_battle_view import InBattleView
from rpg.views.settings_view import SettingsView
from rpg.views.menu_view import MenuView
from rpg.views.dialogues_view import DialogueView


class LoadingView(arcade.View):
    def __init__(self):
        super().__init__()
        self.started = False
        self.progress = 0
        self.map_list = None
        arcade.set_background_color(arcade.color.ALMOND)
        self.player_sprite = PlayerSprite(":characters:" + constants.PLAYER_SPRITE_PATH)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(
            "Loading...",
            self.window.width / 2,
            self.window.height / 2,
            arcade.color.ALLOY_ORANGE,
            44,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width,
        )
        self.started = True
        draw_bar(
            current_amount=self.progress,
            max_amount=100,
            center_x=self.window.width / 2,
            center_y=20,
            width=self.window.width,
            height=10,
            color_a=arcade.color.BLACK,
            color_b=arcade.color.WHITE,
        )

    def setup(self):
        pass

    def on_update(self, delta_time: float):
        # Dictionary to hold all our maps
        if self.started:
            done, self.progress, self.map_list = load_maps(self.player_sprite)
            if done:
                self.window.views["game"] = GameView(self.map_list, self.player_sprite)
                self.window.views["game"].setup()
                self.window.views["inventory"] = InventoryView()
                self.window.views["inventory"].setup()
                self.window.views["main_menu"] = MainMenuView()
                self.window.views["settings"] = SettingsView()
                self.window.views["settings"].setup()
                self.window.views["battle"] = BattleView()
                self.window.views["battle"].setup()
                self.window.views["in_battle"] = InBattleView()
                self.window.views["menu"] = MenuView()
                self.window.views["load_game"] = LoadGameView()

                self.window.show_view(self.window.views["game"])
