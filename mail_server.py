__author__ = 'Guy Davidovich'

import os
from socket import *
from threading import Thread
import pickle

smtp_port = 587
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


def imap_client():
    client_server = socket()
    client_server.bind(('0.0.0.0', imap_port))
    client_server.listen(1)
    while True:
        client, address = client_server.accept()
        print 'connected to client'
        send_messages(client)
        client.close()
    client_server.close()


def upload_message_to_database(message):
    msg_db = Database(database_file_name)
    receiver = message.split('\n')[1][4:]
    print 'the message was sent to ' + receiver
    msg_db.add_message(receiver, message)


def smtp_server():
    smtp_server = socket()
    smtp_server.bind(('0.0.0.0', smtp_port))
    smtp_server.listen(1)
    while True:
        client_socket, address = smtp_server.accept()
        print 'connected to smtp server'
        message = client_socket.recv(1024)
        print message
        upload_message_to_database(message)
        client_socket.close()
    smtp_server.close()


def main():
    smtp_communication = Thread(target=smtp_server)
    imap_client_communication = Thread(target=imap_client)
    smtp_communication.start()
    imap_client_communication.start()


if __name__ == '__main__':
    main()