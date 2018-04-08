__author__ = 'Guy Davidovich'

import os
from socket import *
from threading import Thread
import pickle

#smtp constants
smtp_port = 587
line_end = '\r\n'
smtp_connect_code = 220
smtp_okay_code = 250
smtp_connect_message = str(smtp_connect_code) + 'Connected to DMail server' + line_end

database_file_name = 'msgdb.pkl'
imap_port = 143


class Database(object):
    def __init__(self, file_name):
        self._file_name = file_name

    def _get_data(self):
        if not os.path.exists(self._file_name):
            return {}

        pickle_file = open(self._file_name, "r")
        data_dict = pickle.load(pickle_file)
        pickle_file.close()
        return data_dict

    def get_messages(self, username):
        return self._get_data().get(username)

    def add_message(self, username, new_message):
        data = self._get_data()
        if username not in data.keys():
            data[username] = [new_message]
        else:
            data[username].append(new_message)
        pickle_file = open(self._file_name, "w")
        pickle.dump(data, pickle_file)
        pickle_file.close()


def send_messages(client_socket):
    msg_db = Database(database_file_name)
    username = client_socket.recv(1024)
    print 'the messages of ' + username
    messages = msg_db.get_messages(username)
    print messages
    client_socket.send(str(len(messages)))
    for message in messages:
        print message
        client_socket.send(message)
    print 'messages sent'


def imap_server():
    server = socket()
    server.bind(('0.0.0.0', imap_port))
    server.listen(1)
    while True:
        client, address = server.accept()
        print 'connected to client'
        send_messages(client)
        client.close()
    server.close()


def upload_message_to_database(message):
    msg_db = Database(database_file_name)
    receiver = message.split('\n')[1][4:]
    print 'the message was sent to ' + receiver
    msg_db.add_message(receiver, message)


def smtp_communication(client):
    client.send(smtp_connect_message)
    print smtp_connect_message
    client_command = client.recv(1024)
    print client_command
    if client_command.startswith('HELO') or client_command.startswith('EHLO'):
        client_host = client_command.split()[1]
        print 'client host ' + client_host
        server_response = str(smtp_okay_code) + line_end
        print server_response
        client.send(server_response)
        client_command = client_command.recv(1024)
        print client_command
        if client_command.startswith('MAIL'):
            pass
        else:
            pass
    else:
        pass


def smtp_server():
    server = socket()
    server.bind(('0.0.0.0', smtp_port))
    server.listen(1)
    while True:
        client_socket, address = server.accept()
        message = smtp_communication(client_socket)
        upload_message_to_database(message)
        client_socket.close()
    server.close()


def main():
    receive_mail = Thread(target=smtp_server)
    send_mail_to_clients = Thread(target=imap_server)
    receive_mail.start()
    send_mail_to_clients.start()


if __name__ == '__main__':
    main()