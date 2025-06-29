"""
Python Arcade Community RPG

An open-source RPG
"""
import builtins

original_import = builtins.__import__

def blocking_import(name, globals=None, locals=None, fromlist=(), level=0):
    if "newton" in name.lower() or "cradle" in name.lower():
        raise ImportError(f"[BLOQUEADO] Intento de importar módulo prohibido: {name}")
    return original_import(name, globals, locals, fromlist, level)

builtins.__import__ = blocking_import

import subprocess
import sys

try:
    import pygame
except ImportError:
    print("Pygame no está instalado. Instalando...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
    import pygame  # intentar importar nuevamente después de la instalación

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
