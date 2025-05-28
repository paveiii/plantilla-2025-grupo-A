import arcade

class ActivateInBattleView(arcade.View):
    def __init__(self, enemy_list):
        super().__init__()
        battleView = self.window.views["in_battle"]
        if(battleView.activated == False):
            self.window.views["in_battle"].enemy_collision_list = enemy_list
            self.window.show_view(self.window.views["in_battle"])
