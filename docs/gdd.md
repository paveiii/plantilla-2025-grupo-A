# Documento de diseño

## No Time Left

**INTRODUCCIÓN**

No Time Left es un un videojuego RPG indie con mecanicas de batallas estratégicas entre equipos, manejo de Items y variedad de enemigos y personajes basado en RNG.

**OBJETIVOS** 

Vence a los enemigos y derrota finalmente a Sorus para evitar las paradojas temporales y la fracturación de la realidad.

**HISTORIA**

Año 2089, la humanidad está en el apogeo del proceso tecnológico y ha logrado viajar en el tiempo tras la invención del acelerador de partículas. Temporis Lex, una agencia gubernamental creada para detectar y contener amenazas temporales, ha detectado fuertes anormalidades en la línea temporal pricipal.

Nuestro protagonista, el mejor agente de la agencia con más de 1250 misiones exitosas, le ha sido encomendada la ardua tarea de reparar el tiempo. A través de múltiples épocas, luchará contra enemigos que han sido desviados de su tiempo. Reclutará a personas de diferentes épocas y se enfrentará a la criatura que orquesta todos los movimientos de los sujetos que han huido de su tiempo.

Es esencial para la supervivencia de nuestro tiempo tal y como lo conocemos reparar la principal línea temporal, si fracasa toda la raza humana se sumiría en una paradoja y bucles temporales donde estaríamos condenados a repetir este proyecto por el resto de nuestros dias...

**PERSONAJES**

Nuestro protagonista ha sido escrito deliberadamente para no tener características únicas o bien definidas, dado a que es considerado como un "avatar" del jugador, lo importante no es él, sino lo que va a hacer. El jugador controla a este personaje y junto a este se podrán unir otros personajes o aliados formando un equipo. Dichos personajes solo serán reclutados bajo el requisito de primero encontrar en el mapa un objeto especifico y darselos, dicho objeto estará relacionado a la caracterización de dicho aliado. Los aliados podrán ayudar al jugador acabando con los enemigos que se encuentren. El equipo tendrá un máximo de 3 aliados que el jugador podrá llevar, se podrá reemplazar a un aliado en caso de querer aceptar un aliado nuevo.

Como extra para favorecer la estética del juego y mayor comprensión de la historia, se tiene el personaje que es el encargado de la agencia, el cual nos indicará nuestro propósito y misión. También se llevará a cabo el diseño de varios NPC´s para dar ambiente a las distintas líneas temporales encontradas en el juego. El boss final, nuestra criatura ancestral, que es la razón última de nuestro viaje temporal. 

**ALIADOS**

La esencia del juego son las batallas que hay que librar para salir con vida tras enfrentarse a los enemigos. Estos son combates en los que todos los personajes permanecen estáticos y solo se permite actuar mediante botones para seleccionar items y ataques.\
Cada uno está dotado de su propia barra de vida y capacidad de ataque, que pude alcanzar hasta un maximo de tres.\
Los personajes cuentan con sus propios ataques, porcentaje de vitalidad y daño.\
Existen varias opciones con las que seguir una estrategia a la hora de enfrentarse a algún enemigo. Dependiento de quien ataque y quien es atacado, el daño es mayor, la vida se regenera más rápido, la recuperación de la habilidad de ataque es inmediata dependiendo de si se emplea o no, valoraciones de daño en caso de ser atacado  etc. Teniendo siempre presente que las estadísticas se mantienen después de cada confrontación.

Los aliados tendrán habilidades únicas dependiendo de su "clase",  imitación de varios arquetipos de diferentes épocas y tiempos intentando implementar lo que se espera ficcionalmente de ellos. Dichas clases se separarán en las siguientes:


* Tanque: Puntos de vida máximos elevado, poca recuperacion de Stamina. Efectos secundarios adicionales.
* Guerrero: Puntos de vida moderados, daño alto, Stamina moderada.
* Curandero: No tiene ataques, solo curar o revivir.
* Mago: Ataques con efecto.
* Asesino: Stamina alta, puntos de vida moderados y poco daño. Con la particularidad de tener doble turno.
* Capitan: Efecto grupal y ataques moderados.

**ENEMIGOS**

Los enemigos están diseñados para perseguir al personaje y al colisionar con estos, comienza una batalla. Los enemigos nunca atacan solos, siempre lo hacen en grupo, y cada integrante emplea su propia barra de "Stamina" que se recarga con cada turno. Esta se emplea para tomar decisiones sobre cómo actuar. Su modus operandi es atacar según el criterio de: rival mas débil, seguido de los medico o lideres, personajes con mucha vida y por último al protagonista. De no tener un criterio claro, ataca al azar. Para el jefe final, este usará varios ataques normales hasta cargar un ataque especial, dicho ataque especial puede reiniciarse haciendo suficiente daño en un solo turno.

**MECÁNICAS**

*   Sistema de batalla en una ventana separada: donde ocurre la batalla por turnos contra el equipo de enemigos que nos hayamos encontrado. Permite la elección de cómo actuar por aliado: ataque a un solo enemigo, ataque a varios enemigos, curar a un aliado o a varios y revivir a un aliado. Tras el turno del jugador, los enemigos actuarán acorde lo que indique la IA del equipo enemigo.
*   Guardado de partida manual y automático.
*   Por cada nivel, el jefe final tomará una forma final, evolucionando su apariencia y ataques hasta alcanzar su fase final. Aumenta la dificultad por cada nivel.
*   El equipo del jugador tendrá la capacidad de añadir hasta tres miembros, con los cuales se puede interaccionar como otorgándoles objetos.
*   Cajas de diálogos predeterminados
*   Opciones para hablar con otros personajes con el fin de reclutarlos: en lugar de usar un objeto de reclutamiento, se podrá optar por reclutar a un personaje por medio opciones de dialogo que el jugador eligirá, cada una tiene una posibilidad de terminar reclutando al personaje de forma exitosa.
*   Aprendizaje de habilidades nuevas.
*   Selección en el menú principal de "skin": permitirá que el personaje del jugador tenga una apariencia distinta a la predeterminada.
*   Ataques combinados: ataques donde dos o más aliados combinan fuerzas para dar paso a un ataque mucho más poderoso.
*   Ataques "ultimates": ataques más fuertes que se cargan tras un tiempo.
*   Logros: emblemas que los jugadores podrán desbloquear cuando realicen ciertas acciones en el juego.
*   Tienda de objetos y vestimentas: en los diferentes mapas habrán tiendas en las que el jugador podrá comprar y vender objetos utilizando una moneda del juego. Se podrá vender objetos como el "Traductor Universal" que usa el protagonista para comunicarse con los otros personajes reclutables, de hacer esto se recibiría una enorme suma de dinero, pero el jugador sería incapaz de reclutar a otros personajes.
*   Habilidad de correr a alta velocidad (Sprint)
*   Knockback: ciertos enemigos pueden empujar al jugador en varias direcciones haciendo daño en el proceso.

**SECUENCIA DE NIVELES**

*   Tres niveles, cada nivel terminará con una batalla contra el jefe.
*   La ambientación de cada nivel estará acorde con cada línea temporal: Medieval, Futurista y Prehistórico.
*   Habrán items distribuidos alrededor del mapa que ayudarán al jugador durante las batallas.
*   NPC´s ocultos.
*   Diseño abierto y diferentes caminos. 

**ESTÉTICA**

*   Diversos personajes con escenarios únicos y diseños acordes a las épocas que representan.
*   Pixel-Art (64x64).








