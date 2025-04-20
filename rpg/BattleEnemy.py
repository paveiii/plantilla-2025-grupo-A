import arcade
from rpg.BattleBuddy import BattleBuddy

class BattleEnemy(BattleBuddy):

    def __init__(self, sheet_name, displayName, displayDescription, maxStamina, maxHealth, restoredStamina):
        super().__init__(sheet_name, displayName, displayDescription, maxStamina, maxHealth, restoredStamina)