Carrot Crisis

Un juego de plataformas verticales creado con Pygame, donde el jugador debe subir por plataformas, recoger monedas y evitar caer.
El nivel termina al alcanzar la parte superior del mundo.
Incluye:
⦁	Fondo vertical infinito
⦁	Plataformas generadas aleatoriamente
⦁	Monedas funcionales
⦁	Saltos con física
⦁	Pantalla de inicio y pantalla de victoria
⦁	Colisiones perfectas
⦁	Límite inferior que mata al jugador
⦁	Soporte para teclas de flechas y WASD
Imágenes personalizables para:
⦁	Fondo
⦁	Plataformas
⦁	Monedas
⦁	Personaje
⦁	Obstáculos

Estructura del Juego

Nivel #1:

carrot crisis/
│  Nivel 1.Carrot Crisis.py
│
└─ assets/
      bg.png
      player.png
      platform.png
      coin.png
      spikes.png

Nivel #2:

carrot crisis 2/
│  Nivel 2 (Catch or Crash).py
|--FontsPressStart2P.ttf
│
└─ assets/
      bad.ending.png
      good.ending.png
      level.2.background.png
      carrot.coin.png
      Menuu.background.png
      player.png
      second.level.background.png
      


Como ejecutar el juego
1. Instala Python (3.10 o superior)
Descargar desde:
https://www.python.org/downloads/

2. Instala Pygame
En la terminal o CMD:
pip install pygame

3. Ejecuta el juego
Nivel 1.Carrot Crisis.py
Nivel 2 (Catch or Crash).py

Controles
Acción	Teclas Primer Nivel
Mover izquierda	←  o  A
Mover derecha	→  o  D
Saltar	↑  o  W o SPACE
Iniciar juego	SPACE or Enter

Acción Teclas Segundo Nivel
Mover izquierda ←  o  A
Mover derecha	→  o  D
Iniciar juego SPACE

Funcionalidades principales
⦁	Movimiento suave y salto reactivo
⦁	Gravedad configurable
⦁	Fondo infinito vertical
⦁	Plataformas con separación segura
⦁	Monedas que desaparecen al tomarlas
⦁	Vidas
⦁	Pantalla de inicio (menú)
⦁	Pantalla final “¡Nivel completo!”
⦁	Scroll vertical automático al subir

Personalización
Puedes reemplazar las imágenes dentro de la carpeta assets/:
bg.png → fondo infinito
player.png → personaje
platform.png → plataformas
coin.png → monedas
spikes.png → obstáculo en el piso

Las imágenes deben ser formato .png y preferiblemente:

Fondo: 800×600
Personaje: 40×50
Plataforma: 150×20
Moneda: 20×20

Configuraciones Importantes
Puedes ajustar parámetros en main.py:

Nivel #1: 

GRAVITY = 1
JUMP_FORCE = -18
PLAYER_SPEED = 6
platform_gap = 140

PLAYER_SPEED = 4
JUMP_POWER = 17
GRAVITY = 0.9
COYOTE_TIME = 0.12
JUMP_BUFFER = 0.12

LEVEL_HEIGHT = 6000
START_LIVES = 500
COIN_SCORE = 10

# Generador ajustado
MIN_PLAT_W, MAX_PLAT_W = 110, 150
PLAT_H = 18
PLAT_X_MARGIN = 24
PLAT_MIN_GAP = 120
PLAT_MAX_GAP = 130
MAX_SHIFT = 180
COIN_CHANCE = 6
SPIKE_CHANCE = 2
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Vertical Platformer")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 26)
big_font = pygame.font.SysFont(None, 40)
small_font = pygame.font.SysFont(None, 20)
