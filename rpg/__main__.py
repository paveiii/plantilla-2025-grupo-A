"""
Python Arcade Community RPG

An open-source RPG
"""

import arcade

from rpg.constants import SCREEN_HEIGHT, SCREEN_TITLE, SCREEN_WIDTH
from rpg.views import LoadingView
from rpg.views.menu_view import MenuView


class MyWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
        self.views = {}

        #Permite cargar recursos facilmente usando una direccion como base de la busqueda.
        # Ej: PlayerSprite(":characters:Female/Female 19-1.png")
        arcade.resources.add_resource_handle("characters", "../resources/characters")
        arcade.resources.add_resource_handle("maps", "../resources/maps")
        arcade.resources.add_resource_handle("data", "../resources/data")
        arcade.resources.add_resource_handle("sounds", "../resources/sounds")
        arcade.resources.add_resource_handle("misc", "../resources/misc")
        arcade.resources.add_resource_handle("items", "../resources/items")


def main():
    """Main method"""
    window = MyWindow()
    window.center_window()
    start_view = MenuView()
    start_view.setup()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
