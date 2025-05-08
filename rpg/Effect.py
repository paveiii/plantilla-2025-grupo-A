import json


class Effect():

    def __init__(self, name, description, effectType, amount, durationInTurns, statAffected:None):

        self.displayName = name
        self.displayDescription = description

        self.effectType = effectType #Damage, Heal, Multiplier
        self.amount = amount
        self.duration = durationInTurns


        self.stat = statAffected #En caso de multiplicador.

    def useEffect(self):
        if(self.duration <= 0):
            self.duration = 0
        else:
            self.duration -= 1
