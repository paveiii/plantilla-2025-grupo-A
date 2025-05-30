# Memoria

## No Time Left

**Organizacion del equipo**

- Pável David Tabata Rodríguez: Jefatura de proyecto, Programación, Pruebas 
- Beatriz Arribas Schudeck: Diseño Gráfico, Pruebas.
- Daniel Guillén Ruiz: Diseño gráfico, Pruebas, Diseño de niveles, Programación. 
- Pablo Álvaro Peña Sánchez: Diseño Gráfico, Diseño de niveles, Pruebas .
- Rubén Dobre: Programación, Pruebas.
- Samuel García de Dios: Programación, Pruebas, Diseño de niveles 

El equipo fue organizado basado en sus habiliades y debilidades destacables, pero todos terminamos aportando nuestro grano de arena en tareas que no terminaban siendo nuestra especialidad. La comunicación interna se mantuvo principalmente por un grupo de Whatsapp, sin embargo se mantenia un control de las tareas por medio de Github Issues. Debido a la dificultad de las tareas, el jefe de proyecto intentaba mantener fechas límite o "Deadlines" internas basado en una aproximación de cuanto tiempo se tardaría para realizar una cosa u otra, dichas fechas fueron movidas basado en los resultados y la disponibilidad de los miembros, haciendo que algunas tareas se extendieran por tiempos prolongados en favor de tener un producto mucho más completo.

El elemento más complicado durante el desarrollo fue el arte para el proyecto, al no tener la experiencia el tiempo suficiente para desarrollar una estética propia, tuvimos que echar mano de distintos recursos de uso libre y generación por inteligencia artificial. Las fuentes principales fueron:
* [OpenGameArt.org](https://opengameart.org/): Un repositorio de Assets que pueden ser usados gratuitamente en proyectos, principalmente de código abierto.
* * [Liberated Pixel Cup](https://lpc.opengameart.org/): La vasta cantidad de enemigos y aliados que fueron creados no sería posible sin el trabajo creado por los artistas que participaron en este evento. para esta competición.
* [Universal LPC Spritesheet Generator](https://liberatedpixelcup.github.io/Universal-LPC-Spritesheet-Character-Generator/#?body=Body_color_light&head=Human_male_light): Software que usamos para generar los personajes usando los Assets de la Liberated Pixel Cup.
* [Craftpix Free Rocky Area Objects Pixel Art]([https://opengameart.org/](https://craftpix.net/freebies/free-rocky-area-objects-pixel-art/?srsltid=AfmBOopkGluWB6UjM03wZRjRUa0K62cL9j9jErPmHgEuThCgQvgjc1IO))
* [Craftpix Free Undead Tileset Top Down Pixel Art](https://craftpix.net/freebies/free-undead-tileset-top-down-pixel-art/?srsltid=AfmBOoo7ri7NnaXeE4C__u1hMCTA2qNxYZUtaeUAAjYyj78FK2Dx3Q6W)
* [Craftpix Top-Down Crystals Pixel Art](https://craftpix.net/freebies/top-down-crystals-pixel-art/?srsltid=AfmBOorE1fXsdHP2tWeCCsgfepVGB1b__Z1YOfjy0O1LW9Q8VHOUhvwL)
* [Craftpix Free Rocks and Stones Top-Down Pixel Art](https://craftpix.net/freebies/free-rocks-and-stones-top-down-pixel-art/?srsltid=AfmBOor2wo8v8i414nPk-Ex8Ey1CGRuFsQ4pdW6rHDU3HY9xAGrPpUk_)
* [rectTile Universe Basic Dirt](https://dkproductions.itch.io/recttile-universe-basic-dirt)

**Principales objetivos implementados**
* Interfaz del inventario mejorado.
* 
* Musica ambiental.
* La interfaz ha sido trabajada para darle al jugador todas las herramientas que necesita para logaraUna interfaz que cuenta con una pantalla individual de batalla, junto con un inventario renovado, musica ambiental para cada nivel adecuada a la época a la que queremos emular  y una pantalla de inicio totalmente nueva.
  
*  Un sistema de batalla basado en botones de acción, con los que el jugador puede interactuar para atacar a sus enemigos. Implementados también varias opciones de uso de estos mismos ataques, así como la capacidad de no hacer ningún movimiento para la recuperación de vida y barra de poder.
*  Sistema de reclutamiento por el cual el jugador puede añadir a su arsenal otros personajes que también lucharán contra enemigos. 
*  Diseño  e implementación de las tres fases con las que cuenta el boss a lo largo de los tres niveles.
*  Cajas de diálogos que se muestran cada vez que el jugador intente reclutar a otro personaje que, además, cumple con la función de ilustrar la historia y formar un hilo conductor a lo largo de la aventura. Sin embargo, estos están predeterminados y el jugador no puede elegirlos libremente. 
*  Diseño de tres niveles, que cumplen con la estética inicial de recrear tres etapas diferentes del tiempo. 
*  Implementación de las animaciones de los sprites, que permiten una mejor visualizacion de los movimientos tanto de los aliados como de los enemigos, sus ataques y sus defensas.
*  Sistema de guardado que recuerda la posición, inventario, miembros reclutados, mapa, items y enemigos.
*  Implementación del Spawn del objeto especial de requerimiento, que los personajes reclutables exigirán para poder acompañar al jugador en el resto de aventura. Además de otros adicionales que pueden llegar a usarse en batalla. 
*  Aleatoriedad de personajes, que permite la rejugabilidad. Una vez acabado y vuelto a iniciar, el jugador no sabrá de antemano que personajes puede llegar a encontrarse en cada mapa y que objetos requerirán.
*  IA de los enemigos: una vez que detectan que el jugador está muy próximo a ellos, comienzan a perseguirle hasta que entran en batalla.

**Lo que no se hizo**

Lamentablemente gran parte de las ideas adicionales que teníamos no han podido ser llevadas a cabo: 

* No fue posible agregar ataques múltiples ni últimates. 
* Un menú principal en el que el jugador pudiese elegir el tipo de indumentaria. 
* Un sistema de logros con recompensas adicionales. 
* Una tienda de compra de armamento, vestimenta y objetos especiales, así como el traductor universal comerciable.
* KnockBack
* Aprendizaje de habilidades nuevas según se superan las batallas.
* Capacidad de dialogar con enemigos. 

**Aspectos tecnicos destacables**

**Información adicional**
