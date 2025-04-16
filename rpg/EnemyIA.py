import random

class EnemyIA():
    def __init__(self, team, playerTeam):
        #Lista de los integrantes del equipo enemigo actual en batalla.
        self.team = team
        #Lista de los integrantes del equipo del jugador en batalla.
        self.playerTeam = playerTeam
    #Devuelve al bucle el turno que el equipo enemigo quiere realizar.
    def returnTurnToExecute(self, turnTeammate):
        currentActions = self.returnAvailableActions(turnTeammate)
        tags = self.tagPlayerTeammates()
        playerTeammate = self.returnHighestPriorityPlayerTeammate(tags)
        actionToExecute = currentActions[random.randint[0,len(currentActions)-1]]
        return actionToExecute, playerTeammate

    #Devuelve las acciones realizables por el integrante especificado
    #como parametro del equipo enemigo.
    def returnAvailableActions(self, enemyTeammate):
        actions = []
        for action in enemyTeammate.actions:
            if(action.staminaExpense < enemyTeammate.currentStamina):
                actions.append(action)
    #Se encarga de asignar prioridad a cada integrante del equipo del juegador.
    #1 > 2 > 3 > 4 > 5
    #(No tiene sentido, pero asi es mas facil de implementar mas prioridades.)
    def tagPlayerTeammates(self):
        tags = []

        for playerTeammate in self.playerTeam:
            #Numero 1000 es arbitrario, habra que cambiarlo para cuando
            #creamos las estadisticas finales.
            if(playerTeammate.currentHealth < 1000):
                tags.append(1)
                continue
            if(playerTeammate.type == "Medic" or playerTeammate.type == "Captain"):
                tags.append(2)
                continue
            if(playerTeammate.type == "Tank"):
                tags.append(3)
                continue
            else:
                tags.append(4)
                continue
        return tags
    #Funcion que se encarga de devolver al integrante del equipo del jugador con mayor prioridad de ataque.
    def returnHighestPriorityPlayerTeammate(self, tags):
        enemyIndex = 0
        highestPriority = 0
        for i in range(tags):
            if(highestPriority == 1):
                break
            if(tags[i] < highestPriority):
                enemyIndex = i
        return self.playerTeam[enemyIndex]

