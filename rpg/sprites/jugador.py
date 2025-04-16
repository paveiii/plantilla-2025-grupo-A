import arcade

from rpg.sprites.character_sprite import CharacterSprite


class Jugador(CharacterSprite):
    def __init__(self, sheet_name, vida_max=100):
        super().__init__(sheet_name)
        self.vida_max = vida_max
        self.vida_actual = vida_max

    def on_draw(self):
        super().draw()
        bar_width = 40
        bar_height = 6
        bar_x = self.center_x
        bar_y = self.top + 10

        vida_ratio = self.vida_actual / self.vida_max

        arcade.draw_rectangle_filled(bar_x, bar_y, bar_width, bar_height, arcade.color.ASH_GREY)

        if vida_ratio > 0.5:
            color = arcade.color.GREEN
        elif vida_ratio > 0.25:
            color = arcade.color.ORANGE
        else:
            color = arcade.color.RED

        arcade.draw_rectangle_filled(
            bar_x - (bar_width * (1 - vida_ratio)) / 2,  # ajuste para recortar por la izquierda
            bar_y,
            bar_width * vida_ratio,
            bar_height,
            color
        )

        arcade.draw_rectangle_outline(bar_x, bar_y, bar_width, bar_height, arcade.color.BLACK, 1)