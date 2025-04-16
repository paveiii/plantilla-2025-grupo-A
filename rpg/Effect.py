import json


class Effect():

    def __init__(self, name, description, effectType, amount, durationInTurns, statAffected:None):

        self.displayName = name
        self.displayDescription = description

        self.effectType = effectType #Damage, Heal, Multiplier
        self.amount = amount
        self.duration = durationInTurns


        self.stat = statAffected #En caso de multiplicador.

    def __init__(self,  effectsDictionaryPath: str, effectName: str):
        with open(effectsDictionaryPath, "r") as f:
            data = json.load(f)

            self.displayName = data[effectName]["name"]
            self.displayDescription = data[effectName]["description"]

            self.effectType = data[effectName]["effectType"]  # Damage, Heal, Multiplier
            self.amount = data[effectName]["amount"]
            self.duration = data[effectName]["durationInTurns"]

            self.stat = data[effectName]["statAffected"]  # En caso de multiplicador.

    def useEffect(self):
        if(self.duration <= 0):
            pass
        pass
