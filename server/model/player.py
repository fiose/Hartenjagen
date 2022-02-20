import random

from model.card import Card
from model.game import Game


class Player:
    def __init__(self, name: str, clientID: int):
        self.__name = name
        self.__clientID = clientID
        self.__game = None
        self.__holding_cards = []
        self.__earned_cards = []
        self.__points_round = 0
        self.__points_game = 0

    def __repr__(self):
        return f'Player(name: "{self.__name}"' \
               f'holding_cards: "{self.__earned_cards}", ' \
               f'earned_cards: "{self.__earned_cards}", ' \
               f'points_round: "{self.__points_round}", ' \
               f'points_game: "{self.__points_game}"' \
               f')'

    def play_card(self):
        playable_cards = self.get_playable_cards()
        card = random.sample(playable_cards, 1)[0]
        self.__holding_cards.remove(card)
        self.__game.get_cards_played_in_hand().append((self, card))
        return card

    def get_playable_cards(self):
        game = self.__game
        cards_played_in_hand = game.get_cards_played_in_hand()
        playable_cards = self.__holding_cards.copy()
        if len(cards_played_in_hand) == 0:
            if not game.__can_play_hearts:
                for card in playable_cards:
                    print(f'checking {card} from {playable_cards}')
                    if card.suit == "Clubs" and card.number == "2":
                        return [card]
                    if card.suit == "Hearts":
                        playable_cards.remove(card)
                        print(f'removed {card} from {playable_cards}')
                if not playable_cards:
                    return self.__holding_cards

        else:
            (starting_player, starting_suit) = cards_played_in_hand[0]
            for card in playable_cards:
                if not card.suit == starting_suit:
                    playable_cards.remove(card)
            if not playable_cards:
                return self.__holding_cards
        return playable_cards

    def start_round(self, cards: [Card]):
        self.__points_game += self.__points_round
        self.__points_round = 0
        self.__holding_cards = cards
        self.__earned_cards = []

    def get_score(self):
        return self.__points_game

    def set_game(self, game: Game):
        self.__game = game

    def add_earned_cards(self, cards: [Card]):
        self.__earned_cards.append(cards)
        for card in cards:
            if card.suit == "Hearts":
                self.__points_round += 1
            elif card.suit == "Spades" and card.number == "Queen":
                self.__points_round += 13

    def reset_earned_cards(self):
        self.__earned_cards = []

    def get_holding_cards(self):
        return self.__holding_cards

    def get_name(self):
        return self.__name
