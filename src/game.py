from .card import Card
import random

class Game:
    def __init__(self, card_ids):
        self.cards = self._create_board(card_ids)
        self.selected = []
        self.attempts = 0
        self.score = 0

    def _create_board(self, ids):
        pairs = ids * 2
        random.shuffle(pairs)
        return [Card(name, "img") for name in pairs]

    def play_turn(self, index):
        card = self.cards[index]
        if card.revealed or card.matched:
            return

        card.reveal()
        self.selected.append(card)

        if len(self.selected) == 2:
            self.attempts += 1
            if self.selected[0].is_match(self.selected[1]):
                self.selected[0].match()
                self.selected[1].match()
                self.score += 1
            else:
                self.selected[0].hide()
                self.selected[1].hide()
            self.selected = []

    def game_over(self):
        return all(card.matched for card in self.cards)
