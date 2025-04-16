import json

import arcade

from rpg.Action import Action
from rpg.constants import SPRITE_SIZE

class BattleBuddy(arcade.Sprite):

    def __init__(self, sheet_name, displayName, displayDescription, maxStamina, maxHealth, restoredStamina, actions):
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

        self.restoredStamina = restoredStamina #Por turno.

        #Esta variable es para que la IA la use para determinar que clase de personaje es.
        #Por ahora propongo los siguientes tipos: Tank, Medic, Captain, Fighter
        self.displayName = displayName
        self.displayDescription = displayDescription

        self.actions = actions
    def __init__(self, characterDictionaryPath:str, characterName:str):
        with open(characterDictionaryPath,"r") as f:
            data = json.load(f)

            super().__init__()
            self.textures = arcade.load_spritesheet(
                data[characterName]["sheet_name"],
                sprite_width=SPRITE_SIZE,
                sprite_height=SPRITE_SIZE,
                columns=3,
                count=12,
            )
            self.should_update = 0
            self.cur_texture_index = 0
            self.texture = self.textures[self.cur_texture_index]

            self.maxStamina = data[characterName]["maxStamina"]
            self.maxHealth = data[characterName]["maxHealth"]

            self.currentStamina = self.maxStamina
            self.currentHealth = self.maxHealth

            self.restoredStamina = data[characterName]["restoredStamina"]  # Por turno.

            self.displayName = data[characterName]["name"]
            self.displayDescription = data[characterName]["description"]

            self.actions = []
            actionNames = data[characterName]["actions"]
            for name in actionNames:
                # RECORDAR CAMBIAR ESTA RUTA A UNA RELATIVA SEGURA.
                """
                ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
                ░░░░░░░░░░▄█▀▀▀█░░░░░░░░░░░░░
                ░░░░░▄░░░▄▌▒▒▒▒█▌░░░░░▄██▄▄▄░
                ░░░░██░▄█▒▒▒▒▒█░░░░░▄█▒▒▀▒▒▒▌
                ░░░█▒▒▀▀▒▒▒▒▒▒▒▀▀█▄█▒▒▒▒▒▒▄█░
                ░░▐▒▒▒▒▒▒▒▒▒▒▒▒▒░░█▀▀▀█▄▒▒▀▀▌
                ▐███▒▒▒▒▒▒▒▒▐▒▒▄█▀░▄▄▄▄░▌▒▒█░
                ▐▒▒▀▒▒▒▒▒▐▄▒▐▀▀░░▄████▒▌██▀░░
                ▐▒▒▒▒▒▒▒▒▒▐▀▀░░▄██████▒▀█░░░░
                ░█▒▒▒▒▒▒▒▒██▀██▒▒████▒▒▒█▌░░░
                ░░█▄▄▄▄▄▄█▄▄▄█▒█▄▒▒▒▄▒▒▄▌█░░░
                ░▄█▀░░░░░░░▄▄█▒▒▒▀▀▀▒▄▀░░▐▌░░
                ▐█▄▄▄▄▀▀▀▀▀░▄▄▌▒▐▒▒▒▐▌░░░░█░░
                ░░░█▄▄▄▄▄▄█▀▒▒▒▒▌▒▒▒▒▌░░░░░█░
                ░░░░▐▒▒▒▒▒▒▒▒▒▒▒▌▒▒▒▒█░░░░░▐▌
                ░░░░█▒▒▒▐▒▒▒▒▒█▒█▒▒▒▒▒▌░░░░█░
                ░░░▐▒▒▒█▒▒▒▒▒▒▒█▐▒▒▒▒▒█▄▄▄█░░
                ░░░▌▒▒▒▐▒▌▒▒▒▒▒█▌▀▀█▀▀▀░░░░░░
                ░▄█▒▒▒▒▐▒▌▒▒▒▒▒▐█░░█░░░░░░░░░
                ░█▒▒▒▒▒▒▌█▒▒▒▒▒▐█▀▀░░░░░░░░░░
                ▐▒▒▒▒▒▒▒▌▒█▒▒▒▒▒▐░░░░░░░░░░░░
                ░█▒▒▒▒▒▄█▒▒▀█▒▒▒█░░░░░░░░░░░░
                ░░█▄▄▀▀░░▀█▄▄▄▄█░░░░░░░░░░░░░
                ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
                """
                newAction = Action("../resources/data/actions_dictionary.json",name)
                self.actions.append(newAction)
            print(self.actions)

    def changeHealth(self, amount:float):
        self.currentHealth += amount
    def changeStamina(self, amount:float):
        self.currentHealth += amount
    #Funcion para ganar Stamina, llamada durante la batalla.
    def recoverStamina(self):
        self.currentStamina += self.restoredStamina

#Pequeña prueba de un integrante del equipo.
#integrante = BattleBuddy("../resources/data/battleCharacters_dictionary.json","CharacterTemplate")
#print(integrante.actions[0].effect)
#print(integrante.actions[1].effect)