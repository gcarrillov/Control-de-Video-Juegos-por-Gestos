import pygame
import random
import sys

pygame.init()

# Función auxiliar para texto centrado
def dibujar_texto(pantalla, texto, tamano, color, y_offset=0):
    fuente = pygame.font.SysFont(None, tamano)
    superficie = fuente.render(texto, True, color)
    rect = superficie.get_rect(center=(pantalla.get_width() // 2, pantalla.get_height() // 2 + y_offset))
    pantalla.blit(superficie, rect)

# === MENÚ PRINCIPAL ===
def menu_principal():
    pantalla = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Menú Principal - Control por Gestos')
    
    opciones = ["1. Snake (Gusanito)", "2. Tank Shooter", "3. Carrera Infinita", "4. Salir"]
    seleccion = 0
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_DOWN, pygame.K_s):
                    seleccion = (seleccion + 1) % len(opciones)
                if evento.key in (pygame.K_UP, pygame.K_w):
                    seleccion = (seleccion - 1) % len(opciones)
                if evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if seleccion == 0: return 'snake'
                    if seleccion == 1: return 'tanque'
                    if seleccion == 2: return 'carrera'
                    if seleccion == 3:
                        pygame.quit()
                        sys.exit()

        pantalla.fill((10, 10, 40))
        dibujar_texto(pantalla, "CONTROL DE VIDEOJUEGOS POR GESTOS", 70, (0, 255, 255), -150)
        dibujar_texto(pantalla, "CARRILLO VILLALTA GUSTAVO - 20230484", 40, (200, 200, 200), -80)
        dibujar_texto(pantalla, "Usa W/S o ↑↓ para seleccionar - ENTER para jugar", 35, (180, 180, 180), -20)

        for i, opcion in enumerate(opciones):
            color = (255, 255, 0) if i == seleccion else (255, 255, 255)
            dibujar_texto(pantalla, opcion, 50, color, 80 + i * 80)

        pygame.display.flip()
        pygame.time.Clock().tick(30)

# === JUEGO SNAKE (adaptado) ===
def jugar_snake():
    WIDTH, HEIGHT = 600, 600
    pantalla = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Snake')
    clock = pygame.time.Clock()

    while True:  # Permite repetir con R
        GRID_SIZE = 20
        serpiente = [(WIDTH // GRID_SIZE // 2, HEIGHT // GRID_SIZE // 2)]
        direccion = (0, -1)
        comida = (random.randint(0, WIDTH//GRID_SIZE-1), random.randint(0, HEIGHT//GRID_SIZE-1))
        puntaje = 0
        velocidad = 8

        corriendo = True
        while corriendo:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return 'salir'
                if event.type == pygame.KEYDOWN:
                    if (event.key in (pygame.K_w, pygame.K_UP)) and direccion != (0, 1): direccion = (0, -1)
                    elif (event.key in (pygame.K_s, pygame.K_DOWN)) and direccion != (0, -1): direccion = (0, 1)
                    elif (event.key in (pygame.K_a, pygame.K_LEFT)) and direccion != (1, 0): direccion = (-1, 0)
                    elif (event.key in (pygame.K_d, pygame.K_RIGHT)) and direccion != (-1, 0): direccion = (1, 0)

            cabeza = serpiente[0]
            nueva_cabeza = ((cabeza[0] + direccion[0]) % (WIDTH//GRID_SIZE), (cabeza[1] + direccion[1]) % (HEIGHT//GRID_SIZE))
            serpiente.insert(0, nueva_cabeza)

            if nueva_cabeza == comida:
                comida = (random.randint(0, WIDTH//GRID_SIZE-1), random.randint(0, HEIGHT//GRID_SIZE-1))
                puntaje += 10
                if puntaje % 50 == 0: velocidad += 2
            else:
                serpiente.pop()

            if nueva_cabeza in serpiente[1:]:
                corriendo = False

            pantalla.fill((0,0,0))
            for x in range(0, WIDTH, GRID_SIZE): pygame.draw.line(pantalla, (50,50,50), (x,0), (x,HEIGHT))
            for y in range(0, HEIGHT, GRID_SIZE): pygame.draw.line(pantalla, (50,50,50), (0,y), (WIDTH,y))

            pygame.draw.rect(pantalla, (255,0,0), (comida[0]*GRID_SIZE, comida[1]*GRID_SIZE, GRID_SIZE, GRID_SIZE))
            for seg in serpiente:
                pygame.draw.rect(pantalla, (0,255,0), (seg[0]*GRID_SIZE, seg[1]*GRID_SIZE, GRID_SIZE, GRID_SIZE))

            dibujar_texto(pantalla, f"Puntaje: {puntaje}", 40, (255,255,255), -270)
            pygame.display.flip()
            clock.tick(velocidad)

        # Game Over Snake
        pantalla.fill((0,0,0))
        dibujar_texto(pantalla, "¡Game Over!", 70, (255,0,0), -80)
        dibujar_texto(pantalla, f"Puntaje final: {puntaje}", 50, (255,255,0), 0)
        dibujar_texto(pantalla, "R = Repetir   M = Menú   ESC = Salir", 40, (255,255,255), 100)
        pygame.display.flip()

        esperando = True
        while esperando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return 'salir'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r: esperando = False
                    if event.key == pygame.K_m: return 'menu'
                    if event.key == pygame.K_ESCAPE: return 'salir'

# === JUEGO TANK SHOOTER (adaptado) ===
def jugar_tanque():
    ANCHO, ALTO = 800, 600
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption('Tank Shooter')
    clock = pygame.time.Clock()

    TIEMPO_TOTAL = 60000
    vel_tanque = 6
    vel_bala = 10
    vel_enemigo = 3

    while True:
        balas = []
        enemigos = []
        puntuacion = 0
        tanque_x = ANCHO // 2 - 30
        tanque_y = ALTO - 80
        tiempo_inicio = pygame.time.get_ticks()
        juego_activo = True

        while juego_activo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT: return 'salir'
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_w:
                        balas.append([tanque_x + 25, tanque_y])

            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_a] and tanque_x > 0: tanque_x -= vel_tanque
            if teclas[pygame.K_d] and tanque_x < ANCHO - 60: tanque_x += vel_tanque

            if random.randint(1, 25) == 1:
                enemigos.append([random.randint(0, ANCHO-40), -40])

            for bala in balas[:]:
                bala[1] -= vel_bala
                if bala[1] < 0: balas.remove(bala)

            for enemigo in enemigos[:]:
                enemigo[1] += vel_enemigo
                if enemigo[1] > ALTO: enemigos.remove(enemigo)

                for bala in balas[:]:
                    if bala[0] > enemigo[0] and bala[0] < enemigo[0]+40 and bala[1] > enemigo[1] and bala[1] < enemigo[1]+40:
                        balas.remove(bala)
                        enemigos.remove(enemigo)
                        puntuacion += 10
                        break

            tiempo_restante = TIEMPO_TOTAL - (pygame.time.get_ticks() - tiempo_inicio)
            if tiempo_restante <= 0: juego_activo = False

            pantalla.fill((20, 40, 80))
            pygame.draw.rect(pantalla, (40, 80, 40), (0, ALTO-50, ANCHO, 50))
            pygame.draw.rect(pantalla, (0, 255, 0), (tanque_x, tanque_y, 60, 40))
            pygame.draw.rect(pantalla, (200, 200, 0), (tanque_x + 20, tanque_y - 20, 20, 25))
            for bala in balas: pygame.draw.rect(pantalla, (255, 255, 0), (bala[0], bala[1], 8, 16))
            for enemigo in enemigos:
                pygame.draw.rect(pantalla, (255, 50, 50), (enemigo[0], enemigo[1], 40, 40))

            dibujar_texto(pantalla, f"Tiempo: {tiempo_restante // 1000}s   Puntos: {puntuacion}", 40, (255,255,255), -270)
            pygame.display.flip()
            clock.tick(60)

        # Game Over Tanque
        pantalla.fill((20, 40, 80))
        dibujar_texto(pantalla, "¡TIEMPO TERMINADO!", 70, (255,100,100), -80)
        dibujar_texto(pantalla, f"{puntuacion} PUNTOS", 60, (255,255,0), 0)
        dibujar_texto(pantalla, "R = Repetir   M = Menú   ESC = Salir", 40, (255,255,255), 100)
        pygame.display.flip()

        esperando = True
        while esperando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return 'salir'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r: esperando = False
                    if event.key == pygame.K_m: return 'menu'
                    if event.key == pygame.K_ESCAPE: return 'salir'

# === JUEGO CARRERA (adaptado) ===
def jugar_carrera():
    ANCHO, ALTO = 500, 700
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption('Carrera Infinita')
    clock = pygame.time.Clock()

    vel = 6
    vel_enemigos = 8

    while True:
        enemigos = []
        puntuacion = 0
        scroll_y = 0
        auto_x = ANCHO//2 - 25
        auto_y = 600
        juego_activo = True

        while juego_activo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT: return 'salir'

            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_a] and auto_x > 0: auto_x -= vel
            if teclas[pygame.K_d] and auto_x < ANCHO-50: auto_x += vel
            if teclas[pygame.K_w]: scroll_y += 5
            if teclas[pygame.K_s]: scroll_y -= 2

            if random.randint(1, 25) == 1:
                enemigos.append([random.randint(0, ANCHO-50), -50])

            for enemigo in enemigos[:]:
                enemigo[1] += vel_enemigos + scroll_y//10
                if enemigo[1] > ALTO:
                    enemigos.remove(enemigo)
                    puntuacion += 5

            for enemigo in enemigos:
                if (auto_x < enemigo[0] + 50 and auto_x + 50 > enemigo[0] and
                    auto_y < enemigo[1] + 80 and auto_y + 80 > enemigo[1]):
                    juego_activo = False

            pantalla.fill((100, 100, 100))
            for i in range(0, ALTO, 40):
                pygame.draw.rect(pantalla, (255, 255, 255), (ANCHO//2-5, (i+scroll_y)%40, 10, 40))

            pygame.draw.rect(pantalla, (0, 255, 0), (auto_x, auto_y, 50, 80))
            for enemigo in enemigos:
                pygame.draw.rect(pantalla, (255, 0, 0), (enemigo[0], enemigo[1], 50, 80))

            dibujar_texto(pantalla, f'{puntuacion}', 50, (255,255,255), -300)
            pygame.display.flip()
            clock.tick(60)

        # Game Over Carrera
        pantalla.fill((100, 100, 100))
        dibujar_texto(pantalla, "¡GAME OVER!", 70, (255,100,100), -80)
        dibujar_texto(pantalla, f"{puntuacion} PUNTOS", 60, (255,255,0), 0)
        dibujar_texto(pantalla, "R = Repetir   M = Menú   ESC = Salir", 40, (255,255,255), 100)
        pygame.display.flip()

        esperando = True
        while esperando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return 'salir'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r: esperando = False
                    if event.key == pygame.K_m: return 'menu'
                    if event.key == pygame.K_ESCAPE: return 'salir'

# === BUCLE PRINCIPAL ===
while True:
    eleccion = menu_principal()
    if eleccion == 'snake':
        resultado = jugar_snake()
    elif eleccion == 'tanque':
        resultado = jugar_tanque()
    elif eleccion == 'carrera':
        resultado = jugar_carrera()
    if resultado == 'salir':
        pygame.quit()
        sys.exit()