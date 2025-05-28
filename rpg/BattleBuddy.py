import json

import arcade

from rpg.Action import Action
from rpg.constants import CHARACTER_SPRITE_SIZE
from rpg.sprites.character_sprite import CharacterSprite, Anim

class BattleBuddy(CharacterSprite):

    def __init__(self, key, sheet_name, displayName, displayDescription, maxHealth, maxStamina, restoredStamina, actions):
        super().__init__(sheet_name)

        self.characterKey = key

        self.maxStamina = maxStamina
        self.maxHealth = maxHealth

        self.currentStamina = maxStamina
        self.currentHealth = maxHealth

        self.restoredStamina = restoredStamina #Por turno.

        self.displayName = displayName
        self.displayDescription = displayDescription

        self.actions = actions

        self.texture = self.textures[0]
        self.defaultAnim = Anim.BATTLEIDLE
        self.currentAnimation = self.defaultAnim
        self.setAnim()

    def changeHealth(self, amount:float):
        self.currentHealth += amount
        if self.currentHealth > self.maxHealth:
            self.currentHealth = self.maxHealth
        if self.currentHealth < 0:
            self.currentHealth = 0
    def setHealth(self, amount:float):
        self.currentHealth = amount
    def changeStamina(self, amount:float):
        self.currentStamina += amount
        if self.currentStamina > self.maxStamina:
            self.currentStamina = self.maxStamina
        if self.currentStamina < 0:
            self.currentStamina = 0
    #Funcion para ganar Stamina, llamada durante la batalla.
    def recoverStamina(self):
        self.currentStamina += self.restoredStamina
    def setStamina(self, amount:float):
        self.currentStamina = amount