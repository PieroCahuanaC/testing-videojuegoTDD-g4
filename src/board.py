import random
from src.card import Card

class Board:
    def __init__(self, card_ids):
        # Creamos pares a partir de los IDs proporcionados
        self.cards = [Card(name, "img") for name in card_ids * 2]
        random.shuffle(self.cards)
        self.selected_cards = []

    def select_card(self, index):
        card = self.cards[index]
        if not card.revealed and not card.matched:
            card.reveal()
            self.selected_cards.append(card)

    def check_match(self):
        if len(self.selected_cards) != 2:
            return False

        c1, c2 = self.selected_cards
        if c1.is_match(c2):
            c1.match()
            c2.match()
            self.selected_cards.clear()
            return True
        else:
            c1.hide()
            c2.hide()
            self.selected_cards.clear()
            return False

    def all_matched(self):
        return all(card.matched for card in self.cards)
