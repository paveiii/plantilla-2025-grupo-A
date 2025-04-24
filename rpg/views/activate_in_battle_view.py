import arcade


class ActivateInBattleView(arcade.View):
    def __init__(self):
        super().__init__()
        self.window.show_view(self.window.views["in_battle"])
