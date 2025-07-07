import pygame
import sys
import random
from src.settings import WIDTH, HEIGHT, CARD_SIZE, CARD_BACK, HEART_IMG, SETTINGS_IMG, BACKGROUND_IMG, CARD_NAMES, MAX_LIVES, GAP, FPS

WIDTH, HEIGHT = 800, 600
FPS = 30

def show_menu(screen, font, background_img):
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
        screen.blit(background_img, (0, 0))
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

def pause_menu(screen, font, background_img):
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
        screen.blit(background_img, (0, 0))
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
                    return i
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
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    big_font = pygame.font.SysFont(None, 72)
    small_font = pygame.font.SysFont(None, 36)

    main_text = big_font.render(f"¡Nivel {level} completado!", True, (0, 255, 0))
    main_rect = main_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
    sub_text = small_font.render("Haz clic para continuar", True, (255, 255, 255))
    sub_rect = sub_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))

    screen.blit(main_text, main_rect)
    screen.blit(sub_text, sub_rect)

    for particle in confetti_particles:
        particle.update()
        particle.draw(screen)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

def show_game_over(screen):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    big_font = pygame.font.SysFont(None, 72)
    small_font = pygame.font.SysFont(None, 36)

    main_text = big_font.render("¡Game Over!", True, (255, 0, 0))
    main_rect = main_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
    sub_text = small_font.render("Haz clic para volver al menú", True, (255, 255, 255))
    sub_rect = sub_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))

    screen.blit(main_text, main_rect)
    screen.blit(sub_text, sub_rect)
    pygame.display.flip()

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
