import json

from rpg.Effect import Effect


class Action():

    def __init__(self, name, description, actionType, amount, staminaExpense, targets:1, effect:None):

        self.displayName = name
        self.displayDescription = description

        self.actionType = actionType #Damage, Heal, Apply effect, Revive
        self.staminaExpense = staminaExpense
        self.amount = amount
        self.effect = effect

        self.targetQuantity = targets

    def get_name(self):
        return self.displayName
