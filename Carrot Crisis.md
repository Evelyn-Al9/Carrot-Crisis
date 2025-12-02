# Carrot Crisis



Un juego de plataformas verticales creado con Pygame, donde el jugador debe subir por plataformas, recoger monedas y evitar caer. 

El nivel termina al alcanzar la parte superior del mundo.

Incluye:

* Fondo vertical infinito
* Plataformas generadas aleatoriamente
* Monedas funcionales
* Saltos con física
* Pantalla de inicio y pantalla de victoria
* Colisiones perfectas
* Límite inferior que mata al jugador
* Soporte para teclas de flechas y WASD

**Imágenes personalizables para:**

* Fondo
* Plataformas
* Monedas
* Personaje
* Obstáculos



**Estructura del Juego**

carrot crisis/

│  main.py

│  README.md

│

└─ assets/

      bg.png

      player.png

      platform.png

      coin.png

      spikes.png



**Como ejecutar el juego**

**1. Instala Python (3.10 o superior)**

Descargar desde:

https://www.python.org/downloads/



**2. Instala Pygame**

En la terminal o CMD:

pip install pygame



**3. Ejecuta el juego**

python main.py



**Controles**

**Acción	Teclas Primer Nivel**

Mover izquierda	←  o  A

Mover derecha	→  o  D

Saltar	↑  o  W

Iniciar juego	SPACE



**Acción Teclas Segundo Nivel**

Mover izquierda ←  o  A

Mover derecha	→  o  D

Iniciar juego SPACE



**Funcionalidades principales**

* Movimiento suave y salto reactivo
* Gravedad configurable
* Fondo infinito vertical
* Plataformas con separación segura
* Monedas que desaparecen al tomarlas
* Vidas
* Pantalla de inicio (menú)
* Pantalla final “¡Nivel completo!”
* Scroll vertical automático al subir



**Personalización**

**Puedes reemplazar las imágenes dentro de la carpeta assets/:**

bg.png → fondo infinito

player.png → personaje

platform.png → plataformas

coin.png → monedas

spikes.png → obstáculo en el piso



**Las imágenes deben ser formato .png y preferiblemente:**



Fondo: 800×600

Personaje: 40×50

Plataforma: 150×20

Moneda: 20×20



**Configuraciones Importantes**

**Puedes ajustar parámetros en main.py:**

GRAVITY = 1

JUMP\_FORCE = -18

PLAYER\_SPEED = 6

platform\_gap = 140







