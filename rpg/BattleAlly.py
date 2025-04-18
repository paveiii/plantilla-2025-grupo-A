import json

import arcade

from rpg.BattleBuddy import BattleBuddy
from rpg.constants import CHARACTER_SPRITE_SIZE

class BattleAlly(BattleBuddy):

    def __init__(self, sheet_name, displayName, displayDescription, type, maxStamina, maxHealth, restoredStamina, dialogueNoItem, dialogueWithItem:"", requirementItemName:""):
        super().__init__(sheet_name, displayName, displayDescription, maxStamina, maxHealth, restoredStamina)

        #Esta variable es para que la IA la use para determinar que clase de personaje es.
        #Por ahora propongo los siguientes tipos: Tank, Medic, Captain, Fighter
        self.type = type

        self.dialogueNoItem = dialogueNoItem #Dialogo cuando el jugador no tiene el item necesitado para reclutar al personaje.
        self.dialogueRecruit = dialogueWithItem #Dialogo cuando el jugador tiene el item necesitado para reclutar al personaje.
        self.requirementItemName = requirementItemName #Nombre del objeto necesitado para reclutar al personaje.

    def __init__(self, characterDictionaryPath:str, characterName:str):
        super().__init__(characterDictionaryPath, characterName)

        with open(characterDictionaryPath,"r") as f:
            data = json.load(f)

            # Esta variable es para que la IA la use para determinar que clase de personaje es.
            # Por ahora propongo los siguientes tipos: Tank, Medic, Captain, Fighter
            self.type = data[characterName]["type"]

            self.dialogueNoItem = data[characterName]["dialogueNoItem"]  # Dialogo cuando el jugador no tiene el item necesitado para reclutar al personaje.
            self.dialogueRecruit = data[characterName]["dialogueWithItem"]  # Dialogo cuando el jugador tiene el item necesitado para reclutar al personaje.
            self.requirementItemName = data[characterName]["requirementItemName"]  # Nombre del objeto necesitado para reclutar al personaje.


