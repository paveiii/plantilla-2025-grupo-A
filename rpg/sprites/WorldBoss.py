import math

import arcade
from arcade import SpriteCircle, check_for_collision, SpriteList

from rpg.sprites.character_sprite import Anim
from rpg.sprites.character_sprite import CharacterSprite
from rpg.views.activate_in_battle_view import ActivateInBattleView


class WorldBoss(CharacterSprite):

    def __init__(self, sheet_name, scene, player, boss):
        super().__init__(sheet_name)
        self.enemigosBatalla= boss
        self.setPulseAnim(Anim.BATTLEIDLE)
        self.scene = scene
        self.jugador = player
        self.distanciaJugador = 0


    def checkCollision(self):
        if self.distanciaJugador <= 150 and self.distanciaJugador >= 0:
            print("JUGADOR COLISIONA CON EL ENEMIGO")
            switch_to_battle = ActivateInBattleView(self)

    def on_update(self, delta_time):
        super().on_update(delta_time)
        self.distanciaJugador = arcade.get_distance_between_sprites(self.jugador, self)
        self.checkCollision()