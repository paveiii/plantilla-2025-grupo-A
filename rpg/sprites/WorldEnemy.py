import math
import random

import arcade
from arcade import SpriteCircle, check_for_collision, SpriteList

from rpg.sprites.character_sprite import CharacterSprite
from rpg import constants

from rpg.views.activate_in_battle_view import ActivateInBattleView

class WorldEnemy(CharacterSprite):

    def __init__(self, sheet_name, scene, jugador, enemigosBatallaNombres, velocidad:1, radio_deteccion:200,barrierList):
        super().__init__(sheet_name)
        #Notese que esto es una lista de las Keys de battleCharacters_dictionary
        #para que puedan ser cargados posteriormente cuando se inicie una batalla.
        self.enemigosBatalla = enemigosBatallaNombres
        self.speed = velocidad
        self.scene = scene
        self.jugador = jugador
        self.radio_deteccion = radio_deteccion
        self.distanciaJugador = -1

        self.barrier_list = barrierList
        self.path = None

        print("Creando hitbox de", self.texture) # Debug
        print("Hitbox:", self.get_hit_box()) # Debug

    def detectar_jugador(self):
        self.distanciaJugador = arcade.get_distance_between_sprites(self.jugador, self)
        if self.radio_deteccion > self.distanciaJugador >= 16:  #32 es el radio de los sprites
            return True
        else:
            return False
    def chequear_colision(self):
        if self.distanciaJugador <= 34 and self.distanciaJugador >= 0:
            print("JUGADOR COLISIONA CON EL ENEMIGO")
            switch_to_battle = ActivateInBattleView(self)

    def actualizar_path(self):
        newPath = arcade.astar_calculate_path(self.position,
                                                    self.jugador.position,
                                                    self.barrier_list,
                                                    diagonal_movement=False)
        if(newPath != None):
            self.path = newPath
    def perseguir_jugador(self):
        if (self.path == None):
            return
        if(len(self.path) <= 1):
            return
        if (self.center_x == self.path[1][0] and self.center_y == self.path[1][1]):
            self.path.pop(0)
        if (len(self.path) <= 1):
            return
        self.change_x = 0
        self.change_y = 0
        if self.center_y < self.path[1][1]:
            self.center_y += min(self.speed, self.path[1][1] - self.center_y)
            self.change_y = 1
        elif self.center_y > self.path[1][1]:
            self.center_y -= min(self.speed, self.center_y - self.path[1][1])
            self.change_y = -1
        if self.center_x < self.path[1][0]:
            self.center_x += min(self.speed, self.path[1][0] - self.center_x)
            self.change_x = 1
        elif self.center_x > self.path[1][0]:
            self.center_x -= min(self.speed, self.center_x  - self.path[1][0])
            self.change_x = -1
    def cambiar_barrierList(self, newBarrierList):
        self.barrier_list = newBarrierList

    def on_update(self, delta_time):
        super().on_update(delta_time)
        if self.detectar_jugador():
            self.chequear_colision()
            self.actualizar_path()
        self.perseguir_jugador()

