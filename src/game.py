from .board import Board

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
        self.tiempo_restante = 60  # segundos por nivel

    def play_turn(self, index):
        if self.paused or not self.in_game:
            return

        self.board.select_card(index)
        if len(self.board.selected_cards) == 2:
            self.attempts += 1
            if self.board.check_match():
                self.score += 1
                if self.board.all_matched():
                    self.confetti_activo = True
                    self.nivel += 1
                    self.tiempo_restante = 60
                    self.board = Board([card.name for card in self.board.cards[:len(self.board.cards)//2]])
            else:
                self.lives -= 1
                if self.lives <= 0:
                    self.in_game = False

    def game_over(self):
        return self.lives <= 0 or self.tiempo_restante <= 0 or self.board.all_matched()

    def reiniciar(self):
        self.score = 0
        self.attempts = 0
        self.lives = 5
        self.in_game = True
        self.paused = False
        self.confetti_activo = False
        self.tiempo_restante = 60
        self.board = Board([card.name for card in self.board.cards[:len(self.board.cards)//2]])

    def salir_a_menu(self):
        self.in_game = False

    def toggle_pause(self):
        self.paused = not self.paused

    def tick(self):
        if self.paused or not self.in_game:
            return
        self.tiempo_restante -= 1
        if self.tiempo_restante <= 0:
            self.in_game = False
