import arcade
import arcade.gui

import rpg.views.loading_view as l
import rpg.views.load_game_view as g

class MenuView(arcade.View):
    def __init__(self):
        super().__init__()

        # --- Required for all code that uses UI element, a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        self.window.views["load_game"] = g.LoadGameView()

        start_game_button = arcade.gui.UIFlatButton(text="Start", width=200)
        self.v_box.add(start_game_button.with_space_around(bottom=20))
        start_game_button.on_click = self.on_click_start_game_button

        load_game_button = arcade.gui.UIFlatButton(text="Load Game", width=200)
        self.v_box.add(load_game_button.with_space_around(bottom=20))
        load_game_button.on_click = self.on_click_load_game_button

        exit_button = arcade.gui.UIFlatButton(text="Exit", width=200)
        self.v_box.add(exit_button.with_space_around(bottom=20))
        exit_button.on_click = self.on_click_exit_button

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x", anchor_y="center_y", child=self.v_box
            )
        )


    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(arcade.color.ALMOND)


    def on_hide_view(self):
        self.manager.disable()

    def setup(self):
        pass

    def on_draw(self):
        """
        Method that redraws the UI buttons each time we call the pause menu. See game_view.py for more.
        input: None
        output: None
        """
        self.clear()
        self.manager.draw()

    # call back methods for buttons:
    def on_click_start_game_button(self, event):
        print("starting game")
        self.window.views["loading_view"] = l.LoadingView(None)
        self.window.show_view(self.window.views["loading_view"])

    def on_click_exit_button(self, event):
        print("quitting")
        self.window.close()

    def on_click_load_game_button(self, event):
        print("load game screen")
        self.window.views["load_game"].setup()
        self.window.show_view(self.window.views["load_game"])

    # def on_click_settings(self, event):
    #     print("show settings view")
    #     self.window.show_view(self.window.views["settings"])

    # def on_click_new_game(self, event):
    #     print("restart game")
    #     self.window.views["game"].setup()
    #     self.window.show_view(self.window.views["game"])

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            print("quitting")
            self.window.close()

    def on_update(self, delta_time: float):
        pass
