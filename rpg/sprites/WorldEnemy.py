import math
import random

import arcade
from arcade import SpriteCircle, check_for_collision, SpriteList

from rpg.sprites.character_sprite import CharacterSprite
from rpg import constants

from rpg.views.activate_in_battle_view import ActivateInBattleView

class WorldEnemy(CharacterSprite):

    def __init__(self, sheet_name, scene, jugador, enemigosBatallaNombres, velocidad:1, radio_deteccion:200,wallList,mapSize):
        super().__init__(sheet_name)
        #Notese que esto es una lista de las Keys de battleCharacters_dictionary
        #para que puedan ser cargados posteriormente cuando se inicie una batalla.
        self.enemigos_batalla = enemigosBatallaNombres
        self.speed = velocidad
        self.scene = scene
        self.jugador = jugador
        self.radio_deteccion = radio_deteccion
        self.distanciaJugador = -1

        self.barrier_list = arcade.AStarBarrierList(self,wallList,32,
                                                    0,
                                                    mapSize[0]*32,
                                                    0,
                                                    mapSize[1]*32)
        self.path = None

    def detectar_jugador(self):
        self.distanciaJugador = arcade.get_distance_between_sprites(self.jugador, self)
        if self.radio_deteccion > self.distanciaJugador >= 16:  #32 es el radio de los sprites
            return True
        else:
            return False
    def chequear_colision(self):
        if self.distanciaJugador <= 34 and self.distanciaJugador >= 0:
            print("JUGADOR COLISIONA CON EL ENEMIGO")
            switch_to_battle = ActivateInBattleView(self.enemigos_batalla)

    def actualizar_path(self):
        newPath = arcade.astar_calculate_path(self.position,
                                                    self.jugador.position,
                                                    self.barrier_list,
                                                    diagonal_movement=False)
        if(newPath != None):
            self.path = newPath
    def perseguir_jugador(self):
        #Recordatorio de mencionar en GDD al genio que hizo un video sobre enemigos con Pathfinding de Arcade.
        #https://www.youtube.com/watch?v=nh0DHdX11oE&ab_channel=CharlieSmith
        if (self.path == None):
            return
        if(len(self.path) <= 1):
            return
        if (self.center_x == self.path[1][0] and self.center_y == self.path[1][1]):
            self.path.pop(0)
        if (len(self.path) <= 1):
            return
        if self.center_y < self.path[1][1]:
            self.center_y += min(self.speed, self.path[1][1] - self.center_y)
            self.change_y += 1
        elif self.center_y > self.path[1][1]:
            self.center_y -= min(self.speed, self.center_y - self.path[1][1])
            self.change_y = -1
        if self.center_x < self.path[1][0]:
            self.center_x += min(self.speed, self.path[1][0] - self.center_x)
            self.change_x += 1
        elif self.center_x > self.path[1][0]:
            self.center_x -= min(self.speed, self.center_x  - self.path[1][0])
            self.change_x = -1

    def on_update(self, delta_time):
        super().on_update(delta_time)
        if self.detectar_jugador():
            self.chequear_colision()
            self.actualizar_path()
        print(self.path)
        self.perseguir_jugador()

