import json

import arcade

from rpg.BattleBuddy import BattleBuddy
from rpg.constants import CHARACTER_SPRITE_SIZE

class BattleAlly(BattleBuddy):

    def __init__(self, sheet_name, displayName, displayDescription, type, maxStamina, maxHealth, restoredStamina, actions, dialogueNoItem, dialogueWithItem:"", requirementItemName:""):
        super().__init__(sheet_name, displayName, displayDescription, maxHealth, maxStamina, restoredStamina,actions)

        #Esta variable es para que la IA la use para determinar que clase de personaje es.
        #Por ahora propongo los siguientes tipos: Tank, Medic, Captain, Fighter
        self.type = type

        self.dialogueNoItem = dialogueNoItem #Dialogo cuando el jugador no tiene el item necesitado para reclutar al personaje.
        self.dialogueRecruit = dialogueWithItem #Dialogo cuando el jugador tiene el item necesitado para reclutar al personaje.
        self.requirementItemName = requirementItemName #Nombre del objeto necesitado para reclutar al personaje.

