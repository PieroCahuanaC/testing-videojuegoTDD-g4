from .board import Board

class Game:
    def __init__(self, card_ids):
        self.board = Board(card_ids)
        self.score = 0
        self.attempts = 0

    def play_turn(self, index):
        self.board.select_card(index)
        if len(self.board.selected_cards) == 2:
            self.attempts += 1
            if self.board.check_match():
                self.score += 1

    def game_over(self):
        return self.board.all_matched()
