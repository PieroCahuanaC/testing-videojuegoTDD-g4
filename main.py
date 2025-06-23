import pygame
import os
import random
import sys

# Configuración inicial
WIDTH, HEIGHT = 800, 600
FPS = 30
CARD_SIZE = (100, 140)
GAP = 20
MAX_LIVES = 5

# Rutas y carga de imágenes
ASSETS_DIR = "assets/cards"
CARD_BACK = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_DIR, "card_back.png")), CARD_SIZE)
HEART_IMG = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_DIR, "heart.png")), (40, 40))
SETTINGS_IMG = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_DIR, "ajustes.png")), (50, 50))
BACKGROUND_IMG = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_DIR, "fondo.png")), (WIDTH, HEIGHT))

# Nombres de cartas disponibles
CARD_NAMES = ["apple", "banana", "cherry", "grape", "lemon", "orange"]

class Card:
    def __init__(self, name, pos):
        self.name = name
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_DIR, f"{name}.png")), CARD_SIZE)
        self.rect = pygame.Rect(pos[0], pos[1], CARD_SIZE[0], CARD_SIZE[1])
        self.is_flipped = False
        self.is_matched = False

    def draw(self, screen):
        if self.is_flipped or self.is_matched:
            screen.blit(self.image, self.rect)
        else:
            screen.blit(CARD_BACK, self.rect)

    def flip(self):
        if not self.is_matched:
            self.is_flipped = not self.is_flipped

class ConfettiParticle:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-50, -10)
        self.size = random.randint(4, 8)
        self.color = random.choice([(94, 86, 227), (3, 217, 195), (204, 0, 0)])
        self.speed_y = random.uniform(1, 3)
        self.speed_x = random.uniform(-1, 1)

    def update(self):
        self.y += self.speed_y
        self.x += self.speed_x

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

def create_board(level):
    num_pairs = min(level + 1, len(CARD_NAMES))
    selected_names = CARD_NAMES[:num_pairs] * 2
    random.shuffle(selected_names)
    board = []

    total_cards = len(selected_names)

    if level == 1:
        rows, cols = 2, 2
    elif level == 2:
        rows, cols = 2, 3
    elif level == 3:
        rows, cols = 2, 4
    elif level == 4:
        rows, cols = 2, 5
    else:
        rows, cols = 3, 4

    total_width = cols * CARD_SIZE[0] + (cols - 1) * GAP
    total_height = rows * CARD_SIZE[1] + (rows - 1) * GAP

    offset_x = (WIDTH - total_width) // 2
    offset_y = (HEIGHT - total_height) // 2 - 30

    idx = 0
    for row in range(rows):
        for col in range(cols):
            if idx >= total_cards:
                break
            x = offset_x + col * (CARD_SIZE[0] + GAP)
            y = offset_y + row * (CARD_SIZE[1] + GAP)
            board.append(Card(selected_names[idx], (x, y)))
            idx += 1

    return board

def show_menu(screen, font):
    menu_options = ["Iniciar Juego", "Salir"]
    clock = pygame.time.Clock()

    button_width, button_height = 250, 60
    button_gap = 30
    total_height = len(menu_options) * button_height + (len(menu_options) - 1) * button_gap
    start_y = (HEIGHT - total_height) // 2
    button_rects = []
    for i in range(len(menu_options)):
        x = (WIDTH - button_width) // 2
        y = start_y + i * (button_height + button_gap)
        button_rects.append(pygame.Rect(x, y, button_width, button_height))

    while True:
        screen.blit(BACKGROUND_IMG, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True

        for i, option in enumerate(menu_options):
            rect = button_rects[i]
            if rect.collidepoint(mouse_pos):
                color = (70, 255, 0)
                text_color = (255, 255, 255)
                if mouse_clicked:
                    return option
            else:
                color = (50, 50, 50)
                text_color = (200, 200, 200)

            pygame.draw.rect(screen, color, rect, border_radius=10)
            text_surf = font.render(option, True, text_color)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)

        pygame.display.flip()
        clock.tick(FPS)

def pause_menu(screen, font):
    pause_options = ["Reanudar", "Menú Principal"]
    clock = pygame.time.Clock()

    button_width, button_height = 220, 55
    button_gap = 20
    total_height = len(pause_options) * button_height + (len(pause_options) - 1) * button_gap
    start_y = (HEIGHT - total_height) // 2
    button_rects = []
    for i in range(len(pause_options)):
        x = (WIDTH - button_width) // 2
        y = start_y + i * (button_height + button_gap)
        button_rects.append(pygame.Rect(x, y, button_width, button_height))

    while True:
        screen.blit(BACKGROUND_IMG, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True

        for i, option in enumerate(pause_options):
            rect = button_rects[i]
            if rect.collidepoint(mouse_pos):
                color = (100, 149, 237)
                text_color = (255, 255, 255)
                if mouse_clicked:
                    return i  # Devuelve el índice de la opción
            else:
                color = (70, 70, 70)
                text_color = (200, 200, 200)

            pygame.draw.rect(screen, color, rect, border_radius=10)
            text_surf = font.render(option, True, text_color)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)

        pygame.display.flip()
        clock.tick(FPS)

def show_level_complete(screen, level, confetti_particles):
    # Fondo semitransparente
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    
    # Fuentes
    big_font = pygame.font.SysFont(None, 72)
    small_font = pygame.font.SysFont(None, 36)
    
    # Texto principal
    main_text = big_font.render(f"¡Nivel {level} completado!", True, (0, 255, 0))
    main_rect = main_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
    
    # Texto secundario
    sub_text = small_font.render("Haz clic para continuar", True, (255, 255, 255))
    sub_rect = sub_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
    
    # Mostrar textos
    screen.blit(main_text, main_rect)
    screen.blit(sub_text, sub_rect)
    
    # Mostrar confeti
    for particle in confetti_particles:
        particle.update()
        particle.draw(screen)
    
    pygame.display.flip()
    
    # Esperar clic del usuario
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

