import random

from model.game import Game
from model.player import Player
from model.card import Card


# todo: make this dynamic, so you could also play with something other than 4 players
HANDS_PER_ROUND = 13
TOTAL_PLAYERS = 4

suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
numbers = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
player_names = ["AI_one", "AI_two", "AI_three", "human_player"]


class GameController:
    def __init__(self, players: [Player]):
        deck = initialize_deck()
        # todo: make it so the game controller adds as many bots as is needed to reach 4 players
        players = players
        self.game = initialize_game(deck, players)

    def play(self):
        highest_score = 0
        while highest_score < 100:
            self.start_round()
            self.play_round()
            for player in self.game.__players:
                if player.get_score() > highest_score:
                    highest_score = player.get_score()

    def start_round(self):
        """
        shuffles the deck
        updates the scores
        resets the players cards
        deals new cards
        :return:
        """
        game = self.game
        game.__can_play_hearts = False
        cards_dealt = 0
        random.shuffle(game.__deck)
        for player in game.__players:
            cards = game.__deck[cards_dealt: cards_dealt + HANDS_PER_ROUND]
            cards = sort_cards(cards)
            cards_dealt += HANDS_PER_ROUND
            player.start_round(cards)
            for card in cards:
                if card.suit == "Clubs" and card.number == "2":
                    game.__next_player_to_move = player

    def play_round(self):
        """
        plays HANDS_PER_ROUND hands
        :return:
        """
        for hand in range(0, HANDS_PER_ROUND):
            self.play_hand()

    def play_hand(self):
        """
        lets all players pick a card
        calculates which card is the highest
        adds the cards to the player that won the hand
        lets the game know what cards have been played
        :return:
        """
        game = self.game
        # let all players play a card
        for player in game.get_players_in_order():
            player.play_card()
        # pick the highest played card
        (winning_player, winning_card) = pick_hand_winner(game.get_cards_played_in_hand())
        winning_player.add_earned_cards([card for (player, card) in game.get_cards_played_in_hand()])
        game.first_player = winning_player
        game.add_played_hand(game.get_cards_played_in_hand())
        self.game.__cards_played_in_hand = []


def initialize_deck():
    deck = []
    for suit in suits:
        for number in numbers:
            deck.append(Card(suit=suit, number=number))
    return deck


def initialize_players():
    players = []
    for name in player_names:
        players.append(Player(name))
    return players


def initialize_game(deck, players):
    game = Game(deck=deck, players=players)
    for player in players:
        player.set_game(game)
    return game


def pick_hand_winner(played_cards: [()]):
    (first_player, first_card) = winner = played_cards[0]
    starting_suit = first_card.suit
    for (player, card) in played_cards[1:]:
        (winning_player, winning_card) = winner
        if card.suit == starting_suit and numbers.index(card.number) > numbers.index(winning_card.number):
            winner = (player, card)
    return winner


def sort_cards(cards: [Card]):
    result = []
    clubs = []
    diamonds = []
    spades = []
    hearts = []
    for card in cards:
        if card.suit == "Clubs":
            clubs.append(card)
        elif card.suit == "Diamonds":
            diamonds.append(card)
        elif card.suit == "Spades":
            spades.append(card)
        else:
            hearts.append(card)
    result.extend(sort_suit(clubs))
    result.extend(sort_suit(diamonds))
    result.extend(sort_suit(spades))
    result.extend(sort_suit(hearts))
    return result


def sort_suit(cards: [Card]):
    result = []
    args = {}
    for card in cards:
        number = card.number
        if number == "Jack":
            number = 11
        elif number == "Queen":
            number = 12
        elif number == "King":
            number = 13
        elif number == "Ace":
            number = 14
        number = int(number)
        args[number] = card
    mylist = list(args.keys())
    mylist.sort()
    for key in mylist:
        result.append(args[key])
    return result





