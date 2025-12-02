import pygame
import random
import os
import sys
from pygame.math import Vector2

pygame.init()

# ---------- CONFIG ----------
W, H = 550, 750
FPS = 60

ASSETS = "assets"
PLAYER_IMG = os.path.join(ASSETS, "player.png")
COIN_IMG   = os.path.join(ASSETS, "coin.png")
PLATFORM_IMG = os.path.join(ASSETS, "platforms.png")
SPIKE_IMG  = os.path.join(ASSETS, "spikes.png")

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Juego con Fondo Infinito")

#Parte en donde se cambia el fondo#
background = pygame.image.load("assets/bg.png").convert()
background = pygame.transform.scale(background, (W, H))

#Velocidad el fondo#
bg_y = 0
bg_scroll_speed = 2

#Velocidad de jugador y otros#
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

def load_img(path, size=None):
    try:
        img = pygame.image.load(path).convert_alpha()
        if size:
            img = pygame.transform.smoothscale(img, size)
        return img
    except:
        return None

player_img = load_img(PLAYER_IMG)
coin_img = load_img(COIN_IMG)
plat_img = load_img(PLATFORM_IMG)
spike_img = load_img(SPIKE_IMG)

# ---------- SPRITES ----------
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w):
        super().__init__()
        if plat_img:
            self.image = pygame.transform.smoothscale(plat_img, (w, PLAT_H))
        else:
            self.image = pygame.Surface((w, PLAT_H))
            self.image.fill((140, 90, 50))
        self.rect = self.image.get_rect(topleft=(x, y))

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        if coin_img:
            self.image = pygame.transform.smoothscale(coin_img, (26, 26))
        else:
            s = pygame.Surface((26,26), pygame.SRCALPHA)
            pygame.draw.circle(s, (255,215,0), (13,13), 12)
            self.image = s
        self.rect = self.image.get_rect(center=(x, y))

class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        if spike_img:
            self.image = pygame.transform.smoothscale(spike_img, (20,20))
        else:
            s = pygame.Surface((28,28), pygame.SRCALPHA)
            pygame.draw.polygon(s, (200,20,20), [(0,28),(14,0),(28,28)])
            self.image = s
        self.rect = self.image.get_rect(midbottom=(x, y))

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        if player_img:
            self.image = pygame.transform.smoothscale(player_img, (40, 25))
        else:
            s = pygame.Surface((36,48), pygame.SRCALPHA)
            pygame.draw.rect(s, (50,130,220), (0,0,36,48))
            self.image = s

        self.rect = self.image.get_rect(topleft=(x, y))
        self.pos = Vector2(x, y)
        self.vel = Vector2(0, 0)
        self.on_ground = False
        self.coyote = 0
        self.jump_buffer = 0
        self.lives = START_LIVES
        self.score = 0

    def update(self, dt, platforms, keys):
        prev_bottom = self.rect.bottom

        # Movimiento horizontal
        dx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx += 1
        self.vel.x = dx * PLAYER_SPEED

        # Gravedad
        self.vel.y += GRAVITY
        if self.vel.y > 20:
            self.vel.y = 20

        # Jump buffer
        if keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]:
            self.jump_buffer = JUMP_BUFFER
        else:
            self.jump_buffer -= dt

        # Coyote time
        if self.on_ground:
            self.coyote = COYOTE_TIME
        else:
            self.coyote -= dt

        # Saltar
        if self.jump_buffer > 0 and self.coyote > 0:
            self.vel.y = -JUMP_POWER
            self.jump_buffer = 0
            self.coyote = 0
            self.on_ground = False

        # Mover en X
        self.pos.x += self.vel.x
        self.rect.x = int(self.pos.x)

        hits = pygame.sprite.spritecollide(self, platforms, False)
        for p in hits:
            if self.vel.x > 0:
                self.rect.right = p.rect.left
            elif self.vel.x < 0:
                self.rect.left = p.rect.right
            self.pos.x = self.rect.x

        # Mover en Y
        self.pos.y += self.vel.y
        self.rect.y = int(self.pos.y)
        self.on_ground = False

        hits = pygame.sprite.spritecollide(self, platforms, False)
        for p in hits:
            if self.vel.y > 0 and prev_bottom <= p.rect.top + 4:
                self.rect.bottom = p.rect.top
                self.pos.y = self.rect.y
                self.vel.y = 0
                self.on_ground = True
            elif self.vel.y < 0:
                self.rect.top = p.rect.bottom
                self.pos.y = self.rect.y
                self.vel.y = 0

bg_y += bg_scroll_speed
if bg_y >= H:
    bg_y = 0

screen.blit(background, (0, bg_y))
screen.blit(background, (0, bg_y - H))

