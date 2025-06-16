import pygame
import os
import random
import sys

# Configuración inicial
WIDTH, HEIGHT = 800, 600
FPS = 30
CARD_SIZE = (100, 140)
GAP = 20
ROWS, COLS = 3, 4
MAX_LIVES = 5


# Ruta absoluta al directorio actual
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "cards")

# Carga de imágenes con rutas absolutas
CARD_BACK = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_DIR, "card_back.png")), CARD_SIZE)
HEART_IMG = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_DIR, "heart.png")), (40, 40))
SETTINGS_IMG = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_DIR, "ajustes.png")), (50, 50))
BACKGROUND_IMG = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_DIR, "fondo.png")), (WIDTH, HEIGHT))

# Nombres de cartas
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

def create_board():
    card_names = CARD_NAMES * 2
    random.shuffle(card_names)
    board = []

    total_width = COLS * CARD_SIZE[0] + (COLS - 1) * GAP
    total_height = ROWS * CARD_SIZE[1] + (ROWS - 1) * GAP

    offset_x = (WIDTH - total_width) // 2
    offset_y = (HEIGHT - total_height) // 2 - 30

    for row in range(ROWS):
        for col in range(COLS):
            x = offset_x + col * (CARD_SIZE[0] + GAP)
            y = offset_y + row * (CARD_SIZE[1] + GAP)
            board.append(Card(card_names.pop(), (x, y)))
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
                color = (70, 130, 180)
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
    pause_options = ["Reiniciar", "Volver al Menú"]
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
                    return option
            else:
                color = (70, 70, 70)
                text_color = (200, 200, 200)

            pygame.draw.rect(screen, color, rect, border_radius=10)
            text_surf = font.render(option, True, text_color)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)

        pygame.display.flip()
        clock.tick(FPS)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Memory Match Game")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    while True:
        choice = show_menu(screen, font)
        if choice == "Salir":
            pygame.quit()
            sys.exit()

        board = create_board()
        flipped_cards = []
        waiting = False
        wait_start_time = 0
        WAIT_TIME = 1000
        lives = MAX_LIVES
        game_over = False
        paused = False

        settings_rect = SETTINGS_IMG.get_rect(topright=(WIDTH - 10, 10))

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
                    if settings_rect.collidepoint(pos):
                        paused = True
                    elif not waiting and not game_over and not paused:
                        for card in board:
                            if card.rect.collidepoint(pos) and not card.is_flipped and not card.is_matched:
                                card.flip()
                                flipped_cards.append(card)
                                break

            if paused:
                option = pause_menu(screen, font)
                if option == "Reiniciar":
                    board = create_board()
                    flipped_cards = []
                    waiting = False
                    wait_start_time = 0
                    lives = MAX_LIVES
                    game_over = False
                    paused = False
                elif option == "Volver al Menú":
                    paused = False
                    running = False

            if not game_over and not paused:
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

            for card in board:
                card.draw(screen)

            for i in range(lives):
                x = WIDTH // 2 - (MAX_LIVES * (HEART_IMG.get_width() + 5)) // 2 + i * (HEART_IMG.get_width() + 5)
                y = HEIGHT - HEART_IMG.get_height() - 10
                screen.blit(HEART_IMG, (x, y))

            screen.blit(SETTINGS_IMG, settings_rect)

            if all(card.is_matched for card in board):
                win_text = font.render("¡Ganaste!", True, (0, 255, 0))
                screen.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2 - win_text.get_height()//2))
            elif game_over:
                lose_text = font.render("¡Game Over!", True, (255, 0, 0))
                screen.blit(lose_text, (WIDTH//2 - lose_text.get_width()//2, HEIGHT//2 - lose_text.get_height()//2))

            pygame.display.flip()

if __name__ == "__main__":
    main()
