"""
Load maps
"""
import sys
import random
import json
import os
from collections import OrderedDict
from os.path import isfile, join

import arcade
from arcade.experimental.lights import Light, LightLayer
from arcade import Sprite
if sys.platform == "win32" or sys.platform == "win64":
    from pyglet.gl.wglext_arb import wglWaitForSbcOML

from rpg.sprites.WorldEnemy import WorldEnemy
from rpg.sprites.WorldAlly import WorldAlly
from rpg.sprites.character_sprite import CharacterSprite
from rpg.constants import TILE_SCALING
from rpg.sprites.path_following_sprite import PathFollowingSprite
from rpg.sprites.random_walking_sprite import RandomWalkingSprite


class GameMap:
    name = None
    scene = None
    map_layers = None
    light_layer = None
    map_size = None
    properties = None
    background_color = arcade.color.AMAZON


def load_map(map_name,player):
    """
    Load a map
    """

    game_map = GameMap()
    game_map.map_layers = OrderedDict()

    game_map.light_layer = LightLayer(100, 100)

    # List of blocking sprites

    layer_options = {
        "trees_blocking": {
            "use_spatial_hash": True,
        },
        "misc_blocking": {
            "use_spatial_hash": True,
        },
        "bridges": {
            "use_spatial_hash": True,
        },
        "water_blocking": {
            "use_spatial_hash": True,
        },
        "decoration_blocking": {
            "use_spatial_hash": True,
        },
        "decoration_blocking2": {
            "use_spacial_hash": True,
        }
    }

    # Read in the tiled map
    print(f"Loading map: {map_name}")
    my_map = arcade.tilemap.load_tilemap(
        map_name, scaling=TILE_SCALING, layer_options=layer_options
    )

    game_map.scene = arcade.Scene.from_tilemap(my_map)

    if "searchable" in my_map.object_lists:
        f = open("../resources/data/item_dictionary.json")
        item_dictionary = json.load(f)
        item_object_list = my_map.object_lists["searchable"]

        for item_object in item_object_list:
            if "item_type" not in item_object.properties:
                print(
                    f"No 'item_type' field for character in map {map_name}. {item_object.properties}"
                )
                continue

            item_key = item_object.properties["item_key"]
            if item_key not in item_dictionary:
                print(
                    f"Unable to find '{item_key}' in characters_dictionary.json."
                )
                continue

            item_data = item_dictionary[item_key]
            print(item_data)
            shape = item_object.shape
            item_sprite = None

            if isinstance(shape, list) and len(shape) == 2:
                # Point
                if item_object.properties.get("item_type") == "Requirement":
                    sheetName = f":items:{item_data['sheet_name']}"
                    item_sprite = Sprite(sheetName)
            if (item_sprite is not None): item_sprite.position = shape
            if (item_sprite != None):
                print(f"Adding item {item_key} at {item_sprite.position}")
                print(item_sprite)
                game_map.scene.add_sprite("searchable", item_sprite)

    if "characters" in my_map.object_lists:
        f = open("../resources/data/characters_dictionary.json")
        character_dictionary = json.load(f)
        character_object_list = my_map.object_lists["characters"]

        #Cargar los personajes de batalla.
        f = open("../resources/data/battleCharacters_dictionary.json")
        battleCharacter_dictionary = json.load(f)

        allyNamesSpawned = []

        #f = open("../resources/data/actions_dictionary.json")
        #actions_dictionary = json.load(f)

        for character_object in character_object_list:
            if "type" not in character_object.properties:
                print(
                    f"No 'type' field for character in map {map_name}. {character_object.properties}"
                )
                continue

            character_type = character_object.properties["type"]
            if character_type not in character_dictionary:
                print(
                    f"Unable to find '{character_type}' in characters_dictionary.json."
                )
                continue

            character_data = character_dictionary[character_type]
            print(character_data)
            shape = character_object.shape

            if isinstance(shape, list) and len(shape) == 2:
                # Point
                if character_object.properties.get("movement") == "random":
                    character_sprite = RandomWalkingSprite(
                        f":characters:{character_data['images']}", game_map.scene
                    )
                #Spawn de enemigos.
                elif character_object.properties.get("movement") == "enemy":

                    #Carga  en la lista los nombres de los posibles enemigos que pueden aparecer en la batalla.
                    #En caso de que un nombre no este en el diccionario de personajes de batalla, se ignora.
                    availableBattleAllyNames = []
                    for battleCharacter_name in character_data["battleTeammate_names"]:
                        if battleCharacter_name not in battleCharacter_dictionary:
                            print(battleCharacter_name + " no se encuentra en el diccionario de personajes de batalla.")
                            continue
                        availableBattleAllyNames.append(battleCharacter_name)

                    #Lista que contiene los nombres de los enemigos que apareceran en batalla.
                    battleEnemyNames = []


                    battleTeammatesAmount = character_data["battleTeammates_amount"]

                    #En caso de que la cantidad de enemigos en batalla sea aleatoria, se toma como maximo "battleTeammates_amount"
                    if(character_data["random_amount"] == True):
                        battleTeammatesAmount = random.randint(1,battleTeammatesAmount)

                    for i in range(0,battleTeammatesAmount):
                        randomNameIndex = random.randint(0, len(availableBattleAllyNames) - 1)
                        battleEnemyNames.append(availableBattleAllyNames[randomNameIndex])

                    #Se toma el nombre de un enemigo del equipo que aparecera en batalla para mostrar su Sprite en el nivel.
                    #Notese que se usa la lista final para favorecer la aparicion
                    #de los Sprites de los enemigos mas abundantes en el equipo.
                    randomSpriteIndex = random.randint(0, len(battleEnemyNames) - 1)

                    #Se crea el enemigo en el nivel.
                    character_sprite = WorldEnemy(f":characters:{battleCharacter_dictionary[battleEnemyNames[randomSpriteIndex]]['sheet_name']}", game_map.scene,player, battleEnemyNames,character_data["speed"],character_data["detectionRadius"])

                #Spawn de aliados.
                elif character_object.properties.get("movement") == "ally":
                    #SPAWN DE OBJETO DE REQUERIMIENTO.

                    # Carga  en la lista los nombres de los posibles aliados que pueden aparecer en la batalla.
                    # En caso de que un nombre no este en el diccionario de personajes de batalla, se ignora.
                    availableBattleAllyNames = []
                    for battleCharacter_name in character_data["battleTeammate_names"]:
                        if battleCharacter_name not in battleCharacter_dictionary:
                            print(battleCharacter_name + " no se encuentra en el diccionario de personajes de batalla.")
                            continue
                        elif battleCharacter_name in allyNamesSpawned:
                            print(battleCharacter_name + " Ya está en la lista.")
                            continue
                        availableBattleAllyNames.append(battleCharacter_name)

                    if(len(availableBattleAllyNames) > 0):
                        randomIndex = random.randint(0, len(availableBattleAllyNames) - 1)

                        battleKey = availableBattleAllyNames[randomIndex]
                        allyNamesSpawned.append(battleKey)

                        requirementItemName = character_data["requirementItemName"]
                        dialogueNoItem = character_data["dialogueNoItem"]
                        dialogueWithItem = character_data["dialogueWithItem"]

                        character_sprite = WorldAlly(f":characters:{battleCharacter_dictionary[battleKey]['sheet_name']}", game_map.scene, player, battleKey, requirementItemName, dialogueNoItem, dialogueWithItem)
                    else:
                        character_sprite = None
                else:
                    character_sprite = None
                if(character_sprite is not None): character_sprite.position = shape
            elif isinstance(shape, list) and len(shape[0]) == 2:
                # Rect or polygon.
                location = [shape[0][0], shape[0][1]]
                character_sprite = PathFollowingSprite(
                    f":characters:{character_data['images']}"
                )
                character_sprite.position = location
                path = []
                for point in shape:
                    location = [point[0], point[1]]
                    path.append(location)
                character_sprite.path = path
            else:
                print(
                    f"Unknown shape type for character with shape '{shape}' in map {map_name}."
                )
                continue

            if(character_sprite != None):
                print(f"Adding character {character_type} at {character_sprite.position}")
                print(character_sprite)
                game_map.scene.add_sprite("characters", character_sprite)

    if "lights" in my_map.object_lists:
        lights_object_list = my_map.object_lists["lights"]

        for light_object in lights_object_list:
            if "color" not in light_object.properties:
                print(f"No color for light in map {map_name}.")
                continue

            shape = light_object.shape

            if isinstance(shape, list) and len(shape) == 2:
                # Point
                if "radius" in light_object.properties:
                    radius = light_object.properties["radius"]
                else:
                    radius = 150
                mode = "soft"
                color = light_object.properties["color"]
                color = (color.red, color.green, color.blue)
                light = Light(shape[0], shape[1], radius, color, mode)
                game_map.light_layer.add(light)
                print("Added light", color, "radius", radius)
            else:
                print("Failed to add light")
    else:
        # Hack
        x = 0
        y = 0
        radius = 1
        mode = "soft"
        color = arcade.csscolor.WHITE
        dummy_light = Light(x, y, radius, color, mode)
        game_map.light_layer.add(dummy_light)
        print("Added default light")

    # Get all the tiled sprite lists
    # Get all the tiled sprite lists
    game_map.map_layers = my_map.sprite_lists

    # Define the size of the map, in tiles
    game_map.map_size = my_map.width, my_map.height

    # Set the background color
    game_map.background_color = my_map.background_color

    game_map.properties = my_map.properties

    # Any layer with '_blocking' in it, will be a wall
    game_map.scene.add_sprite_list("wall_list", use_spatial_hash=True)
    game_map.scene.add_sprite_list("slowdown_list", use_spatial_hash=True)
    for layer, sprite_list in game_map.map_layers.items():
        if "_blocking" in layer:
            game_map.scene.remove_sprite_list_by_object(sprite_list)
            game_map.scene["wall_list"].extend(sprite_list)
        if "_slowdown" in layer:
            game_map.scene.remove_sprite_list_by_object(sprite_list)
            game_map.scene["slowdown_list"].extend(sprite_list)


    return game_map


def load_maps(player):
    """
    Load all the Tiled maps from a directory.
    (Must use the .json extension.)
    """

    # Directory to pull maps from
    mypath = "../resources/maps"

    if load_maps.map_file_names is None:

        # Dictionary to hold all our maps
        load_maps.map_list = {}

        # Pull names of all json files in that path
        load_maps.map_file_names = [
            f[:-5]
            for f in os.listdir(mypath)
            if isfile(join(mypath, f)) and f.endswith(".json")
        ]
        load_maps.map_file_names.sort()
        load_maps.file_count = len(load_maps.map_file_names)

    # Loop and load each file
    map_name = load_maps.map_file_names.pop(0)
    load_maps.map_list[map_name] = load_map(f"../resources/maps/{map_name}.json",player)

    files_left = load_maps.file_count - len(load_maps.map_file_names)
    progress = 100 * files_left / load_maps.file_count

    done = len(load_maps.map_file_names) == 0
    return done, progress, load_maps.map_list


load_maps.map_file_names = None
load_maps.map_list = None
load_maps.file_count = None
