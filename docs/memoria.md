# No Time Left - Memoria

## Organizacion del equipo

- Pável David Tabata Rodríguez: Jefatura de proyecto, Programación, Pruebas 
- Beatriz Arribas Schudeck: Diseño Gráfico, Pruebas.
- Daniel Guillén Ruiz: Diseño gráfico, Pruebas, Diseño de niveles, Programación. 
- Pablo Álvaro Peña Sánchez: Diseño Gráfico, Diseño de niveles, Pruebas .
- Rubén Dobre: Programación, Pruebas.
- Samuel García de Dios: Programación, Pruebas, Diseño de niveles 

El equipo fue organizado basado en sus habiliades y debilidades destacables, pero todos terminamos aportando nuestro grano de arena en tareas que no terminaban siendo nuestra especialidad. La comunicación interna se mantuvo principalmente por un grupo de Whatsapp, sin embargo se mantenia un control de las tareas por medio de Github Issues. Debido a la dificultad de las tareas, el jefe de proyecto intentaba mantener fechas límite o "Deadlines" internas basado en una aproximación de cuanto tiempo se tardaría para realizar una cosa u otra, dichas fechas fueron movidas basado en los resultados y la disponibilidad de los miembros, haciendo que algunas tareas se extendieran por tiempos prolongados en favor de tener un producto mucho más completo.

