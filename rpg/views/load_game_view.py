import json
import os
from os.path import isfile, join

import rpg.views.loading_view as l

import arcade
import arcade.gui

# from rpg.views import LoadingView
from rpg.views.menu_view import MenuView


class LoadGameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.contenedor = arcade.gui.UIBoxLayout()
        arcade.set_background_color(arcade.color.ALMOND)

        # --- Required for all code that uses UI element, a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

    def on_draw(self):
        arcade.start_render()
        self.manager.draw()
        arcade.draw_text(
            "Load game",
            self.window.width / 2,
            self.window.height - 50,
            arcade.color.ALLOY_ORANGE,
            44,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width,
        )

    def setup(self):
        saveFilePath = "../rpg"
        savefiles = []

        for f in os.listdir(saveFilePath):
            if isfile(join(saveFilePath, f)) and f.endswith(".json"):
                savefiles.append(f)

        botones_por_fila = 3
        fila = arcade.gui.UIBoxLayout(vertical=False, space_between=10)
        for i in range(len(savefiles)):
            newSaveButton = SaveFileButton(savefiles[i], self)
            fila.add(newSaveButton)

            #Añadir la fila cuando se completa o estamos en el último botón
            if (i + 1) % botones_por_fila == 0 or i == len(savefiles) - 1:
                self.contenedor.add(fila.with_space_around(bottom=20))
                fila = arcade.gui.UIBoxLayout(vertical=False, space_between=20)
        self.contenedor.add(fila.with_space_around(bottom=20))
        # Agregar los widgets a la vista
        widgets = arcade.gui.UIAnchorWidget(
                anchor_x="center",
                anchor_y="center",
                align_y=0,
                child=self.contenedor
            )
        self.manager.add(widgets)

    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(arcade.color.ALMOND)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_hide_view(self):
        self.manager.disable()

    def on_key_press(self, symbol: int, modifiers: int):
        close_inputs = [
            arcade.key.ESCAPE,
        ]
        if symbol in close_inputs:
            self.window.show_view(self.window.views["menu"])
    def on_update(self, delta_time: float):
        self.window.views["menu"] = MenuView()

class SaveFileButton(arcade.gui.UIFlatButton):
    def __init__(self, savefile, view):
        self.savefile = savefile
        self.loadView = view

        displayText = savefile[:-5]
        super().__init__(text=displayText, width=400, height=45)


    def on_click(self, event: arcade.gui.UIOnClickEvent):
        self.loadView.window.views["loading_view"] = l.LoadingView(self.savefile)
        self.loadView.window.show_view(self.loadView.window.views["loading_view"])
