"""
Animated sprite for characters that walk around.
"""


import arcade

from enum import Enum
from rpg.constants import CHARACTER_SPRITE_SIZE

Direction = Enum("Direction", "DOWN LEFT RIGHT UP")

SPRITE_INFO = {
    #Frames de animacion.
    Direction.UP: [1,2,3,4,5,7,8],
    Direction.LEFT: [9,10,11,12,13,14,15,16,17],
    Direction.DOWN: [19,20,21,22,23,24,25,26],
    Direction.RIGHT: [27,28,29,30,31,32,33,34,35],

    #Antiguo:
    #Direction.DOWN: [0, 1, 2],
    #Direction.LEFT: [3, 4, 5],
    #Direction.RIGHT: [6, 7, 8],
    #Direction.UP: [9, 10, 11],
}


class CharacterSprite(arcade.Sprite):
    def __init__(self, sheet_name):
        super().__init__()
        self.textures = arcade.load_spritesheet(
            sheet_name,
            sprite_width=CHARACTER_SPRITE_SIZE,
            sprite_height=CHARACTER_SPRITE_SIZE,
            columns=9, #Original: 3
            count=36, #Original: 12
        )
        self.should_update = 0
        self.cur_texture_index = 0
        self.texture = self.textures[self.cur_texture_index]

    def on_update(self, delta_time):
        if not self.change_x and not self.change_y:
            return

        # self.center_x += self.change_x
        # self.center_y += self.change_y

        #Control de velocidad en la que se actualizan los frames de la animacion.
        if self.should_update <= 3:
            self.should_update += 1
        else:
            self.should_update = 0
            self.cur_texture_index += 1

        direction = Direction.LEFT
        slope = self.change_y / (self.change_x + 0.0001)
        if abs(slope) < 0.8:
            if self.change_x > 0:
                direction = Direction.RIGHT
            else:
                # technically not necessary, but for readability
                direction = Direction.LEFT
        else:
            if self.change_y > 0:
                direction = Direction.UP
            else:
                direction = Direction.DOWN

        if self.cur_texture_index not in SPRITE_INFO[direction]:
            self.cur_texture_index = SPRITE_INFO[direction][0]

        self.texture = self.textures[self.cur_texture_index]
