import arcade
from rpg.BattleBuddy import BattleBuddy

class BattleEnemy(BattleBuddy):

    def __init__(self, key, sheet_name, displayName, displayDescription, maxHealth, maxStamina, restoredStamina, actions):
        super().__init__(key, sheet_name, displayName, displayDescription, maxHealth, maxStamina, restoredStamina, actions)