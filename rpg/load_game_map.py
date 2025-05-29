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
from arcade import tilemap
from arcade.experimental.lights import Light, LightLayer
from arcade import Sprite

from rpg.Action import Action
from rpg.BattleAlly import BattleAlly
from rpg.BattleEnemy import BattleEnemy
from rpg.sprites.WorldBoss import WorldBoss

if sys.platform == "win32" or sys.platform == "win64":
    from pyglet.gl.wglext_arb import wglWaitForSbcOML

from rpg.sprites.WorldEnemy import WorldEnemy
from rpg.sprites.WorldAlly import WorldAlly
from rpg.sprites.WorldItem import WorldItem
from rpg.sprites.character_sprite import CharacterSprite
from rpg.constants import TILE_SCALING
from rpg.sprites.path_following_sprite import PathFollowingSprite
from rpg.sprites.random_walking_sprite import RandomWalkingSprite
from rpg import constants


class GameMap():
    def __init__(self):
        self.worldEnemyList = arcade.SpriteList()
        self.worldAllyList = arcade.SpriteList()
        self.worldItemList = arcade.SpriteList()
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
    ally_list = []

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
            "use_spatial_hash": True,
        },
        "rivers_blocking": {
            "use_spatial_hash": True,
        },
        "test_blocking": {
            "use_spatial_hash": True,
        }
    }

    # Read in the tiled map
    print(f"Loading map: {map_name}")
    my_map = arcade.tilemap.load_tilemap(
map_name, scaling=TILE_SCALING, layer_options=layer_options
    )

    game_map.scene = arcade.Scene.from_tilemap(my_map)

    # Get all the tiled sprite lists
    game_map.map_layers = my_map.sprite_lists

    # Define the size of the map, in tiles
    game_map.map_size = my_map.width, my_map.height

    # Set the background color
    game_map.background_color = my_map.background_color

    game_map.properties = my_map.properties

    try:
        #Este bool define si el mapa es un submapa, es decir, un mapa al que eres teletransportado desde otro mapa.
        #De ser True, se ignora el proceso de verificar si existe start_x y start_y, ya que la posicion de inicio
        #es definida en otro sitio.
        isSubmap = game_map.properties.get("isSubmap")
    except AttributeError:
        raise AttributeError(f"EL MAPA {map_name} NO TIENE DEFINIDA LA VARIABLE 'isSubmap'")
    if(isSubmap == False):
        try:
            print(game_map.properties.get("start_x") ,game_map.properties.get("start_y"))
        except AttributeError:
            raise AttributeError(f"EL MAPA {map_name} NO TIENE DEFINIDA UNA POSICION INICIAL X y/o Y.")

    # Any layer with '_blocking' in it, will be a wall
    game_map.scene.add_sprite_list("wall_list", use_spatial_hash=True)
    game_map.scene.add_sprite_list("slowdown_list", use_spatial_hash=True)
    game_map.scene.add_sprite_list("grass_top", use_spatial_hash=True)
    for layer, sprite_list in game_map.map_layers.items():
        if "_blocking" in layer:
            # Eliminar la spritelist original
            game_map.scene.remove_sprite_list_by_object(sprite_list)

            # Crear nueva lista filtrada con solo los que tienen hitbox
            filtered = arcade.SpriteList(use_spatial_hash=True)
            for sprite in sprite_list:
                if sprite.get_hit_box():
                    filtered.append(sprite)
                else:
                    print(f"[AVISO] Sprite ignorado por hitbox vacía en capa '{layer}': {sprite}")

            # Añadir a wall_list
            game_map.scene["wall_list"].extend(filtered)

        if "_slowdown" in layer:
            game_map.scene.remove_sprite_list_by_object(sprite_list)
            game_map.scene["slowdown_list"].extend(sprite_list)
        if layer == "top":
            # game_map.scene.remove_sprite_list_by_object(sprite_list)
            game_map.scene["grass_top"].extend(sprite_list)

    f = open("../resources/data/worldItem_dictionary.json")
    worldItem_dictionary = json.load(f)

    f = open("../resources/data/item_dictionary.json")
    item_dictionary = json.load(f)

    spawnedAlliesKeys = []
    mapBarrierList = None
    if "characters" in my_map.object_lists:
        f = open("../resources/data/characters_dictionary.json")
        character_dictionary = json.load(f)
        character_object_list = my_map.object_lists["characters"]

        #Cargar los personajes de batalla.
        f = open("../resources/data/battleCharacters_dictionary.json")
        battleCharacter_dictionary = json.load(f)

        #Puse este código hace como un mes y ahora lo necesito ouuu yeah
        f = open("../resources/data/actions_dictionary.json")
        actions_dictionary = json.load(f)

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
            shape = character_object.shape

            if isinstance(shape, list) and len(shape) == 2:
                # Point
                if character_object.properties.get("movement") == "random":
                    character_sprite = RandomWalkingSprite(
                        f":characters:{character_data['images']}", game_map.scene
                    )
                #Spawn de enemigos.
                elif character_object.properties.get("movement") == "boss":
                    battleKey = character_object.properties.get("type")

                    character_sprite = WorldBoss(f":characters:{battleCharacter_dictionary[battleKey]['sheet_name']}", game_map.scene,player, [battleKey])
                    character_sprite.position = character_object.shape
                    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa")
                    print(character_sprite.position)



                elif character_object.properties.get("movement") == "enemy":

                    #Carga en la lista los nombres de los posibles enemigos que pueden aparecer en la batalla.
                    #En caso de que un nombre no este en el diccionario de personajes de batalla, se ignora.
                    availableBattleAllyKeys = []
                    for battleCharacter_key in character_data["battleTeammate_keys"]:
                        if battleCharacter_key not in battleCharacter_dictionary:
                            print(battleCharacter_key + " no se encuentra en el diccionario de personajes de batalla.")
                            continue
                        availableBattleAllyKeys.append(battleCharacter_key)

                    #Lista que contiene los nombres de los enemigos que apareceran en batalla.
                    battleEnemyKeys = []


                    battleTeammatesAmount = character_data["battleTeammates_amount"]

                    #En caso de que la cantidad de enemigos en batalla sea aleatoria, se toma como maximo "battleTeammates_amount"
                    if(character_data["random_amount"] == True):
                        battleTeammatesAmount = random.randint(1,battleTeammatesAmount)

                    for i in range(0,battleTeammatesAmount):
                        randomKeyIndex = random.randint(0, len(availableBattleAllyKeys) - 1)
                        battleEnemyKeys.append(availableBattleAllyKeys[randomKeyIndex])

                    #Se toma el nombre de un enemigo del equipo que aparecera en batalla para mostrar su Sprite en el nivel.
                    #Notese que se usa la lista final para favorecer la aparicion
                    #de los Sprites de los enemigos mas abundantes en el equipo.
                    randomSpriteIndex = random.randint(0, len(battleEnemyKeys) - 1)

                    #Se crea el enemigo en el nivel.
                    # Debug
                    print("Creando enemigo con sprite:",
                          f":characters:{battleCharacter_dictionary[battleEnemyKeys[randomSpriteIndex]]['sheet_name']}")
                    character_sprite = WorldEnemy(f":characters:{battleCharacter_dictionary[battleEnemyKeys[randomSpriteIndex]]['sheet_name']}", game_map.scene,player, battleEnemyKeys,character_data["speed"],character_data["detectionRadius"],mapBarrierList)
                    game_map.worldEnemyList.append(character_sprite)

                    if(mapBarrierList == None):
                        mapBarrierList = arcade.AStarBarrierList(character_sprite, game_map.scene["wall_list"], 32,
                                            0,
                                            game_map.map_size[0] * 32,
                                            0,
                                            game_map.map_size[1] * 32)
                        character_sprite.cambiar_barrierList(mapBarrierList)

                        # Sprites problemáticos sin hitbox
                        for i, wall in enumerate(game_map.scene["wall_list"]):
                            hb = wall.get_hit_box()
                            if not hb:
                                print(f"[ERROR] Wall #{i} sin hitbox:", wall)
                #Spawn de aliados.
                elif character_object.properties.get("movement") == "ally":

                    # Carga  en la lista los nombres de los posibles aliados que pueden aparecer en la batalla.
                    # En caso de que un nombre no este en el diccionario de personajes de batalla, se ignora.
                    availableBattleAllyKeys = []
                    for battleCharacter_key in character_data["battleTeammate_keys"]:
                        if battleCharacter_key not in battleCharacter_dictionary:
                            print(battleCharacter_key + " no se encuentra en el diccionario de personajes de batalla.")
                            continue
                        elif battleCharacter_key in spawnedAlliesKeys:
                            print(battleCharacter_key + " Ya está en la lista.")
                            continue
                        availableBattleAllyKeys.append(battleCharacter_key)

                    if(len(availableBattleAllyKeys) > 0):
                        randomIndex = random.randint(0, len(availableBattleAllyKeys) - 1)

                        #REFACTORIZAR
                        battleKey = availableBattleAllyKeys[randomIndex]

                        allyActions = []
                        for action in battleCharacter_dictionary[battleKey]['actions']:
                            action_object = Action(actions_dictionary[action]["name"],
                                                   actions_dictionary[action]["description"],
                                                   actions_dictionary[action]["actionType"],
                                                   actions_dictionary[action]["amount"],
                                                   actions_dictionary[action]["staminaExpense"],
                                                   actions_dictionary[action]["targetQuantity"],
                                                   actions_dictionary[action]["effectName"])
                            allyActions.append(action_object)

                        battleAlly = BattleAlly(battleKey,f":characters:{battleCharacter_dictionary[battleKey]['sheet_name']}",
                                                 battleCharacter_dictionary[battleKey]['name'],
                                                 battleCharacter_dictionary[battleKey]['description'],
                                                 battleCharacter_dictionary[battleKey]['type'],
                                                 battleCharacter_dictionary[battleKey]['maxStamina'],
                                                 battleCharacter_dictionary[battleKey]['maxHealth'],
                                                 battleCharacter_dictionary[battleKey]['restoredStamina'],
                                                 allyActions,
                                                 battleCharacter_dictionary[battleKey]['dialogueNoItem'],
                                                 battleCharacter_dictionary[battleKey]['dialogueWithItem'],
                                                 battleCharacter_dictionary[battleKey]['requirementItemKey'])

                        requirementItemName = item_dictionary[battleCharacter_dictionary[battleKey]["requirementItemKey"]].get("name")
                        dialogueNoItem = battleCharacter_dictionary[battleKey]["dialogueNoItem"]
                        dialogueWithItem = battleCharacter_dictionary[battleKey]["dialogueWithItem"]

                        character_sprite = WorldAlly(f":characters:{battleCharacter_dictionary[battleKey]['sheet_name']}", game_map.scene, player, battleAlly, requirementItemName, dialogueNoItem, dialogueWithItem)
                        game_map.worldAllyList.append(character_sprite)

                        spawnedAlliesKeys.append(battleKey)
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
    spawnedRequirementKeys = []
    if "searchable" in my_map.object_lists:
        item_object_list = my_map.object_lists["searchable"]

        for item_object in item_object_list:
            if "item_key" not in item_object.properties:
                print(
                    f"No 'type' field for character in map {map_name}. {item_object.properties}"
                )
                continue

            itemObjectKey = item_object.properties.get("item_key")
            shape = item_object.shape
            item_sprite = None

            if(isinstance(shape, list) and len(shape)) == 2:
                if(itemObjectKey == "AllyRequirement"):
                    if(len(spawnedAlliesKeys) > 0):
                        print(spawnedAlliesKeys)
                        randomAllyIndex = random.randint(0, len(spawnedAlliesKeys) - 1)
                        allyKeySelected = spawnedAlliesKeys.pop(randomAllyIndex)
                        allyDict = battleCharacter_dictionary[allyKeySelected]
                        print(allyDict)

                        itemKey = allyDict["requirementItemKey"]
                        itemDict = item_dictionary[itemKey]

                        spriteSheet = itemDict["sheet_name"]

                        item_sprite = WorldItem(f":items:{spriteSheet}", itemKey)
                        game_map.worldItemList.append(item_sprite)
                        item_sprite.position = shape


                        spawnedRequirementKeys.append(itemKey)
                else:
                    item_data = worldItem_dictionary[itemObjectKey]
                    availableItemKeys = []
                    for item_key in item_data["item_keys"]:
                        if item_key not in item_dictionary:
                            print(item_key + " no se encuentra en el diccionario de Items.")
                            continue
                        availableItemKeys.append(item_key)

                    randomKeyIndex = random.randint(0, len(availableItemKeys) - 1)
                    itemKey = availableItemKeys[randomKeyIndex]
                    itemDict = item_dictionary[itemKey]
                    spriteSheet = itemDict["sheet_name"]

                    item_sprite = WorldItem(f":items:{spriteSheet}",itemKey)
                    game_map.worldItemList.append(item_sprite)
                    item_sprite.position = shape
            if (item_sprite != None):
                 print(f"Adding item {item_sprite.itemKey} at {item_sprite.position}")
                 game_map.scene.add_sprite("searchable", item_sprite)

  #  if len(spawnedAlliesKeys) > 0:
   #     raise Exception("Existen mas aliados spawneados que items de requerimiento posibles.")

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
def loadMapFromSave(player, saveFile, map_name):
    ally_list = []

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
            "use_spatial_hash": True,
        },
        "rivers_blocking": {
            "use_spatial_hash": True,
        },
        "test_blocking": {
            "use_spatial_hash": True,
        }
    }

    # Read in the tiled map
    path = "../resources/maps/"
    print(f"Loading map: {map_name}")
    my_map = arcade.tilemap.load_tilemap(
        (path + map_name + ".json"), scaling=TILE_SCALING, layer_options=layer_options
    )

    game_map.scene = arcade.Scene.from_tilemap(my_map)

    # Get all the tiled sprite lists
    game_map.map_layers = my_map.sprite_lists

    # Define the size of the map, in tiles
    game_map.map_size = my_map.width, my_map.height

    # Set the background color
    game_map.background_color = my_map.background_color

    game_map.properties = my_map.properties

    try:
        # Este bool define si el mapa es un submapa, es decir, un mapa al que eres teletransportado desde otro mapa.
        # De ser True, se ignora el proceso de verificar si existe start_x y start_y, ya que la posicion de inicio
        # es definida en otro sitio.
        isSubmap = game_map.properties.get("isSubmap")
    except AttributeError:
        raise AttributeError(f"EL MAPA {map_name} NO TIENE DEFINIDA LA VARIABLE 'isSubmap'")
    if (isSubmap == False):
        try:
            print(game_map.properties.get("start_x"), game_map.properties.get("start_y"))
        except AttributeError:
            raise AttributeError(f"EL MAPA {map_name} NO TIENE DEFINIDA UNA POSICION INICIAL X y/o Y.")

    # Any layer with '_blocking' in it, will be a wall
    game_map.scene.add_sprite_list("wall_list", use_spatial_hash=True)
    game_map.scene.add_sprite_list("slowdown_list", use_spatial_hash=True)
    game_map.scene.add_sprite_list("grass_top", use_spatial_hash=True)
    for layer, sprite_list in game_map.map_layers.items():
        if "_blocking" in layer:
            # Eliminar la spritelist original
            game_map.scene.remove_sprite_list_by_object(sprite_list)

            # Crear nueva lista filtrada con solo los que tienen hitbox
            filtered = arcade.SpriteList(use_spatial_hash=True)
            for sprite in sprite_list:
                if sprite.get_hit_box():
                    filtered.append(sprite)
                else:
                    print(f"[AVISO] Sprite ignorado por hitbox vacía en capa '{layer}': {sprite}")

            # Añadir a wall_list
            game_map.scene["wall_list"].extend(filtered)

        if "_slowdown" in layer:
            game_map.scene.remove_sprite_list_by_object(sprite_list)
            game_map.scene["slowdown_list"].extend(sprite_list)
        if layer == "top":
            # game_map.scene.remove_sprite_list_by_object(sprite_list)
            game_map.scene["grass_top"].extend(sprite_list)
    mapBarrierList = None

    f = open("../resources/data/item_dictionary.json")
    item_dictionary = json.load(f)

    f = open("../resources/data/battleCharacters_dictionary.json")
    battleCharacter_dictionary = json.load(f)

    f = open("../resources/data/actions_dictionary.json")
    actions_dictionary = json.load(f)

    for character_object in my_map.object_lists["characters"]:
        if character_object.properties.get("movement") == "boss":
            battleKey = character_object.properties.get("type")

            character_sprite = WorldBoss(f":characters:{battleCharacter_dictionary[battleKey]['sheet_name']}",
                                         game_map.scene, player, [battleKey])
            character_sprite.position = character_object.shape
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa")
            print(character_sprite.position)


    if "worldAllies" in saveFile["maps"][map_name]:
        for worldAlly in saveFile["maps"][map_name]["worldAllies"]:
            battleKey = list(worldAlly.keys())[0]

            allyActions = []
            for action in battleCharacter_dictionary[battleKey]['actions']:
                action_object = Action(actions_dictionary[action]["name"],
                                       actions_dictionary[action]["description"],
                                       actions_dictionary[action]["actionType"],
                                       actions_dictionary[action]["amount"],
                                       actions_dictionary[action]["staminaExpense"],
                                       actions_dictionary[action]["targetQuantity"],
                                       actions_dictionary[action]["effectName"])
                allyActions.append(action_object)

            battleAlly = BattleAlly(battleKey,
                                    f":characters:{battleCharacter_dictionary[battleKey]['sheet_name']}",
                                    battleCharacter_dictionary[battleKey]['name'],
                                    battleCharacter_dictionary[battleKey]['description'],
                                    battleCharacter_dictionary[battleKey]['type'],
                                    battleCharacter_dictionary[battleKey]['maxStamina'],
                                    battleCharacter_dictionary[battleKey]['maxHealth'],
                                    battleCharacter_dictionary[battleKey]['restoredStamina'],
                                    allyActions,
                                    battleCharacter_dictionary[battleKey]['dialogueNoItem'],
                                    battleCharacter_dictionary[battleKey]['dialogueWithItem'],
                                    battleCharacter_dictionary[battleKey]['requirementItemKey'])

            requirementItemName = item_dictionary[
                battleCharacter_dictionary[battleKey]["requirementItemKey"]].get("name")
            dialogueNoItem = battleCharacter_dictionary[battleKey]["dialogueNoItem"]
            dialogueWithItem = battleCharacter_dictionary[battleKey]["dialogueWithItem"]

            character_sprite = WorldAlly(
                f":characters:{battleCharacter_dictionary[battleKey]['sheet_name']}", game_map.scene,
                player, battleAlly, requirementItemName, dialogueNoItem, dialogueWithItem)
            game_map.worldAllyList.append(character_sprite)

            print(worldAlly)
            #WorldAlly tiene la posicion donde aparecer.
            character_sprite.position = worldAlly[battleKey]

            print(f"Adding character ally at {character_sprite.position}")
            print(character_sprite)
            game_map.scene.add_sprite("characters", character_sprite)
    if "worldEnemies" in saveFile["maps"][map_name]:
        for worldEnemy in saveFile["maps"][map_name]["worldEnemies"]:
            # Se crea el enemigo en el nivel.
            # Debug
            print("Creando enemigo con sprite:",f":characters:{worldEnemy['sheetName']}")

            character_sprite = WorldEnemy(worldEnemy['sheetName'],
                game_map.scene, player, worldEnemy["battleEnemies"], worldEnemy["speed"],
                worldEnemy["detectionRadius"], mapBarrierList)
            game_map.worldEnemyList.append(character_sprite)
            character_sprite.position = worldEnemy["position"]

            print(f"Adding character enemy at {character_sprite.position}")
            print(character_sprite)
            game_map.scene.add_sprite("characters", character_sprite)

            if (mapBarrierList == None):
                mapBarrierList = arcade.AStarBarrierList(character_sprite, game_map.scene["wall_list"], 32,
                                                         0,
                                                         game_map.map_size[0] * 32,
                                                         0,
                                                         game_map.map_size[1] * 32)
                character_sprite.cambiar_barrierList(mapBarrierList)

                # Sprites problemáticos sin hitbox
                for i, wall in enumerate(game_map.scene["wall_list"]):
                    hb = wall.get_hit_box()
                    if not hb:
                        print(f"[ERROR] Wall #{i} sin hitbox:", wall)
    if "worldItems" in saveFile["maps"][map_name]:
        for worldItem in saveFile["maps"][map_name]["worldItems"]:
            print(worldItem)
            itemKey = list(worldItem.keys())[0]

            itemDict = item_dictionary[itemKey]
            spriteSheet = itemDict["sheet_name"]

            item_sprite = WorldItem(f":items:{spriteSheet}", itemKey)
            game_map.worldItemList.append(item_sprite)
            #WorldItem tiene la posicion (Lo se, la notacion no tiene sentido, estoy cayendo en la locura)
            item_sprite.position = worldItem[itemKey]
            print(f"Adding item {item_sprite.itemKey} at {item_sprite.position}")
            game_map.scene.add_sprite("searchable", item_sprite)
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
    return game_map

