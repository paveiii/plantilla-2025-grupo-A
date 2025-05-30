import arcade


class CreditsView(arcade.View):
    def __init__(self):
        super().__init__()
        self.temporizador = 0
        arcade.set_background_color(arcade.color.BLUE)
        self.x = 0
        self.y = self.window.height
        self.text = "asdknlkjamskj ajdnclkasjxópqljsd jsadnieñaslo  qlkjijmxkxiqo ajkhcukkajxo akj,cmnahkcnñiola kajhsoialsjx uiahjdajksasdsdasdas"



    def on_draw(self):
        self.clear()
        arcade.start_render()
        self.temporizador += 1
        arcade.draw_text(self.text, self.window.width/2 - 50, self.y, arcade.color.BLACK, multiline=True, width=200)
        if self.temporizador == 2:
            self.y -= 1
            self.temporizador = 0

    def setup(self):
        pass
