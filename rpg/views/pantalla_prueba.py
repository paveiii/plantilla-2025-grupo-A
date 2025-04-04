import arcade
import arcade.gui

class PantallaPrueba(arcade.View):
    def __init__(self):
        super().__init__()

        self.manager = arcade.gui.UIManager()
        self.activated = False

    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(arcade.color.GREEN)

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