import json

from rpg.Effect import Effect


class Action():

    def __init__(self, name, description, actionType, amount, staminaExpense, targets:1, effect:None):

        self.displayName = name
        self.displayDescription = description

        self.actionType = actionType #Damage, Heal, Apply effect, Revive
        self.effect = effect

        self.staminaExpense = staminaExpense
        self.amount = amount
        self.targetQuantity = targets

    def __init__(self, actionDictionaryPath: str, actionName: str):

        with open(actionDictionaryPath, "r") as f:
            data = json.load(f)

            self.displayName = data[actionName]["name"]
            self.displayDescription = data[actionName]["description"]

            self.actionType = data[actionName]["actionType"]  # Damage, Heal, Apply effect, Revive

            self.staminaExpense = data[actionName]["staminaExpense"]
            self.amount = data[actionName]["amount"]
            self.targetQuantity = data[actionName]["targetQuantity"]

            self.effect = None
            if(self.actionType == "ApplyEffect"): self.effect = Effect("../resources/data/effects_dictionary.json",data[actionName]["effectName"])

    def get_name(self):
        return self.displayName
