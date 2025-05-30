import arcade
import arcade.gui


class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = None

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Crear el botón INICIO
        self.botonInicio = arcade.gui.UIFlatButton(text="INICIO", width=150)
        self.botonInicio.on_click = self.on_click_inicio

        # Crear widget ancla para el botón abajo a la derecha con margen
        anchor = arcade.gui.UIAnchorWidget(
            child=self.botonInicio,
            anchor_x="right",
            anchor_y="bottom",
            align_x=-20,  # 20 px desde la derecha
            align_y=20    # 20 px desde abajo
        )

        # Añadir el widget ancla al manager
        self.manager.add(anchor)

    def on_draw(self):
        self.clear()
        arcade.start_render()
        if self.background:
            self.background.draw()
        self.manager.draw()

    def setup(self):
        self.background = arcade.Sprite("../resources/UIThings/GameOver.png", scale=0.85)
        self.background.center_x = 650
        self.background.center_y = 350
        self.background.height = self.background.height - 125

    def on_click_inicio(self, event):
        self.window.show_view((self.window.views["menu"]))