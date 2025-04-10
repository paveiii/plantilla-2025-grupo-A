class Effect():

    def __init__(self, name, effectType, amount, durationInTurns, statAffected:None):

        self.displayName = name

        self.effectType = effectType #Damage, Heal, Multiplier
        self.amount = amount
        self.duration = durationInTurns


        self.stat = statAffected #En caso de multiplicador.