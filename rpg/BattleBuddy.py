import json

import arcade

from rpg.Action import Action
from rpg.constants import CHARACTER_SPRITE_SIZE

class BattleBuddy(arcade.Sprite):

    def __init__(self, key, sheet_name, displayName, displayDescription, maxHealth, maxStamina, restoredStamina, actions):
        super().__init__()
        self.textures = arcade.load_spritesheet(
            sheet_name,
            sprite_width=CHARACTER_SPRITE_SIZE,
            sprite_height=CHARACTER_SPRITE_SIZE,
            columns=3,
            count=12,
        )

        self.characterKey = key
        self.sheetName = sheet_name

        self.should_update = 0
        self.cur_texture_index = 0
        self.texture = self.textures[self.cur_texture_index]

        self.maxStamina = maxStamina
        self.maxHealth = maxHealth

        self.currentStamina = maxStamina
        self.currentHealth = maxHealth

        self.restoredStamina = restoredStamina #Por turno.

        self.displayName = displayName
        self.displayDescription = displayDescription

        self.actions = actions

    def changeHealth(self, amount:float):
        self.currentHealth += amount
    def changeStamina(self, amount:float):
        self.currentStamina += amount
    #Funcion para ganar Stamina, llamada durante la batalla.
    def recoverStamina(self):
        self.currentStamina += self.restoredStamina