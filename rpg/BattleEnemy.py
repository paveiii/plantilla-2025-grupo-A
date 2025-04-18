import arcade
from rpg.BattleBuddy import BattleBuddy
from rpg.constants import CHARACTER_SPRITE_SIZE

class BattleAlly(BattleBuddy):

    def __init__(self, sheet_name, displayName, displayDescription, maxStamina, maxHealth, restoredStamina):
        super().__init__(sheet_name, displayName, displayDescription, maxStamina, maxHealth, restoredStamina)
    def __init__(self, characterDictionaryPath:str, characterName:str):
        super().__init__(characterDictionaryPath, characterName)