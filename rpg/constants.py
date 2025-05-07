"""
Constant values for the game
"""
import arcade

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Python Community RPG"
TILE_SCALING = 1.0
CHARACTER_SPRITE_SIZE = 64 #Original: 32
MAP_TILE_SIZE = 32

#Ruta del Sprite del jugador en la carpeta "resources/characters"
PLAYER_SPRITE_PATH = "Test/testWalk.png"


# How fast does the player move
MOVEMENT_SPEED = 8

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 300
RIGHT_VIEWPORT_MARGIN = 300
BOTTOM_VIEWPORT_MARGIN = 300
TOP_VIEWPORT_MARGIN = 300

# What map, and what position we start at
STARTING_MAP = "mapa_edad_media"


# Key mappings
KEY_UP = [arcade.key.UP, arcade.key.W]
KEY_DOWN = [arcade.key.DOWN, arcade.key.S]
KEY_LEFT = [arcade.key.LEFT, arcade.key.A]
KEY_RIGHT = [arcade.key.RIGHT, arcade.key.D]
INVENTORY = [arcade.key.I]
SEARCH = [arcade.key.E]

# Message box
MESSAGE_BOX_FONT_SIZE = 38
MESSAGE_BOX_MARGIN = 30

# How fast does the camera pan to the user
CAMERA_SPEED = 0.1

# Characters battle positions (in order)
ally_x_positions = [430, 180, 345, 280]
ally_y_positions = [490, 430, 345, 565]

# Enemies battle positions
enemy_x_positions = [SCREEN_WIDTH - 430,
                     SCREEN_WIDTH - 230,
                     SCREEN_WIDTH - 380,
                     SCREEN_WIDTH - 280]
enemy_y_positions = [490, 430, 345, 565]

CHARACTER_POINTER_SPEED = 0.3