import pygame, random, sys

pygame.init()
ANCHO, ALTO = 900, 650
screen = pygame.display.set_mode((ANCHO, ALTO))
clock = pygame.time.Clock()


#Cargar sprites
""""permite que aparezcan los objetos (imagenes) necesarias"""
player_img = pygame.transform.scale(pygame.image.load("Assets/player.png"), (60, 50))
bueno_img  = pygame.transform.scale(pygame.image.load("Assets/carrot.coin.png"), (40, 40))
malo_img   = pygame.transform.scale(pygame.image.load("Assets/objeto.malo.png"), (60, 40))

#Cargar fondos
""""permite que cada pantalla tenga su fondo"""
fondo = pygame.transform.scale(pygame.image.load("Assets/level.2.backgraound.jpg"), (ANCHO, ALTO))
fondo_good = pygame.transform.scale(pygame.image.load("Assets/good.ending.png"), (ANCHO, ALTO))
fondo_bad = pygame.transform.scale(pygame.image.load("Assets/bad.ending.png"), (ANCHO, ALTO))
fondo_menu = pygame.transform.scale(pygame.image.load("Assets/Menuu.background.jpg"), (ANCHO, ALTO))

#Límites de objetos
""""indica el numero exacto de objetos que se generaran"""
TOTAL_BUENOS = 32
TOTAL_MALOS = 45
"""indica cuantos objetos requiere el jugador para ganar o perder"""
META = 24
MAX_MALOS = 3   #si atrapas 3 malos pierdes

