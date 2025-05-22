import arcade
import arcade.gui

from rpg.views.menu_view import MenuView


class LoadGameView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.ALMOND)

        # --- Required for all code that uses UI element, a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        for i in range(12):
            newButton = SaveFileButton(text=str(i), width=500, height=45)
            self.v_box.add(newButton)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x", anchor_y="center_y", align_y=-50, child=self.v_box
            )
        )

    def on_draw(self):
        arcade.start_render()
        self.manager.draw()
        arcade.draw_text(
            "Load game",
            self.window.width / 2,
            self.window.height - 50,
            arcade.color.ALLOY_ORANGE,
            44,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width,
        )

    def setup(self):
        pass

    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(arcade.color.ALMOND)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_hide_view(self):
        self.manager.disable()

    def on_key_press(self, symbol: int, modifiers: int):
        close_inputs = [
            arcade.key.ESCAPE,
        ]
        if symbol in close_inputs:
            self.window.show_view(self.window.views["menu"])
    def on_update(self, delta_time: float):
        self.window.views["menu"] = MenuView()

class SaveFileButton(arcade.gui.UIFlatButton):

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        print(self.text)
