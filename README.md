# No Time Left

## Equipo
- Pável David Tabata Rodríguez: Jefatura de proyecto, Programación, Pruebas 
- Beatriz Arribas Schudeck: Diseño Gráfico, Pruebas.
- Daniel Guillén Ruiz: Diseño gráfico, Pruebas, Diseño de niveles, Programación. 
- Pablo Álvaro Peña Sánchez: Diseño Gráfico, Diseño de niveles, Pruebas.
- Rubén Dobre: Programación, Pruebas.
- Samuel García de Dios: Programación, Pruebas, Diseño de niveles.


En un futuro donde la barrera del tiempo ha sido superada, surge una agencia destinada a arreglar las lineas temporales dañadas por sujetos desviados de su lugar espacio-temporal. Estos vagan a través del tiempo causando problemas que traeran consigo graves consecuencias, sirviendo órdenes de una criatura ancestral a la que llaman Sorus...

## Gameplay
"No time left" es un divertido juego en el que tendrás que aventurarte por distintas épocas recogiendo objetos, luchando contra temibles enemigos y reclutando a distintos personajes que te ayudarán en tu propósito

**Explora distintas épocas**


![img_16.png](img_16.png)  


**Recluta compañeros**

Hacerte con buenos aliados será la clave para el éxito de la tarea que se te ha encomendado.

![img_17.png](img_17.png)

**Consulta tu armamento y recoge objetos valiosos**

Existen varios objetos que te servirán en tu trepidante aventura. Recógelos y consúltalos siempre que lo necesites.

![img_18.png](img_18.png)

**Y enfrenta tu destino**

![img_19.png](img_19.png)

The game is in extremely early stages. For discussion on future direction, see:
* [the github discussion board](https://github.com/pythonarcade/community-rpg/discussions).
* [the #community-ideas channel on Arcade's discord server](https://discord.com/channels/458662222697070613/704736572603629589)

This is an open-source RPG game.

* Everything is open-source, under the permissive MIT license.
* Libraries Used:
  * [Arcade](https://github.com/pythonarcade/arcade)
  * [Pyglet](https://github.com/pyglet/pyglet)
  * [pytiled_parser](https://github.com/pythonarcade/pytiled_parser)
* Maps are created with the [Tiled Map Editor](https://mapeditor.org)
* All code is written in Python

Graphics Assets From:
* [Pipoya Free RPG Tileset 32x32](https://pipoya.itch.io/pipoya-rpg-tileset-32x32)
* [Pipoya Free RPG Character Sprites 32x32](https://pipoya.itch.io/pipoya-free-rpg-character-sprites-32x32)
* [Kenney Input Prompts Pixel 16x16](https://kenney.nl/assets/input-prompts-pixel-16)



### Controles
- **Movement:** Arrow Keys / WASD
- **Toggle Light/Torch:** F
- **Pick Up Items:** E
- **Open Inventory:** I
- **Open Menu:** ESC

## Development

This project targets Python 3.7 or greater.

To install the project and all development dependencies run the following command, this should ideally be done in a [virtual environment](https://docs.python.org/3/tutorial/venv.html):

```bash
pip install -e ".[dev]"
```

The game can then be ran with:

```bash
python -m rpg
```