def loadMapsFromSavefile(player, savefilePath):
    saveFile = {}
    with open(savefilePath, "r") as f:
        saveFile = json.load(f)
    print(saveFile)

    loadedMaps = {}
    for mapName in saveFile["maps"]:
        loadedMaps[mapName] = (loadMapFromSave(player, saveFile, mapName))

    f = open("../resources/data/item_dictionary.json")
    item_dictionary = json.load(f)

    f = open("../resources/data/battleCharacters_dictionary.json")
    battleCharacter_dictionary = json.load(f)

    f = open("../resources/data/actions_dictionary.json")
    actions_dictionary = json.load(f)

    currentMapData = [saveFile["currentMapName"],saveFile["playerPosition"]]

    player.player_team = []
    for ally in saveFile["playerTeam"]:
        battleKey = list(ally.keys())[0]

        allyActions = []
        for action in battleCharacter_dictionary[battleKey]['actions']:
            action_object = Action(actions_dictionary[action]["name"],
                                   actions_dictionary[action]["description"],
                                   actions_dictionary[action]["actionType"],
                                   actions_dictionary[action]["amount"],
                                   actions_dictionary[action]["staminaExpense"],
                                   actions_dictionary[action]["targetQuantity"],
                                   actions_dictionary[action]["effectName"])
            allyActions.append(action_object)

        battleAlly = BattleAlly(battleKey,
                                f":characters:{battleCharacter_dictionary[battleKey]['sheet_name']}",
                                battleCharacter_dictionary[battleKey]['name'],
                                battleCharacter_dictionary[battleKey]['description'],
                                battleCharacter_dictionary[battleKey]['type'],
                                battleCharacter_dictionary[battleKey]['maxStamina'],
                                battleCharacter_dictionary[battleKey]['maxHealth'],
                                battleCharacter_dictionary[battleKey]['restoredStamina'],
                                allyActions,
                                battleCharacter_dictionary[battleKey]['dialogueNoItem'],
                                battleCharacter_dictionary[battleKey]['dialogueWithItem'],
                                battleCharacter_dictionary[battleKey]['requirementItemKey'])
        player.player_team.append(battleAlly)

    savedPlayerInventory = []
    for item in saveFile["playerInventory"]:
        itemName = list(item.keys())[0]
        itemToInventory = None
        for itemKey in item_dictionary:
            if item_dictionary[itemKey]["name"] == itemName:
                itemToInventory = item_dictionary[itemKey]
                break

        itemToInventory["amount"] = item[itemName]
        savedPlayerInventory.append(itemToInventory)

    player.inventory = savedPlayerInventory

    return loadedMaps, currentMapData

load_maps.map_file_names = None
load_maps.map_list = None
load_maps.file_count = None
