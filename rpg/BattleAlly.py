import json

import arcade

from rpg.BattleBuddy import BattleBuddy
from rpg.constants import CHARACTER_SPRITE_SIZE

class BattleAlly(BattleBuddy):

    def __init__(self, key, sheet_name, displayName, displayDescription, type, maxStamina, maxHealth, restoredStamina, actions, dialogueNoItem, dialogueWithItem:"", requirementItemName:""):
        super().__init__(key, sheet_name, displayName, displayDescription, maxHealth, maxStamina, restoredStamina,actions)

        #Esta variable es para que la IA la use para determinar que clase de personaje es.
        #Por ahora propongo los siguientes tipos: Tank, Medic, Captain, Fighter
        self.type = type