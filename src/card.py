class Card:
    def __init__(self, name, image):
        self.name = name
        self.image = image
        self.revealed = False
        self.matched = False

    def reveal(self):
        if not self.matched:
            self.revealed = True

    def hide(self):
        if not self.matched:
            self.revealed = False

    def match(self):
        self.matched = True

    def is_match(self, other_card):
        return self.name == other_card.name
