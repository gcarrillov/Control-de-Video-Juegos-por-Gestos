import pygame
import random
import time

pygame.init()

# colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY  = (50, 50, 50)

# ventana y celdas
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
GRID_WIDTH  = WIDTH  // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake - juego de la serpiente')
clock = pygame.time.Clock()

# fuente de texto
font_large = pygame.font.SysFont(None, 60)
font_small = pygame.font.SysFont(None, 40)

def dibujar_cuadricula():
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

def mostrar_texto(texto, fuente, color, centro):
    superficie = fuente.render(texto, True, color)
    rect = superficie.get_rect(center=centro)
    screen.blit(superficie, rect)

def juego():
    # posicion 0 
    serpiente = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    direccion = (0, -1)          # empieza a moverse para arriba
    comida = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
    
    puntaje = 0
    velocidad = 8                # frames por segundo fps

    corriendo = True
    while corriendo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

            # captura de teclas
            if event.type == pygame.KEYDOWN:
                if (event.key in (pygame.K_w, pygame.K_UP)) and direccion != (0, 1):
                    direccion = (0, -1)   # W
                elif (event.key in (pygame.K_s, pygame.K_DOWN)) and direccion != (0, -1):
                    direccion = (0, 1)    # S
                elif (event.key in (pygame.K_a, pygame.K_LEFT)) and direccion != (1, 0):
                    direccion = (-1, 0)   # A
                elif (event.key in (pygame.K_d, pygame.K_RIGHT)) and direccion != (-1, 0):
                    direccion = (1, 0)    # D

        # mover la cabeza
        cabeza = serpiente[0]
        nueva_cabeza = ((cabeza[0] + direccion[0]) % GRID_WIDTH,
                        (cabeza[1] + direccion[1]) % GRID_HEIGHT)
        serpiente.insert(0, nueva_cabeza)

        # comer comida
        if nueva_cabeza == comida:
            comida = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
            puntaje += 10
            if puntaje % 50 == 0:      # cada 50 puntos se aumenta la velocidad
                velocidad += 2
        else:
            serpiente.pop()            # quitar cola si no comió

        # colisión consigo misma
        if nueva_cabeza in serpiente[1:]:
            corriendo = False

        # dibujar todo
        screen.fill(BLACK)
        dibujar_cuadricula()

        # comida
        pygame.draw.rect(screen, RED,
                         (comida[0] * GRID_SIZE, comida[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # serpiente
        for segmento in serpiente:
            pygame.draw.rect(screen, GREEN,
                             (segmento[0] * GRID_SIZE, segmento[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # puntaje
        mostrar_texto(f"Puntaje: {puntaje}", font_small, WHITE, (80, 20))

        pygame.display.update()
        clock.tick(velocidad)

    # Game Over
    screen.fill(BLACK)
    mostrar_texto("Game Over!", font_large, RED, (WIDTH//2, HEIGHT//2 - 60))
    mostrar_texto(f"Puntaje final: {puntaje}", font_small, WHITE, (WIDTH//2, HEIGHT//2 + 20))
    mostrar_texto("Presiona ESC para salir", font_small, WHITE, (WIDTH//2, HEIGHT//2 + 80))
    pygame.display.update()

    # salir con ESC o cerrar ventana
    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                esperando = False

    pygame.quit()

if __name__ == "__main__":
    juego()