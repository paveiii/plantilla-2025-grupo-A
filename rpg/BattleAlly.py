import arcade
from rpg.constants import SPRITE_SIZE

class BattleAlly(arcade.Sprite):

    def __init__(self, sheet_name, displayName, displayDescription, maxStamina, maxHealth, restoredStamina, dialogueNoItem, dialogueWithItem:"", requirementItemName:""):
        super().__init__()
        self.textures = arcade.load_spritesheet(
            sheet_name,
            sprite_width=SPRITE_SIZE,
            sprite_height=SPRITE_SIZE,
            columns=3,
            count=12,
        )
        self.should_update = 0
        self.cur_texture_index = 0
        self.texture = self.textures[self.cur_texture_index]

        self.maxStamina = maxStamina
        self.maxHealth = maxHealth

        self.currentStamina = maxStamina
        self.currentHealth = maxHealth

        self.restoredStamina = restoredStamina #Per turn

        self.displayName = displayName
        self.displayDescription = displayDescription

        self.dialogueNoItem = dialogueNoItem #Dialogo cuando el jugador no tiene el item necesitado para reclutar al personaje.
        self.dialogueRecruit = dialogueWithItem #Dialogo cuando el jugador tiene el item necesitado para reclutar al personaje.
        self.requirementItemName = requirementItemName #Nombre del objeto necesitado para reclutar al personaje.

        self.actions = []

    def changeHealth(self, amount:float):
        self.currentHealth += amount
    def changeStamina(self, amount:float):
        self.currentHealth += amount