# ---------- Level generator (vertical hacia arriba) ----------
class LevelGenerator:
    def __init__(self, world_bottom):
        self.generated_y = world_bottom   # empezamos en la parte baja (valor grande)
        self.platforms = []   # list of (x,y,w)
        self.coins = []       # list of (cx,cy)
        self.spikes = []      # list of (sx,sy)
        # seed last_x con algo variable para diversidad
        self.last_x = random.randint(PLAT_X_MARGIN, W - PLAT_X_MARGIN - MIN_PLAT_W)

    def generate_until(self, y_limit):
        # genera plataformas mientras generated_y > y_limit
        # se asegura separación vertical, variación horizontal y evita solapamiento vertical
        while self.generated_y > y_limit and self.generated_y > 0:
            gap = random.randint(PLAT_MIN_GAP, PLAT_MAX_GAP)
            new_y = self.generated_y - gap
            w = random.randint(MIN_PLAT_W, MAX_PLAT_W)

            # mover X respecto a last_x pero con variación, evitando columnas
            shift = random.randint(-MAX_SHIFT, MAX_SHIFT)
            x = self.last_x + shift
            x = max(PLAT_X_MARGIN, min(W - PLAT_X_MARGIN - w, x))

            # si por alguna razón se repetiría la misma X demasiadas veces,
            # forzamos un pequeño desplazamiento adicional para diversidad
            if abs(x - self.last_x) < 8:
                x = max(PLAT_X_MARGIN, min(W - PLAT_X_MARGIN - w, x + random.choice([-24, 24])))

            self.last_x = x

            # Añadir plataforma (coordenadas absolutas en el mundo)
            self.platforms.append((x, new_y, w))

            # Moneda (posición aleatoria sobre la plataforma; no centradas en columna)
            if random.random() < COIN_CHANCE:
                cx = x + random.randint(12, max(12, w - 12))
                cy = new_y - 22  # un poco por encima de la plataforma
                self.coins.append((cx, cy))

            # Spike (colocado para quedar sobre la plataforma; usaremos midbottom=new_y)
            if random.random() < SPIKE_CHANCE:
                sx = x + random.randint(12, max(12, w - 12))
                sy = new_y  # top de la plataforma, lo interpretamos como midbottom al crear sprite
                self.spikes.append((sx, sy))

            # avanzar generador
            self.generated_y = new_y

# ---------- Cámara (solo sube) ----------
class Camera:
    def __init__(self, world_bottom):
        # offset_y indica la coordenada Y del tope visible en el mundo
        self.offset_y = max(0, world_bottom - H)
        self.world_bottom = world_bottom

    def update(self, target_rect):
        # subimos si el jugador sube (no permitimos bajar la cámara)
        target = target_rect.centery - H * 0.55
        if target < 0:
            target = 0
        max_off = max(0, self.world_bottom - H)
        new_off = max(0, min(target, max_off))
        # sólo permitir disminuir offset (subir en mundo)
        if new_off < self.offset_y:
            self.offset_y = new_off

    def apply_rect(self, rect):
        return rect.move(0, -self.offset_y)

