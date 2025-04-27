import math

import arcade
from arcade import SpriteCircle, check_for_collision, SpriteList

from rpg.sprites.character_sprite import CharacterSprite

from rpg.views.activate_in_battle_view import ActivateInBattleView

class WorldItem(arcade.Sprite):

    def __init__(self, sheet_name, itemKey):
        super().__init__(sheet_name)
        self.itemKey = itemKey