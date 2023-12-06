import pygame
import sys
import random
import time

# Inicialización de Pygame
pygame.init()

# Definición de colores
WHITE = (203, 134, 134)
RED = (172, 134, 203)
GREEN = (203, 193, 134)

# Tamaño de la ventana y otros parámetros
WIDTH, HEIGHT = 600, 600
FPS = 30

# Tamaño de las celdas del laberinto
CELL_SIZE = 30

# Definición del laberinto (0: camino, 1: pared)
maze = [
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 1, 0],
    [0, 1, 0, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 1, 1, 1, 0],
    [0, 1, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
]

# Niveles del laberinto
LEVELS = [
    maze,
    # Agrega más niveles según lo desees
    [
    [0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1],
    [0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1],
    [0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0],
    [0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1],
    [0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1],
    [0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0],
    [0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1],
    [1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0],
]
]

# Tiempo máximo por nivel (en segundos)
MAX_TIME_PER_LEVEL = 60

# Crear el objeto Clock para controlar la velocidad de fotogramas
clock = pygame.time.Clock()

def draw_timer(current_time, max_time):
    font = pygame.font.Font(None, 36)
    timer_text = font.render(f"Tiempo: {int(max_time - current_time)}s", True, WHITE)
    screen.blit(timer_text, (10, 10))

def draw_maze(level):
    for row in range(len(level)):
        for col in range(len(level[row])):
            if level[row][col] == 1:
                pygame.draw.rect(screen, WHITE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_player(player_pos):
    pygame.draw.rect(screen, RED, (player_pos[1] * CELL_SIZE, player_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def display_message(message):
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    time.sleep(2)

def main():
    global screen  # Declarar screen como una variable global

    # Creación de la ventana
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Laberinto")

    current_level = 0
    player_pos = [0, 0]
    start_time = time.time()

    while current_level < len(LEVELS):
        level = LEVELS[current_level]
        level_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player_pos[0] > 0 and level[player_pos[0] - 1][player_pos[1]] == 0:
            player_pos[0] -= 1
        if keys[pygame.K_DOWN] and player_pos[0] < len(level) - 1 and level[player_pos[0] + 1][player_pos[1]] == 0:
            player_pos[0] += 1
        if keys[pygame.K_LEFT] and player_pos[1] > 0 and level[player_pos[0]][player_pos[1] - 1] == 0:
            player_pos[1] -= 1
        if keys[pygame.K_RIGHT] and player_pos[1] < len(level[0]) - 1 and level[player_pos[0]][player_pos[1] + 1] == 0:
            player_pos[1] += 1

        screen.fill(GREEN)
        draw_maze(level)
        draw_player(player_pos)
        draw_timer(level_time, MAX_TIME_PER_LEVEL)

        pygame.display.flip()
        clock.tick(FPS)

        # Verificar si el jugador llegó al final del laberinto
        if player_pos == [len(level) - 1, len(level[0]) - 1]:
            current_level += 1
            start_time = time.time()
            player_pos = [0, 0]
            if current_level < len(LEVELS):
                display_message(f"Nivel {current_level + 1}")
                time.sleep(1)

        # Verificar si se agotó el tiempo
        if level_time > MAX_TIME_PER_LEVEL:
            display_message("Se agotó el tiempo. Intenta de nuevo.")
            return

    display_message("¡Felicidades! Has completado todos los niveles.")

if __name__ == "__main__":
    main()
