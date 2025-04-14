class Action():

    def __init__(self, name, description, actionType, amount, staminaExpense, targets:1, effect:None):

        self.displayName = name
        self.displayDescription = description

        self.actionType = actionType #Damage, Heal, Apply effect, Revive
        self.effect = effect

        self.staminaExpense = staminaExpense
        self.amount = amount
        self.targetQuantity = targets

