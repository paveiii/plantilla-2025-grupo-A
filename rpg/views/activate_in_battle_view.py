import arcade

class ActivateInBattleView(arcade.View):
    def __init__(self, worldEnemy):
        super().__init__()
        battleView = self.window.views["in_battle"]
        if(battleView.activated == False):
            self.window.views["in_battle"].enemy_collision_list = worldEnemy.enemigos_batalla
            worldEnemy.remove_from_sprite_lists()
            self.window.show_view(self.window.views["in_battle"])
