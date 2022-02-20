import socket
import os
from _thread import *

from client_connection import clientConnection
from server.model.lobby import Lobby
from server.model.player import Player


class Server:
    def __init__(self):
        self.__host = '127.0.0.1'
        self.__port = 2004
        self.__server_side_socket = socket.socket()
        self.__server_side_socket.bind((self.__host, self.__port))
        self.__client_count = 0
        self.__do_listen_for_new_clients = False
        self.__lobbies = []

    def listen_for_new_clients(self):
        print('Socket is listening for new clients...')
        server_side_socket = self.__server_side_socket
        server_side_socket.listen(5)
        self.__do_listen_for_new_clients = True
        while self.__do_listen_for_new_clients:
            Client, address = server_side_socket.accept()
            print('Connected to: ' + address[0] + ':' + str(address[1]))
            start_new_thread(clientConnection, (Client,))
            self.__client_count += 1
            print('Thread Number: ' + str(self.__client_count))
        server_side_socket.close()

    def stop_listen_for_new_clients(self):
        self.__do_listen_for_new_clients = False

    def add_lobby(self, lobby: Lobby):
        self.__lobbies.append(lobby)

    def remove_lobby(self, lobby: Lobby):
        self.__lobbies.remove(lobby)

    def get_lobbies(self):
        return self.__lobbies

    def get_lobby_by_name(self, lobby_name) -> Lobby:
        for lobby in self.__lobbies:
            if lobby.get_lobby_name() == lobby_name:
                return lobby
        raise LookupError("Lobby does not exist")

    def get_lobby_by_host(self, host: Player) -> Lobby:
        for lobby in self.__lobbies:
            if lobby.get_host() == host:
                return lobby
        raise LookupError("Lobby does not exist")


if __name__ == "__main__":
    server = Server()
    server.listen_for_new_clients()