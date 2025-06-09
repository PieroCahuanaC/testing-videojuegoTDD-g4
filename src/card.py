class Card:
    def __init__(self, name, image):
        self.name = name          # Nombre identificador de la carta
        self.image = image        # Imagen asociada a la carta
        self.revealed = False     # Indica si la carta está visible
        self.matched = False      # Indica si la carta ya fue emparejada

    def reveal(self):
        if not self.matched:      # Solo se revela si no está emparejada
            self.revealed = True

    def hide(self):
        if not self.matched:      # Solo se puede ocultar si no está emparejada
            self.revealed = False

    def match(self):
        self.matched = True       # Marca la carta como emparejada

    def is_match(self, other_card):
        return self.name == other_card.name  # Verifica si dos cartas hacen pareja
