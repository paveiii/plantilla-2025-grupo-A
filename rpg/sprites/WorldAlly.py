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

    def checkPlayer(self):
        self.distanciaJugador = arcade.get_distance_between_sprites(self.jugador, self)
        if self.distanciaJugador < 64:  # 32 es el radio de los sprites
            return True
        else:
            return False

    def get_interaction_dialogue(self):
        if not self.checkPlayer():
            return None  # No hay interacción

        itemRequirementFound = any(item.get("name") == self.requirementItemName for item in self.jugador.inventory)

        if itemRequirementFound:
            if len(self.jugador.player_team) < 4:
                self.jugador.player_team.append(self.aliadoBatalla)
            else:
                # Reemplazar segundo personaje por ahora (simplificado)
                self.jugador.player_team[1] = self.aliadoBatalla
            return self.dialogueRecruit, True
        else:
            return self.dialogueNoItem, False

    def on_update(self, delta_time):
        super().on_update(delta_time)