def show_game_over(screen):
    # Fondo semitransparente
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    
    # Fuentes
    big_font = pygame.font.SysFont(None, 72)
    small_font = pygame.font.SysFont(None, 36)
    
    # Texto principal
    main_text = big_font.render("¡Game Over!", True, (255, 0, 0))
    main_rect = main_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
    
    # Texto secundario
    sub_text = small_font.render("Haz clic para volver al menú", True, (255, 255, 255))
    sub_rect = sub_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
    
    # Mostrar textos
    screen.blit(main_text, main_rect)
    screen.blit(sub_text, sub_rect)
    
    pygame.display.flip()
    
    # Esperar clic del usuario
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
def draw_text_with_outline(screen, text, font, x, y, text_color, outline_color):
    base = font.render(text, True, text_color)
    outline = font.render(text, True, outline_color)
    for dx in [-2, 0, 2]:
        for dy in [-2, 0, 2]:
            if dx != 0 or dy != 0:
                screen.blit(outline, (x + dx, y + dy))
    screen.blit(base, (x, y))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Memory Match Game")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    while True:
        # Mostrar menú principal
        choice = show_menu(screen, font)
        if choice == "Salir":
            pygame.quit()
            sys.exit()

        # Iniciar juego desde nivel 1
        level = 1
        
        # Bucle principal de niveles
        back_to_menu = False
        while not back_to_menu:
            # Configuración del nivel actual
            board = create_board(level)
            flipped_cards = []
            waiting = False
            wait_start_time = 0
            WAIT_TIME = 1000
            lives = MAX_LIVES
            game_over = False
            confetti_triggered = False
            confetti_particles = []
            settings_rect = SETTINGS_IMG.get_rect(topright=(WIDTH - 10, 10))
            start_ticks = pygame.time.get_ticks()
            paused_time = 0
            game_paused = False

            # Bucle del juego para el nivel actual
            running = True
            while running:
                clock.tick(FPS)
                screen.blit(BACKGROUND_IMG, (0, 0))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        pos = pygame.mouse.get_pos()
                        
                        # Manejo del botón de ajustes
                        if settings_rect.collidepoint(pos) and not game_over:
                            game_paused = True
                            pause_start = pygame.time.get_ticks()
                            option_index = pause_menu(screen, font)
                            paused_time += pygame.time.get_ticks() - pause_start
                            
                            if option_index == 0:  # Reanudar
                                game_paused = False
                            elif option_index == 1:  # Menú Principal
                                running = False
                                back_to_menu = True
                                break
                        
                        # Manejo de clic en cartas
                        elif not waiting and not game_over and not game_paused:
                            for card in board:
                                if card.rect.collidepoint(pos) and not card.is_flipped and not card.is_matched:
                                    card.flip()
                                    flipped_cards.append(card)
                                    break

                # Lógica del juego (solo si no está pausado o en game over)
                if not game_paused and not game_over:
                    if len(flipped_cards) == 2 and not waiting:
                        c1, c2 = flipped_cards
                        if c1.name == c2.name:
                            c1.is_matched = True
                            c2.is_matched = True
                            flipped_cards = []
                        else:
                            lives -= 1
                            waiting = True
                            wait_start_time = pygame.time.get_ticks()

                    if waiting and pygame.time.get_ticks() - wait_start_time >= WAIT_TIME:
                        for card in flipped_cards:
                            card.flip()
                        flipped_cards = []
                        waiting = False

                    if lives <= 0:
                        game_over = True

                # Dibujar elementos (siempre, incluso cuando está pausado)
                for card in board:
                    card.draw(screen)

                # Dibujar vidas
                for i in range(lives):
                    x = WIDTH // 2 - (MAX_LIVES * (HEART_IMG.get_width() + 5)) // 2 + i * (HEART_IMG.get_width() + 5)
                    y = HEIGHT - HEART_IMG.get_height() - 10
                    screen.blit(HEART_IMG, (x, y))

                # Dibujar botón de ajustes
                screen.blit(SETTINGS_IMG, settings_rect)
                
                # Mostrar "Pausa" si el juego está pausado
                if game_paused and not game_over:
                    pause_text = font.render("PAUSA", True, (255, 255, 255))
                    screen.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2, 50))
                
                # Comprobar condiciones de fin de juego
                if all(card.is_matched for card in board) and not game_paused:
                    if not confetti_triggered:
                        confetti_particles = [ConfettiParticle() for _ in range(300)]
                        confetti_triggered = True
                    
                    show_level_complete(screen, level, confetti_particles)
                    level += 1  # Pasar al siguiente nivel
                    break  # Salir del bucle del nivel actual
                    
                elif game_over:
                    show_game_over(screen)
                    break  # Volver al menú principal

                # Mostrar temporizador (solo si no está pausado)
                # Mostrar temporizador llamativo (estilo Minecraft)
                if not game_paused and not game_over and not all(card.is_matched for card in board):
                 elapsed_seconds = (pygame.time.get_ticks() - start_ticks - paused_time) // 1000
                draw_text_with_outline(screen, f"Tiempo: {elapsed_seconds}s", font, 10, HEIGHT - 40, (255, 255, 0), (0, 0, 0))


                pygame.display.flip()

            # Si game_over es True, salimos del bucle de niveles
            if game_over:
                break

if __name__ == "__main__":
    main()