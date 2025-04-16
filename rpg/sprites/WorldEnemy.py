import math

import arcade
from arcade import SpriteCircle, check_for_collision, SpriteList

from rpg.sprites.character_sprite import CharacterSprite

class WorldEnemy(CharacterSprite):

    def __init__(self, sheet_name, scene, jugador:None, enemigosParaBatalla, speed=1,radio_deteccion = 200):
        super().__init__(sheet_name)
        self.enemigos_batalla = enemigosParaBatalla
        self.speed = speed
        self.scene = scene
        self.jugador = jugador
        self.radio_deteccion = radio_deteccion
        self.destination = None
        self.wall_list = None

    def detectar_jugador(self):
        distancia = arcade.get_distance_between_sprites(self.jugador, self)
        if self.radio_deteccion > distancia >= 16:  #16 es el radio de los sprites
            if distancia <= 18:
                print("JUGADOR COLISIONA CON EL ENEMIGO")
            return True
        else:
            return False


    def perseguir_jugador(self):
        pos_x = self.jugador.center_x - self.center_x
        pos_y = self.jugador.center_y - self.center_y
        angulo = math.atan2(pos_y, pos_x)

        self.change_x = math.cos(angulo) * self.speed
        self.change_y = math.sin(angulo) * self.speed

        self.center_x = self.center_x + self.change_x
        self.center_y = self.center_y + self.change_y



    def on_update(self, delta_time):
        super().on_update(delta_time)

        if self.detectar_jugador():
            self.perseguir_jugador()
        else:
            self.change_x = 0
            self.change_y = 0
