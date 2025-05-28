import json

import arcade

from rpg.Action import Action
from rpg.BattleAlly import BattleAlly
from rpg.sprites.character_sprite import CharacterSprite


class PlayerSprite(CharacterSprite):
    def __init__(self, sheet_name):
        super().__init__(sheet_name)
        self.sound_update = 0
        #self.footstep_sound = arcade.load_sound(":sounds:footstep00.wav")

        self.player_team = []
        self.player_team.append(self.create_battle_player())

        self.inventory = []

    def on_update(self, delta_time):
        super().on_update(delta_time)

        """if not self.change_x and not self.change_y:
            self.sound_update = 0
            return

        if self.should_update > 3:
            self.sound_update += 1

        if self.sound_update >= 3:
            arcade.play_sound(self.footstep_sound)
            self.sound_update = 0"""

    def get_player_team(self):
        return self.player_team

    def create_battle_player(self):
        f = open("../resources/data/battleCharacters_dictionary.json")
        battleCharacter_dictionary = json.load(f)

        f = open("../resources/data/actions_dictionary.json")
        actions_dictionary = json.load(f)

        battleKey = "TestCharacter1"

        playerActions = []
        for action in battleCharacter_dictionary[battleKey]['actions']:
            action_object = Action(actions_dictionary[action]["name"],
                                   actions_dictionary[action]["description"],
                                   actions_dictionary[action]["actionType"],
                                   actions_dictionary[action]["amount"],
                                   actions_dictionary[action]["staminaExpense"],
                                   actions_dictionary[action]["targetQuantity"],
                                   actions_dictionary[action]["effectName"])
            playerActions.append(action_object)

        battleAlly = BattleAlly( battleKey,f":characters:{battleCharacter_dictionary[battleKey]['sheet_name']}",
                                battleCharacter_dictionary[battleKey]['name'],
                                battleCharacter_dictionary[battleKey]['description'],
                                battleCharacter_dictionary[battleKey]['type'],
                                battleCharacter_dictionary[battleKey]['maxStamina'],
                                battleCharacter_dictionary[battleKey]['maxHealth'],
                                battleCharacter_dictionary[battleKey]['restoredStamina'],
                                playerActions,
                                battleCharacter_dictionary[battleKey]['dialogueNoItem'],
                                battleCharacter_dictionary[battleKey]['dialogueWithItem'],
                                battleCharacter_dictionary[battleKey]['requirementItemKey'])
        return battleAlly