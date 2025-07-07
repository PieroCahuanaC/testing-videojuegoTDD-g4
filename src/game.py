# src/game.py

from .board import Board
from src.settings import WIDTH, HEIGHT, CARD_SIZE, CARD_BACK, HEART_IMG, SETTINGS_IMG, BACKGROUND_IMG, CARD_NAMES, MAX_LIVES, GAP, FPS

class Game:
    def __init__(self, card_ids):
        self.board = Board(card_ids)
        self.score = 0
        self.attempts = 0
        self.lives = 5
        self.in_game = True
        self.paused = False
        self.confetti_activo = False
        self.nivel = 1
        self.tiempo_inicial = 0  # Tiempo desde el inicio (en segundos)

    def play_turn(self, index):
        if self.paused or not self.in_game:
            return

        prev_selected = len(self.board.selected_cards)
        self.board.select_card(index)
        if len(self.board.selected_cards) == 2 and prev_selected != 2:
            self.attempts += 1
            if self.board.check_match():
                self.score += 1
                if self.board.all_matched():
                    self.confetti_activo = True
                    self.nivel += 1
                    self.board = Board([card.name for card in self.board.cards[:len(self.board.cards)//2]])
            else:
                self.lives -= 1
                if self.lives <= 0:
                    self.in_game = False


    def game_over(self):
        return self.lives <= 0

    def reiniciar(self):
        self.score = 0
        self.attempts = 0
        self.lives = 5
        self.in_game = True
        self.paused = False
        self.confetti_activo = False
        self.nivel = 1
        self.board = Board([card.name for card in self.board.cards[:len(self.board.cards)//2]])

    def salir_a_menu(self):
        self.in_game = False

    def toggle_pause(self):
        self.paused = not self.paused

    def reset_tiempo(self):
        self.tiempo_inicial = 0

    def incrementar_tiempo(self, segundos=1):
        if not self.paused and self.in_game:
            self.tiempo_inicial += segundos

    def tick(self):
        if not self.paused:
            self.tiempo_inicial += 1
