from server.model.lobby import Lobby
from server.model.player import Player

from server.networking.server import Server


def get_player(clientID, command:str):
    name = command.split(":")[-1]
    return Player(name, clientID)


def create_lobby(server: Server, host: Player, command: str):
    command = command.split(":")
    lobby_name = command[-1]
    lobby = Lobby(host, lobby_name)
    server.add_lobby(lobby)


def show_lobbies(server: [Server]):
    return server.get_lobbies()


def join_lobby(player: Player, server: Server, command: str):
    command = command.split(':')
    lobby_name = command[-1]
    lobby = server.get_lobby_by_name(lobby_name)
    lobby.add_player(player)


def leave_lobby(player: Player, server: Server, command: str):
    command = command.split(':')
    lobby_name = command[-1]
    lobby = server.get_lobby_by_name(lobby_name)
    lobby.remove_player(player)


def start_game(host: Player, server: Server):
    lobby = server.get_lobby_by_host(host)
    lobby.start_game()