# ---------- Helpers ----------
def draw_center_text(surf, text, y, f=None, color=(255,255,255)):
    f = f or font
    img = f.render(text, True, color)
    surf.blit(img, img.get_rect(center=(W//2, y)))

# ---------- Mundo: grupos y sincronización segura ----------
platform_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
spike_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

WORLD_BOTTOM = LEVEL_HEIGHT

# Piso fijo grueso (no se atraviesa)
floor = Platform(0, WORLD_BOTTOM - 80, W)
platform_group.add(floor)

# Plataforma inicial donde aparece el jugador
start_plat = Platform((W//2)-80, WORLD_BOTTOM - 160, 160)
platform_group.add(start_plat)

# Generador y datos iniciales
gen = LevelGenerator(WORLD_BOTTOM)
# generar una buena cantidad inicial
gen.generate_until(WORLD_BOTTOM - 900)

# Sincronizar sprites desde datos generados
# Importante: NO regeneramos gen.* cada frame; gen acumula y sync_groups solo crea sprites.
def sync_groups():
    # limpiar grupos y volver a poblar desde gen (sprites únicos basados en datos)
    platform_group.empty()
    platform_group.add(floor)
    platform_group.add(start_plat)
    for (x,y,w) in gen.platforms:
        platform_group.add(Platform(x, y, w))

    # reconstruimos coins/spikes a partir de gen lists (estas listas se actualizan cuando recoges)
    coin_group.empty()
    for (cx,cy) in gen.coins:
        coin_group.add(Coin(cx, cy))

    spike_group.empty()
    for (sx,sy) in gen.spikes:
        # sy es la Y del tope de la plataforma; Spike usa midbottom para quedar encima
        sp = Spike(sx, sy)
        spike_group.add(sp)

# llamar inicialmente
sync_groups()

# Player
player = Player(W//2 - 10, WORLD_BOTTOM - 220)
all_sprites.add(player)
camera = Camera(WORLD_BOTTOM)

# Estados y UI
STATE_START = "start"
STATE_PLAY = "play"
STATE_WIN  = "win"
STATE_GAMEOVER = "gameover"
state = STATE_START

next_rect = pygame.Rect(W//2 - 110, H//2 + 40, 220, 44)
restart_rect = pygame.Rect(W//2 - 110, H//2 + 100, 220, 44)
time_played = 0.0

# ---------- LOOP PRINCIPAL ----------
running = True
while running:
    dt = clock.tick(FPS) / 1000.0
    keys = pygame.key.get_pressed()

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        if ev.type == pygame.KEYDOWN:
            if state == STATE_START and ev.key == pygame.K_RETURN:
                state = STATE_PLAY
                time_played = 0.0
            elif state == STATE_WIN and ev.key == pygame.K_RETURN:
                # siguiente nivel: aumentar altura y reiniciar
                LEVEL_HEIGHT = int(LEVEL_HEIGHT * 1.12)
                WORLD_BOTTOM = LEVEL_HEIGHT
                gen = LevelGenerator(WORLD_BOTTOM)
                gen.generate_until(WORLD_BOTTOM - 900)
                sync_groups()
                player.pos = Vector2(W//2 - 10, WORLD_BOTTOM - 220)
                player.vel = Vector2(0,0)
                player.lives = START_LIVES
                player.score = 0
                camera = Camera(WORLD_BOTTOM)
                state = STATE_PLAY
            elif state == STATE_GAMEOVER and ev.key == pygame.K_RETURN:
                # reiniciar al inicio
                gen = LevelGenerator(WORLD_BOTTOM)
                gen.generate_until(WORLD_BOTTOM - 900)
                sync_groups()
                player.pos = Vector2(W//2 - 10, WORLD_BOTTOM - 220)
                player.vel = Vector2(0,0)
                player.lives = START_LIVES
                player.score = 0
                camera = Camera(WORLD_BOTTOM)
                state = STATE_START
        if ev.type == pygame.MOUSEBUTTONDOWN:
            if state == STATE_WIN and next_rect.collidepoint(ev.pos):
                LEVEL_HEIGHT = int(LEVEL_HEIGHT * 1.12)
                WORLD_BOTTOM = LEVEL_HEIGHT
                gen = LevelGenerator(WORLD_BOTTOM)
                gen.generate_until(WORLD_BOTTOM - 900)
                sync_groups()
                player.pos = Vector2(W//2 - 10, WORLD_BOTTOM - 220)
                player.vel = Vector2(0,0)
                player.lives = START_LIVES
                player.score = 0
                camera = Camera(WORLD_BOTTOM)
                state = STATE_PLAY
            if state == STATE_GAMEOVER and restart_rect.collidepoint(ev.pos):
                gen = LevelGenerator(WORLD_BOTTOM)
                gen.generate_until(WORLD_BOTTOM - 900)
                sync_groups()
                player.pos = Vector2(W//2 - 10, WORLD_BOTTOM - 220)
                player.vel = Vector2(0,0)
                player.lives = START_LIVES
                player.score = 0
                camera = Camera(WORLD_BOTTOM)
                state = STATE_START
    # ---------- Parte 3: continuación del loop (colisiones, HUD y dibujado) ----------
    # ---------- Estados ----------
    if state == STATE_START:
        screen.fill((18,22,40))
        # Título dividido en 3 líneas para evitar corte y que siempre se vea
        draw_center_text(screen, "Vertical Platformer", H//2 - 48, big_font)
        draw_center_text(screen, "Presiona ENTER para comenzar-Tienes 50 vidas! Las vas a necesitar... :)", H//2 - 8, small_font)
        draw_center_text(screen, "Controles: Flechas o WASD  |  Espacio = Saltar", H//2 + 20, small_font)
        pygame.display.flip()
        continue

    if state == STATE_PLAY:
        time_played += dt

        # generar más hacia arriba si la cámara se aproxima al tope visible
        need_y = int(camera.offset_y - 600)
        if need_y < 0:
            need_y = 0
        gen.generate_until(need_y)
        # sync solo crea sprites a partir de gen (no re-crea gen)
        sync_groups()

        # actualizar jugador
        player.update(dt, platform_group, keys)

        # actualizar cámara (solo sube)
        camera.update(player.rect)

        # si jugador cae por debajo de la vista -> pierde vida o game over
        bottom_visible = camera.offset_y + H
        if player.rect.top > bottom_visible + 4:
            player.lives -= 1
            if player.lives <= 0:
                state = STATE_GAMEOVER
            else:
                # respawn cerca del fondo visible
                player.pos = Vector2(W//2 - 10, bottom_visible - 200)
                player.vel = Vector2(0,0)
                player.rect.topleft = (int(player.pos.x), int(player.pos.y))

        # ---- COLISION CON MONEDAS: dokill=True para quitar sprite del grupo ----
        collected = pygame.sprite.spritecollide(player, coin_group, dokill=True)
        if collected:
            for c in collected:
                player.score += COIN_SCORE
                # eliminar permanentemente de gen.coins para que no se regenere
                # buscamos por proximidad (tolerancia) para evitar problemas de enteros
                to_remove = None
                for (cx, cy) in gen.coins:
                    if abs(cx - c.rect.centerx) <= 6 and abs(cy - c.rect.centery) <= 6:
                        to_remove = (cx, cy)
                        break
                if to_remove:
                    try:
                        gen.coins.remove(to_remove)
                    except ValueError:
                        pass

        # ---- COLISION CON SPIKES ----
        spike_hit = pygame.sprite.spritecollide(player, spike_group, dokill=False)
        if spike_hit:
            # perder vida y respawn (no duplicar si multiple spikes)
            player.lives -= 1
            if player.lives <= 0:
                state = STATE_GAMEOVER
            else:
                player.pos = Vector2(W//2 - 10, bottom_visible - 200)
                player.vel = Vector2(0,0)
                player.rect.topleft = (int(player.pos.x), int(player.pos.y))

        # si alcanza el TOP (rect.top <= 0) -> win
        if player.rect.top <= 0:
            state = STATE_WIN

        # ---------- DIBUJADO ----------
        # fondo tileado verticalmente (si hay imagen)
        if background:
            bh = background.get_height()
            start_tile = int(camera.offset_y // bh)
            end_tile = int((camera.offset_y + H) // bh) + 1
            for t in range(start_tile, end_tile + 1):
                screen.blit(background, (0, t * bh - camera.offset_y))
        else:
            # cielo simple (sin franja verde superior)
            screen.fill((135, 206, 235))

        # dibujar plataformas, monedas y spikes (aplicar cámara)
        for p in platform_group:
            screen.blit(p.image, camera.apply_rect(p.rect))
        for c in coin_group:
            screen.blit(c.image, camera.apply_rect(c.rect))
        for s in spike_group:
            screen.blit(s.image, camera.apply_rect(s.rect))

        # dibujar jugador
        screen.blit(player.image, camera.apply_rect(player.rect))

        # HUD: score, lives, barra de progreso
        screen.blit(font.render(f"Score: {player.score}", True, (255,255,255)), (10,10))
        screen.blit(font.render(f"Vidas: {player.lives}", True, (255,255,255)), (10,34))

        # Barra de progreso (vertical -> muestra cuánto has subido)
        player_world_y = player.rect.centery
        progress = max(0.0, min(1.0, (WORLD_BOTTOM - player_world_y) / max(1, WORLD_BOTTOM)))
        bar_x, bar_y, bar_w, bar_h = 10, 58, W - 20, 12
        pygame.draw.rect(screen, (50,50,50), (bar_x, bar_y, bar_w, bar_h))
        pygame.draw.rect(screen, (100,200,100), (bar_x, bar_y, int(bar_w * progress), bar_h))

        # indicador numérico de progreso (porcentaje)
        pct = int(progress * 100)
        screen.blit(small_font.render(f"{pct}% to top", True, (255,255,255)), (bar_x + bar_w + 6, bar_y - 2))

        pygame.display.flip()
        continue

    # ---------- PANTALLA WIN ----------
    if state == STATE_WIN:
        screen.fill((18,60,20))
        draw_center_text(screen, "¡Felicidades! Llegaste al final", H//2 - 40, big_font, (240,220,80))
        draw_center_text(screen, f"Puntaje: {player.score}   Tiempo: {int(time_played)}s", H//2 + 4)
        pygame.draw.rect(screen, (70,70,100), next_rect)
        pygame.draw.rect(screen, (220,220,220), next_rect, 2)
        draw_center_text(screen, "Siguiente nivel (ENTER o clic)", next_rect.centery)
        pygame.display.flip()
        continue

    # ---------- PANTALLA GAME OVER ----------
    if state == STATE_GAMEOVER:
        screen.fill((60,10,10))
        draw_center_text(screen, "Game Over", H//2 - 40, big_font)
        draw_center_text(screen, f"Puntaje final: {player.score}", H//2 + 4)
        pygame.draw.rect(screen, (70,70,100), restart_rect)
        pygame.draw.rect(screen, (220,220,220), restart_rect, 2)
        draw_center_text(screen, "Reiniciar (ENTER o clic)", restart_rect.centery)
        pygame.display.flip()
        continue

# salir
pygame.quit()
sys.exit()
