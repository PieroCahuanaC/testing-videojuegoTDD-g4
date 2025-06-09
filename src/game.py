from .card import Card
import random

class Game:
    def __init__(self, card_ids):
        self.cards = self._create_board(card_ids)  # Genera y mezcla las cartas en pares
        self.selected = []     # Lista temporal de cartas seleccionadas en el turno
        self.attempts = 0      # Número de intentos realizados
        self.score = 0         # Puntaje acumulado por emparejamientos correctos

    def _create_board(self, ids):
        pairs = ids * 2                   # Duplica los identificadores para formar pares
        random.shuffle(pairs)            # Mezcla aleatoriamente las cartas
        return [Card(name, "img") for name in pairs]  # Crea objetos Card

    def play_turn(self, index):
        card = self.cards[index]
        if card.revealed or card.matched:
            return                       # Ignora si la carta ya está revelada o emparejada

        card.reveal()                    # Revela la carta seleccionada
        self.selected.append(card)

        if len(self.selected) == 2:      # Solo compara cuando hay dos cartas seleccionadas
            self.attempts += 1
            if self.selected[0].is_match(self.selected[1]):
                # Si hacen match, se marcan como emparejadas y se incrementa el puntaje
                self.selected[0].match()
                self.selected[1].match()
                self.score += 1
            else:
                # Si no hacen match, se ocultan ambas
                self.selected[0].hide()
                self.selected[1].hide()
            self.selected = []  # Reinicia la selección para el siguiente turno

    def game_over(self):
        # Retorna True si todas las cartas han sido emparejadas
        return all(card.matched for card in self.cards)