El elemento más complicado durante el desarrollo fue el arte para el proyecto, al no tener la experiencia el tiempo suficiente para desarrollar una estética propia, tuvimos que echar mano de distintos recursos de uso libre y generación por inteligencia artificial. Las fuentes principales fueron:
* [OpenGameArt.org](https://opengameart.org/): Un repositorio de Assets que pueden ser usados gratuitamente en proyectos, principalmente de código abierto.
* [Liberated Pixel Cup](https://lpc.opengameart.org/): La vasta cantidad de enemigos y aliados que fueron creados no sería posible sin el trabajo creado por los artistas que participaron en este evento. para esta competición.
* [Universal LPC Spritesheet Generator](https://liberatedpixelcup.github.io/Universal-LPC-Spritesheet-Character-Generator/#?body=Body_color_light&head=Human_male_light): Software que usamos para generar los personajes usando los Assets de la Liberated Pixel Cup.
* [Pipoya Free RPG Tileset 32x32](https://pipoya.itch.io/pipoya-rpg-tileset-32x32)
* [Pipoya Free RPG Character Sprites 32x32](https://pipoya.itch.io/pipoya-free-rpg-character-sprites-32x32)
* [Kenney Input Prompts Pixel 16x16](https://kenney.nl/assets/input-prompts-pixel-16)
* [UI Pack - Pixel Adventure](https://kenney.nl/assets/ui-pack-pixel-adventure)
* [Craftpix Free Rocky Area Objects Pixel Art]([https://opengameart.org/](https://craftpix.net/freebies/free-rocky-area-objects-pixel-art/?srsltid=AfmBOopkGluWB6UjM03wZRjRUa0K62cL9j9jErPmHgEuThCgQvgjc1IO))
* [Craftpix Free Undead Tileset Top Down Pixel Art](https://craftpix.net/freebies/free-undead-tileset-top-down-pixel-art/?srsltid=AfmBOoo7ri7NnaXeE4C__u1hMCTA2qNxYZUtaeUAAjYyj78FK2Dx3Q6W)
* [Craftpix Top-Down Crystals Pixel Art](https://craftpix.net/freebies/top-down-crystals-pixel-art/?srsltid=AfmBOorE1fXsdHP2tWeCCsgfepVGB1b__Z1YOfjy0O1LW9Q8VHOUhvwL)
* [Craftpix Free Rocks and Stones Top-Down Pixel Art](https://craftpix.net/freebies/free-rocks-and-stones-top-down-pixel-art/?srsltid=AfmBOor2wo8v8i414nPk-Ex8Ey1CGRuFsQ4pdW6rHDU3HY9xAGrPpUk_)
* [rectTile Universe Basic Dirt](https://dkproductions.itch.io/recttile-universe-basic-dirt)
* [Pixabay](https://pixabay.com/music/)

El jefe fue diseñado y dibujado por Beatriz Arribas, junto al diseño de los primeros aliados. Quien desarrollo arte conceptual durante el desarrollo:
![image](https://github.com/user-attachments/assets/47eefc12-6854-4277-baa4-01c7ad2414a4)
![image](https://github.com/user-attachments/assets/0bb3fa36-ebbd-41e8-80d2-d459544ed845)
![image](https://github.com/user-attachments/assets/e8741a60-0109-4e1a-8ece-720173df6587)
![image](https://github.com/user-attachments/assets/5219b329-292d-4455-856d-07e4f0cf14eb)

El mapa Cyberpunk recibió la mayoría de arte por parte de generación por Inteligencia Artificial, sin embargo, Pablo Peña tuvo que arreglar bastante de los diseños generados al ser deficientes de una forma u otra. Para el arte de pantallas también se usó IA.

## Principales objetivos implementados
*  **Un sistema de batalla basado en turnos**\
  Donde el jugador puede dirigir los ataques que realizan sus aliados al equipo enemigo. También se pueden usar items que el jugador encuentra por el mapa, ya sea con una función defensiva como también una funcion ofensiva. Se han implementado distintos tipos de ataques y habilidades, utilizando diccionarios en.json para almacenar la información de estos. También el jugador tiene la posibilidad de no realizar ningún movimiento y recuperar mucha más Stamina.
  
*  **Aliados y Sistema de reclutamiento de aliados**\
   Los aliados se encontrarán estacionados en un punto del mapa específicado por el diseñador, dichos puntos pueden contener a más de un aliado posible, que será elegido aleatoriamente. El jugador podrá reclutar a dichos aliados buscando en el mapa un "Objeto de requerimiento", nombre interno dado por el equipo, el cual aparece aleatoriamente alrededor del mapa en puntos específicos, en cuanto el jugador tenga este objeto, podrá reclutar al personaje y usarse en batalla. Cada aliado tiene habilidades únicas que fueron puestas dependiendo de su clase. En caso de que se intente reclutar a más de tres aliados, se dará la elección al jugador de reemplazar alguno de los que ya tiene por el nuevo que va a entrar en el equipo, aún asi se dará la posibilidad al jugador de volver a reclutar dicho personaje, dejando su objeto de requerimento en el suelo.
   
*  **Cajas de diálogos de aliados**\
   Los aliados comunicarán la exigencia del objeto de reclutamiento y su satisfacción una vez encuentres dichos objetos por medio de dialogos mostrados en cajas de texto. Estos cumplen con la función adicional de ilustrar a estos personajes y formar un hilo conductor a lo largo de la aventura.
   
* **Enemigos e Inteligencia Artificial en batalla**
   Los enemigos aparecen similiar a los aliados, aleatoriamente basado en una lista de posibles enemigos de batalla, junto a esto también tienen predefinido atributos como la velocidad, radio de detección y la cantidad de enemigos que pueden aparecer en su equipo en la batalla. Estos se situan por el mapa utilizando la solución de PathFinding A* nativa de Arcade, seguirán al jugador en cuanto este entre dentro de su rango de detección. Una vez en combate, estos luchan basado a un críterio mucho más simple al planteado al GDD, esta vez seleccionando al azar un aliado y atacando, esto se repetirá por cada integrante del equipo enemigo hasta terminar su turno. Una vez el jugador gana, vuelve la pantalla del mapa, en caso contrario el jugador se le mostrará una pantalla de Game Over.\
  Para el Pathfinding usamos de referencia este [video de Charlie Smith](https://www.youtube.com/watch?v=nh0DHdX11oE&ab_channel=CharlieSmith)
  
* **Sistema de aparición de objetos extendido**\
  Ahora pueden salir objetos aleatoriamente tomando de una lista predefinida en un diccionario. Haciendo que cada sesión sea única.\
  
* **Interfaz del inventario mejorado**\
  Posee información sobre los items que carga y los aliados que posee actualmente en su equipo.\
  
* **Musica ambiental y para batallas**.
* **Diseño original  e implementación de las tres fases con las que cuenta el boss a lo largo de los tres niveles.**
* **Tres niveles con la ambientación definida en el GDD**
* **Implementación de animaciones de Sprites**
* **Sistema de guardado manual del Game State del jugador**
  

## Sistemas descartados o modificados
Muchas ideas tuvieron que ser desechadas o modificadas durante el proyecto. Algunas de las más destacables fueron:

* **Una tienda de compra de armamento, vestimenta y objetos especiales, Así como el traductor universal comerciable.**
* **Un menú principal en el que el jugador pudiese elegir el tipo de indumentaria.**\
* **Aprendizaje de habilidades nuevas según se superan las batallas.**\
* **Un sistema de logros con recompensas adicionales.**\
* **KnockBack**\
  No fueron tomados como una prioridad desde el inicio.
* **Ataques múltiples ni últimates.**
  La falta de tiempo y de un diseño convincente fue lo que nos hizo echar para atras esta idea. Dejando un sistema de combate más simple.
* **Dialogar con NPCs**
  La implementación actual de la caja de texto para los items de reclutamiento es muy poco flexible, al punto que no puede ser reciclada para hacer que aparezca arbitrariamente sin hacer vueltas para evitar el problema base. Este problema fue notado muy tarde durante el desarrollo, dando como resultado que se desechara esta idea.
* **Reclutar a personajes por medio de convencimiento**
  Un tanto relacionado con el punto anterior pero fue más por no ser una prioridad, al considerarse muy complejo y con muchos casos de error probables.
* **IA de enemigos en batalla más inteligente**
  La idea de que el equipo enemigo ataque a los aliados de forma estrategica basandose en sus tipos e información fue implementado bastante temprano en el desarrollo, al menos en forma de funciones que devuelven numeros. Sin embargo el desarrollo extendido de la pantalla de batalla ocasionó que su implementación se hiciera bastante tarde durante el desarrollo, provocando que tuvieramos que simplificar el sistema.

Un factor importante para estas complicaciones durante el desarrollo fue la falta de experiencia por parte de los miembros del equipo, tanto con el motor de juego que utilizabamos como el proceso general detras del desarrollo de un videojuego. Con el tiempo ajustamos no consideramos completamente todas las facetas que iba a tener implementar algunas de las mecanicas que fueron planteadas en el GDD, ni mucho menos pensamos a largo plazo que efecto iban a tener con otros sistemas implementados. Ha sido una gran enseñanza sobre nunca subestimar el tiempo que puede tomar diseñar, implementar y probar una característica, especialmente en un desarrollo tan transversal como puede ser el desarrollo de un videojuego, aun siendo tan simple como este.

También la puesta de prioridad sobre cada tarea es algo que falló por parte de la dirección del proyecto, tareas como la creación de los mapas no debieron haber sido dedicadas tanto tiempo como puede ser la implementación de sistemas base en el juego. El tiempo es el que tenemos y lo mejor que se puede hacer es hacer lo máximo con lo minimo que tengas.

Por último, si bien se intentó mantener una comunicación activa entre los miembros del proyecto, ciertamente hubo épocas donde miembros se encontraban aislados trabajando en características escasamente definidas o atendiendo a otras cuestiones personales. Nos guste o no, siempre tenemos que estar pendiente del trabajo de los demás, y cuestionar por qué algo se hace de una forma u otra y si esto podría tener conflictos a futuro, es la mejor forma de trabajar.
