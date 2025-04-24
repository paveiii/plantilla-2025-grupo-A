import math

import arcade
from arcade import SpriteCircle, check_for_collision, SpriteList

from rpg.BattleAlly import BattleAlly
from rpg.sprites.character_sprite import CharacterSprite

class WorldAlly(CharacterSprite):

    def __init__(self, sheet_name, scene, player, battleKey, requirementItemName, dialogueNoItem, dialogueWithItem):
        super().__init__(sheet_name)
        self.aliadoBatalla= battleKey
        self.scene = scene
        self.jugador = player
        self.destination = None
        self.wall_list = None
        print(battleKey)

        self.dialogueNoItem = dialogueNoItem #Dialogo cuando el jugador no tiene el item necesitado para reclutar al personaje.
        self.dialogueRecruit = dialogueWithItem #Dialogo cuando el jugador tiene el item necesitado para reclutar al personaje.
        self.requirementItemName = requirementItemName #Nombre del objeto necesitado para reclutar al personaje.

    def detectar_jugador(self):
        distancia = arcade.get_distance_between_sprites(self.jugador, self)
        if self.radio_deteccion > distancia >= 16:  #16 es el radio de los sprites
            if distancia <= 18:
                print("JUGADOR COLISIONA CON EL ENEMIGO")
            return True
        else:
            return False
    def on_update(self, delta_time):
        super().on_update(delta_time)