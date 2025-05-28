"""
Animated sprite for characters that walk around.
"""


import arcade

from enum import Enum
from rpg.constants import CHARACTER_SPRITE_SIZE

Anim = Enum("Animation", "DOWN LEFT RIGHT UP BATTLEIDLE ATTACK SKILL HURT DEAD")

SPRITE_INFO = {
    #Frames de animacion.
    Anim.UP:    [1, 2, 3, 4, 5, 6,7, 8],
    Anim.LEFT:  [9, 10, 11, 12, 13, 14, 15, 16, 17],
    Anim.DOWN:  [19, 20, 21, 22, 23, 24, 25, 26],
    Anim.RIGHT: [27, 28, 29, 30, 31, 32, 33, 34, 35],

    Anim.BATTLEIDLE:[36,37],
    Anim.ATTACK:    [45,46,47,48,49,50],
    Anim.SKILL:     [54,55,56,57,58,59,60],
    Anim.HURT:      [63,64],
    Anim.DEAD:      [72,73]

}


class CharacterSprite(arcade.Sprite):
    def __init__(self, sheet_name):
        super().__init__()
        self.textures = arcade.load_spritesheet(
            sheet_name,
            sprite_width=CHARACTER_SPRITE_SIZE,
            sprite_height=CHARACTER_SPRITE_SIZE,
            columns=9, #Valores 'Hardcoded', hacer constantes para esto.
            count=81,
        )
        self.sheetName = sheet_name

        self.should_update = 0
        self.cur_texture_index = 0
        self.texture = self.textures[self.cur_texture_index]

        self.currentAnimation = None
        self.animLock = False
        self.defaultAnim = Anim.BATTLEIDLE

    def on_update(self, delta_time):
        if(self.animLock == True):
            self.updateAnim()
            self.setAnim()
            self.exitAnim()
        else:
            if (self.change_x or self.change_y):
                self.setMoveAnim()

    def debugAnim(self):
        self.setPulseAnim(Anim.ATTACK)

    def updateAnim(self):
        #Control de velocidad en la que se actualizan los frames de la animacion.
        if self.should_update <= 3:
            self.should_update += 1
        else:
            self.should_update = 0
            self.cur_texture_index += 1
    def exitAnim(self):
        if self.currentAnimation == None:
            return
        if self.cur_texture_index == SPRITE_INFO[self.currentAnimation][-1]:
            self.currentAnimation = self.defaultAnim
            self.setAnim()
            self.animLock = False

    def setAnim(self):
        if self.currentAnimation == None:
            return
        if self.cur_texture_index not in SPRITE_INFO[self.currentAnimation]:
            self.cur_texture_index = SPRITE_INFO[self.currentAnimation][0]

        self.texture = self.textures[self.cur_texture_index]
    def setMoveAnim(self):
        self.currentAnimation = Anim.LEFT
        slope = self.change_y / (self.change_x + 0.0001)
        if abs(slope) < 0.1:
            if self.change_x > 0:
                self.currentAnimation = Anim.RIGHT
            else:
                # technically not necessary, but for readability
                self.currentAnimation = Anim.LEFT
        else:
            if self.change_y > 0:
                self.currentAnimation = Anim.UP
            else:
                self.currentAnimation = Anim.DOWN
        self.setAnim()
        self.updateAnim()
    def setPulseAnim(self, newAnimation):
        self.currentAnimation = newAnimation
        self.animLock = True
        self.setAnim()