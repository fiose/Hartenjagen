class Game:
    def __init__(self, players, deck):
        self.__players = players
        self.__next_player_to_move = None
        self.__deck = deck
        self.__hands_played_in_round = []
        self.__cards_played_in_hand = []
        self.__can_play_hearts = False

    def get_players_in_order(self):
        index = self.__players.index(self.first_player)
        return self.__players[index:4] + self.__players[0:index]

    def get_played_cards(self):
        cards = []
        for hand in self.__hands_played_in_round:
            for (player, card) in hand:
                cards.append(card)
        return cards

    def add_played_hand(self, hand):
        self.__hands_played_in_round.append(hand)

    def add_played_card(self, player, card):
        self.__cards_played_in_hand.append((player, card))
        if not self.__can_play_hearts and card.suit == "Hearts":
            self.__can_play_hearts = True

    def reset_cards_played_in_hand(self):
        self.__cards_played_in_hand = []

    def get_cards_played_in_hand(self) -> list:
        return self.__cards_played_in_hand

    def get_hands_played_in_round(self) -> list:
        return self.__hands_played_in_round





