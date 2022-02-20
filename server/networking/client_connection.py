from server.control import client_command_handler
from server.networking.server import Server


class clientConnection:
    def __init__(self, server: Server, connection, clientID):
        self.__server = server
        self.__connection = connection
        self.__do_listen_for_incoming_messages = False
        self.__player = self.initialize_player(clientID)
        if self.__player is not None:
            self.listen_for_incoming_messages()

    def initialize_player(self, clientID):
        connection = self.__connection
        connection.send(str.encode('Server is working, please provide player name'))
        data = connection.recv(2048)
        if not data:
            connection.close()
            return None
        return client_command_handler.get_player(clientID, repr(data))

    def listen_for_incoming_messages(self):
        connection = self.__connection
        self.__do_listen_for_incoming_messages = True
        while self.__do_listen_for_incoming_messages:
            data = connection.recv(2048)
            if not data:
                break
            command = repr(data)
            if command.startswith("create lobby"):
                client_command_handler.create_lobby(self.__server, self.__player, command)
                response = b'Success: Lobby created'
            elif command.startswith("show lobbies"):
                lobbies = client_command_handler.show_lobbies(self.__server)
                response = b'Success: ' + lobbies
            elif command.startswith("join lobby"):
                client_command_handler.join_lobby(self.__player, self.__server, command)
                response = b'Success: Joined lobby'
            elif command.startswith("leave lobby"):
                client_command_handler.leave_lobby(self.__player, self.__server, command)
                response = b'Success: Left lobby'
            elif command.startswith("start game"):
                client_command_handler.start_game(self.__player, self.__server)
                response = b''
            else:
                response = b'Error: Command not found'
            connection.sendall(response)
        connection.close()

    def stop_listen_for_incoming_messages(self):
        self.__do_listen_for_incoming_messages = False
