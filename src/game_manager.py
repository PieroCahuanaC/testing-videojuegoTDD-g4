import pygame
import sys
import random
import os
from src.settings import WIDTH, HEIGHT, CARD_SIZE, CARD_BACK, HEART_IMG, SETTINGS_IMG, BACKGROUND_IMG, CARD_NAMES, MAX_LIVES, GAP, FPS

from .card import Card
from .menu import (
    show_menu,
    pause_menu,
    show_level_complete,
    show_game_over,
    draw_text_with_outline,
)

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

class GameManager:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)

    def create_board(self, level):
        from .card_ui import CardUI

        num_pairs = min(level + 1, len(CARD_NAMES))
        selected_names = CARD_NAMES[:num_pairs] * 2
        random.shuffle(selected_names)
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

        board = []
        idx = 0
        for row in range(rows):
            for col in range(cols):
                if idx >= total_cards:
                    break
                x = offset_x + col * (CARD_SIZE[0] + GAP)
                y = offset_y + row * (CARD_SIZE[1] + GAP)

                card_logic = Card(selected_names[idx])
                rect = pygame.Rect(x, y, CARD_SIZE[0], CARD_SIZE[1])
                card_ui = CardUI(card_logic, rect)

                board.append(card_ui)
                idx += 1

        return board

    def run(self):
        while True:
            choice = show_menu(self.screen, self.font, BACKGROUND_IMG)
            if choice == "Salir":
                pygame.quit()
                sys.exit()

            level = 1
            back_to_menu = False

            while not back_to_menu:
                board = self.create_board(level)
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

                running = True
                while running:
                    self.clock.tick(FPS)
                    self.screen.blit(BACKGROUND_IMG, (0, 0))

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            pos = pygame.mouse.get_pos()
                            if settings_rect.collidepoint(pos) and not game_over:
                                game_paused = True
                                pause_start = pygame.time.get_ticks()
                                option_index = pause_menu(self.screen, self.font, BACKGROUND_IMG)
                                paused_time += pygame.time.get_ticks() - pause_start
                                if option_index == 0:
                                    game_paused = False
                                elif option_index == 1:
                                    running = False
                                    back_to_menu = True
                                    break
                            elif not waiting and not game_over and not game_paused:
                                for card in board:
                                    if card.rect.collidepoint(pos) and not card.card.is_flipped and not card.card.is_matched:
                                        card.card.flip()
                                        flipped_cards.append(card)
                                        break

                    if not game_paused and not game_over:
                        if len(flipped_cards) == 2 and not waiting:
                            c1, c2 = flipped_cards
                            if c1.card.name == c2.card.name:
                                c1.card.is_matched = True
                                c2.card.is_matched = True
                                flipped_cards = []
                            else:
                                lives -= 1
                                waiting = True
                                wait_start_time = pygame.time.get_ticks()

                        if waiting and pygame.time.get_ticks() - wait_start_time >= WAIT_TIME:
                            for card in flipped_cards:
                                card.card.flip()
                            flipped_cards = []
                            waiting = False

                        if lives <= 0:
                            game_over = True

                    for card in board:
                        card.draw(self.screen)

                    for i in range(lives):
                        x = WIDTH // 2 - (MAX_LIVES * (HEART_IMG.get_width() + 5)) // 2 + i * (HEART_IMG.get_width() + 5)
                        y = HEIGHT - HEART_IMG.get_height() - 10
                        self.screen.blit(HEART_IMG, (x, y))

                    self.screen.blit(SETTINGS_IMG, settings_rect)

                    if game_paused and not game_over:
                        pause_text = self.font.render("PAUSA", True, (255, 255, 255))
                        self.screen.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2, 50))

                    if all(card.card.is_matched for card in board) and not game_paused:
                        if not confetti_triggered:
                            confetti_particles = [ConfettiParticle() for _ in range(300)]
                            confetti_triggered = True
                        show_level_complete(self.screen, level, confetti_particles)
                        level += 1
                        break
                    elif game_over:
                        show_game_over(self.screen)
                        break

                    if not game_paused and not game_over and not all(card.card.is_matched for card in board):
                        elapsed_seconds = (pygame.time.get_ticks() - start_ticks - paused_time) // 1000
                        draw_text_with_outline(self.screen, f"Tiempo: {elapsed_seconds}s", self.font, 10, HEIGHT - 40, (255, 255, 0), (0, 0, 0))

                    pygame.display.flip()

                if game_over:
                    break
