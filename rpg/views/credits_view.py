import arcade

import rpg.constants


class CreditsView(arcade.View):
    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.DARK_BLUE)
        self.scroll_speed = 1.5
        self.text = (
            "Créditos del juego\n\n"
            "Jefatura de proyecto:\n"
            "Pável David Tabata Rodríguez\n\n"
            "Programación:\n"
            "Pável David Tabata Rodríguez\n"
            "Rubén Dobre\n"
            "Samuel García de Dios\n"
            "Daniel Guillén Ruiz\n\n"
            "Diseño gráfico:\n"
            "Beatriz Arribas Schudeck\n"
            "Pablo Álvaro Peña Sánchez\n"
            "Daniel Guillén Ruiz\n\n"
            "Diseño de niveles:\n"
            "Pablo Álvaro Peña Sánchez\n"
            "Samuel García de Dios\n"
            "Daniel Guillén Ruiz\n\n"
            "Pruebas:\n"
            "Pável David Tabata Rodríguez\n"
            "Beatriz Arribas Schudeck\n"
            "Pablo Álvaro Peña Sánchez\n"
            "Rubén Dobre\n"
            "Samuel García de Dios\n"
            "Daniel Guillén Ruiz\n\n"
            "Gracias por jugar\n"
            "<3"
        )
        self.cont = 0
        for i in self.text:
            if i == "\n":
                self.cont += 1

        self.text_height = 1600
        self.text_y = -self.cont * 24 + self.window.height - 50
    def on_draw(self):
        self.clear()
        arcade.start_render()
        arcade.set_background_color(arcade.color.DARK_BLUE)


        # Dibuja el texto centrado y multilínea
        arcade.draw_text(
            self.text,
            self.window.width / 2,
            self.text_y,
            arcade.color.WHITE,
            font_size=24,
            anchor_x="center",
            align="center",
            multiline=True,
            width=600
        )

    def on_update(self, delta_time):
        self.text_y += self.scroll_speed

        if self.text_y > self.window.height + 2*self.cont*24:
            self.window.show_view(self.window.views["menu"])
            # view = self.window.views["MenuView"]
            # view.setup()
            # self.window.show_view(view)

    def setup(self):
        self.text_y = -self.cont * 24 + self.window.height - 50

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.window.views["game"])
