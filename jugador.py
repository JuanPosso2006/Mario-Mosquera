import pygame
import random

pygame.init()

ANCHO = 900
ALTO = 700
FPS = 60
COLOR_FONDO = (135, 206, 250)
COLOR_PISO = (135, 206, 250)
ALTURA_PISO = 50

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mario Mosquera - Juego")
reloj = pygame.time.Clock()

try:
    fondo = pygame.image.load("fondo.jpg").convert()
    fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
except:
    fondo = None

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.imagen_normal = pygame.image.load("mario.png").convert_alpha()
        self.imagen_normal = pygame.transform.scale(self.imagen_normal, (40, 60))
        self.image = self.imagen_normal
        self.rect = self.image.get_rect()
        self.rect.midbottom = (60, ALTO - ALTURA_PISO)
        self.velocidad = 5
        self.vidas = 2
        self.inmune = False
        self.ultimo_tiempo_inmunidad = 0
        self.en_suelo = True
        self.velocidad_salto = 0
        self.salto_maximo = -15
        self.gravedad = 0.5
        self.direccion = 1
        self.grande = False

    def update(self):
        if self.inmune and pygame.time.get_ticks() - self.ultimo_tiempo_inmunidad > 8000:
            self.inmune = False

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
            self.direccion = -1
            if self.rect.x < 0:
                self.rect.x = 0
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidad
            self.direccion = 1
            if self.rect.x > ANCHO - self.rect.width:
                self.rect.x = ANCHO - self.rect.width
        if teclas[pygame.K_SPACE] and self.en_suelo:
            self.velocidad_salto = self.salto_maximo
            self.en_suelo = False

        if not self.en_suelo:
            self.velocidad_salto += self.gravedad
            self.rect.y += self.velocidad_salto
            if self.rect.bottom >= ALTO - ALTURA_PISO:
                self.rect.bottom = ALTO - ALTURA_PISO
                self.en_suelo = True
                self.velocidad_salto = 0

        if self.direccion == -1:
            self.image = pygame.transform.flip(self.imagen_normal, True, False)
        else:
            self.image = self.imagen_normal

class Moneda(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            imagen = pygame.image.load("moneda.png").convert_alpha()
            self.image = pygame.transform.scale(imagen, (25, 25))
        except:
            self.image = pygame.Surface((25, 25))
            self.image.fill((255, 215, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(100, ANCHO - 100)
        self.rect.y = random.randint(ALTO - ALTURA_PISO - 290, ALTO - ALTURA_PISO - 85)

class Hongo(pygame.sprite.Sprite):
    def __init__(self, tipo, posicion, tiempo_visible=5):
        super().__init__()
        self.tipo = tipo
        self.tiempo_visible = tiempo_visible
        self.visible = False
        self.tiempo_activado = 0
        try:
            if tipo == "rojo":
                imagen = pygame.image.load("hongo_rojo.png").convert_alpha()
            else:
                imagen = pygame.image.load("hongo_azul.png").convert_alpha()
            self.image = pygame.transform.scale(imagen, (30, 30))
        except:
            self.image = pygame.Surface((30, 30))
            self.image.fill((255, 0, 0) if tipo == "rojo" else (0, 0, 255))
        self.rect = self.image.get_rect()
        self.posicion_inicial = posicion
        self.ocultar()

    def mostrar(self):
        self.visible = True
        self.tiempo_activado = pygame.time.get_ticks()
        self.rect.topleft = self.posicion_inicial

    def ocultar(self):
        self.visible = False
        self.rect.x = -100

    def update(self):
        if self.visible:
            if pygame.time.get_ticks() - self.tiempo_activado > self.tiempo_visible * 1000:
                self.ocultar()

class Estrella(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            imagen = pygame.image.load("estrella.png").convert_alpha()
            self.image = pygame.transform.scale(imagen, (30, 30))
        except:
            self.image = pygame.Surface((30, 30))
            self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ANCHO - self.rect.width)
        self.rect.y = random.randint(ALTO - ALTURA_PISO - 290, ALTO - ALTURA_PISO - 70)

class Goomba(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            imagen = pygame.image.load("goomba.png").convert_alpha()
            self.image = pygame.transform.scale(imagen, (40, 25))
        except:
            self.image = pygame.Surface((40, 40))
            self.image.fill((139, 69, 19))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(200, ANCHO - 100)
        self.rect.y = ALTO - ALTURA_PISO - 25
        self.velocidad = 2
        self.direccion = 1

    def update(self):
        self.rect.x += self.velocidad * self.direccion
        if self.rect.x <= 0 or self.rect.x >= ANCHO - self.rect.width:
            self.direccion *= -1

def dibujar_piso():
    pygame.draw.rect(pantalla, COLOR_PISO, (0, ALTO - ALTURA_PISO, ANCHO, ALTURA_PISO))

def main():
    jugador = Jugador()
    monedas = pygame.sprite.Group([Moneda() for _ in range(10)])
    hongo_rojo = Hongo("rojo", (300, ALTO - ALTURA_PISO - 30))
    hongo_azul = Hongo("azul", (500, ALTO - ALTURA_PISO - 30))
    estrella = Estrella()
    goombas = pygame.sprite.Group([Goomba() for _ in range(5)])

    hongos = pygame.sprite.Group(hongo_rojo, hongo_azul)
    todos = pygame.sprite.Group(jugador, monedas, hongos, estrella, goombas)

    monedas_recogidas = 0
    corriendo = True

    hongo_rojo.mostrar()
    hongo_azul.mostrar()

    while corriendo:
        reloj.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        todos.update()

        # Monedas
        colisionadas = pygame.sprite.spritecollide(jugador, monedas, dokill=True)
        monedas_recogidas += len(colisionadas)
        if monedas_recogidas == 11:
            jugador.vidas += 1
            monedas_recogidas = 0

        # Hongos
        for hongo in pygame.sprite.spritecollide(jugador, hongos, dokill=False):
            if hongo.visible:
                if hongo.tipo == "rojo":
                    jugador.vidas += 1
                elif hongo.tipo == "azul" and not jugador.grande:
                    jugador.rect.inflate_ip(10, 10)
                    jugador.grande = True
                hongo.ocultar()

        # Goombas
        if pygame.sprite.spritecollide(jugador, goombas, dokill=True):
            if jugador.grande:
                jugador.rect.inflate_ip(-10, -10)
                jugador.grande = False
            elif not jugador.inmune:
                jugador.vidas -= 1

        # Estrella
        if jugador.rect.colliderect(estrella.rect):
            jugador.inmune = True
            jugador.ultimo_tiempo_inmunidad = pygame.time.get_ticks()
            estrella.rect.x = -100

        # Game Over
        if jugador.vidas <= 0:
            fuente = pygame.font.SysFont("Arial", 50)
            texto = fuente.render(" Game Over", True, (255, 0, 0))
            pantalla.blit(texto, (ANCHO // 2 - 150, ALTO // 2 - 30))
            pygame.display.flip()
            pygame.time.delay(2000)
            corriendo = False

        if fondo:
            pantalla.blit(fondo, (0, 0))
        else:
            pantalla.fill(COLOR_FONDO)
        dibujar_piso()

        # Mostrar vidas y monedas
        fuente = pygame.font.SysFont("Arial", 30)
        texto_vidas = fuente.render(f'Vidas: {jugador.vidas}', True, (255, 255, 255))
        texto_monedas = fuente.render(f'Monedas: {monedas_recogidas}', True, (255, 255, 255))
        pantalla.blit(texto_vidas, (20, 20))
        pantalla.blit(texto_monedas, (20, 50))

        todos.draw(pantalla)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
