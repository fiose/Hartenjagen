from player import Player
from server.control.game_controller import GameController


class Lobby:
    def __init__(self, host: Player, lobby_name):
        self.__lobby_name = lobby_name
        self.__host = host
        self.__players = [host]
        self.__game = None

    def add_player(self, player: Player):
        self.__players.append(player)

    def remove_player(self, player: Player):
        self.__players.remove(player)

    def get_lobby_name(self):
        return self.__lobby_name

    def get_host(self):
        return self.__host

    def start_game(self):
        game_controller = GameController(self.__players)