#menu
class MainMenu:
    """muestra un menu simple al inicio del juego"""
    def __init__(self):
        self.fuente = pygame.font.SysFont("fonts/PressStart2P.ttf", 70)
        self.sub = pygame.font.SysFont("fonts/PressStart2P.ttf", 45)

    def run(self):
        """define que teclas presionar para iniciar o salir de el juego """
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        return
                    if e.key == pygame.K_ESCAPE:
                        pygame.quit(); sys.exit()

            """define el titulo y las instrucciones para iniciar o salir del juego"""
            screen.blit(fondo_menu, (0, 0))

            titulo = self.fuente.render("Carrot Crisis", True, (0, 0, 0))
            start  = self.sub.render("ENTER para comenzar", True, (255,255,255))
            salir  = self.sub.render("ESC para salir", True, (255,255,255))

            screen.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 200))
            screen.blit(start,  (ANCHO//2 - start.get_width()//2, 300))
            screen.blit(salir,  (ANCHO//2 - salir.get_width()//2, 350))
            """define las distancia entre el titulo y las instrucciones"""
            pygame.display.flip()
            clock.tick(60)

#CLASE GOOD ENDING

class GoodEnding:
    """Aparece en pantalla un good ending cuando completas todas las zanahorias"""
    def __init__(self):
        self.fuente = pygame.font.SysFont("fonts/PressStart2P.ttf", 40)
        self.sub = pygame.font.SysFont("fonts/PressStart2P.ttf", 25)

    def run(self):
        """Hace que cuando presiones la tecla return salgas automaticamente del juego"""
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        return

            screen.blit(fondo_good, (0, 0))

            texto = self.fuente.render("¡GOOD ENDING!", True, (255,255,255))
            sub = self.sub.render("Presiona ENTER para terminar", True, (255,255,255))

            screen.blit(texto, (ANCHO//2 - texto.get_width()//2, 200))
            screen.blit(sub, (ANCHO//2 - sub.get_width()//2, 280))

            pygame.display.flip()
            clock.tick(60)
"""La línea 83 y 84 indican el texto y el color del mismo. La linea 86 y la 87 indican la distancia entre el titulo y las indicaciones"""


#CLASE BAD ENDING
""""hace que aparezca un bad ending si te golpean 3 piedras"""
class BadEnding:
    def __init__(self):
        self.fuente = pygame.font.SysFont("fonts/PressStart2P.ttf", 50)
        self.sub = pygame.font.SysFont("fonts/PressStart2P.ttf", 30)

    def run(self):
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        return

            screen.blit(fondo_bad, (0, 0))

            texto = self.fuente.render("BAD ENDING...", True, (255,50,50))
            sub   = self.sub.render("Presiona ENTER para terminar", True, (255,255,255))

            screen.blit(texto, (ANCHO//2 - texto.get_width()//2, 200))
            screen.blit(sub, (ANCHO//2 - sub.get_width()//2, 280))

            pygame.display.flip()
            clock.tick(60)
"""Linea 112 y 113 indican el texto y el color del mismo. Linea 115 y 116 indican la distancia entre el titulo y las indicaciones"""


#CLASE OBJETO

class Objeto(pygame.sprite.Sprite):
    def __init__(self, tipo):
        super().__init__()
        self.tipo = tipo
        self.image = bueno_img if tipo == "bueno" else malo_img
        self.rect = self.image.get_rect(
            topleft=(random.randint(0, ANCHO-40), random.randint(-120, -40))
        )
        self.vel = random.randint(2, 5)
        """permite que los objetos aparezcan desde la parte superior de la pantalla pero de manera aleatoria y en distintas velocidades"""

    def update(self):
        self.rect.y += self.vel
        if self.rect.top > ALTO:
            self.kill()



#CLASE JUGADOR
"""indica que puede hacer el jugador"""
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect(center=(ANCHO//2, ALTO-60))
        self.vel = 7

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.vel
        if keys[pygame.K_RIGHT] and self.rect.right < ANCHO:
            self.rect.x += self.vel
"""indica que teclas hay que presionar para que el personaje se mueva hacia la izquierda o derecha"""


#FUNCIÓN PRINCIPAL
"""une todas las clases anteriores"""
def juego():
    global TOTAL_BUENOS, TOTAL_MALOS

    jugador = Jugador()
    grupo_jugador = pygame.sprite.Group(jugador)
    objetos = pygame.sprite.Group()

    buenos_atrapados = 0
    malos_atrapados = 0   # <<--- NUEVO
    fuente = pygame.font.SysFont("fonts/PressStart2P.ttf", 40)

    while True:

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        """bucle para que se muestren correctamente los endings"""
        #GOOD ENDING
        if buenos_atrapados >= META:
            good = GoodEnding()
            good.run()
            pygame.quit(); sys.exit()

        #BAD ENDING
        if malos_atrapados >= MAX_MALOS:
            bad = BadEnding()
            bad.run()
            pygame.quit(); sys.exit()

        #Generar objetos
        if len(objetos) < 5:
            if TOTAL_BUENOS or TOTAL_MALOS:
                tipo = ("bueno" if TOTAL_BUENOS and random.random() < 0.5 else "malo")
                if tipo == "bueno" and TOTAL_BUENOS: TOTAL_BUENOS -= 1
                elif tipo == "malo" and TOTAL_MALOS: TOTAL_MALOS -= 1
                objetos.add(Objeto(tipo))

        #Actualizar
        grupo_jugador.update()
        objetos.update()

        #Colisiones
        colisiones = pygame.sprite.spritecollide(jugador, objetos, True)
        for obj in colisiones:
            if obj.tipo == "bueno":
                buenos_atrapados += 1
            else:
                malos_atrapados += 1

        #Dibujar
        screen.blit(fondo, (0, 0))
        objetos.draw(screen)
        grupo_jugador.draw(screen)

        screen.blit(fuente.render(f"Buenos: {buenos_atrapados}/{META}", True, (250, 248, 241)), (10,10))
        screen.blit(fuente.render(f"Malos: {malos_atrapados}/{MAX_MALOS}", True, (250, 248, 241)), (10,40))

        pygame.display.flip()
        clock.tick(60)

#INICIAR CON MENÚ


menu = MainMenu()
menu.run()
juego()
