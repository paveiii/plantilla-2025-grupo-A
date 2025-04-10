import arcade

class Ally():


    maxStamina = 0
    maxHealth = 0

    currentStamina = 0
    currentHealth = 0

    restoredStamina = 0

    nameDisplay = ""
    descriptionDisplay = ""

    dialogueNoItem = ""
    dialogueRecruit = ""
    recruitRequirementItem = ""

    def changeHealth(self, amount:float):
        self.currentHealth += amount
    def changeStamina(self, amount:float):
        self.currentHealth += amount