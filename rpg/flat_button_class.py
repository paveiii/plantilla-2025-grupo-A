import arcade.gui

class FlatButtonFactory(arcade.View):
    def __init__(self, manager: arcade.gui.UIManager, option):
        super().__init__()
        self.manager = manager
        self.option = option


    def create_button(self, text: str, width = 150, height = 45, function = None):
        button = arcade.gui.UIFlatButton(text=text, width=width, height=height)
        button.on_click = function
        return button




