class Card:
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number

    def __repr__(self):
        return f'Card("{self.suit}", "{self.number}")'
