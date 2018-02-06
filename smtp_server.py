__author__ = 'Guy Davidovich'

from socket import *

smtp_port = 587
imap_server_ip = '127.0.0.1'
smtp_to_imap_port = 587


def send_to_imap_server(message):
    sender = socket()
    sender.connect((imap_server_ip, smtp_to_imap_port))
    sender.send(message)
    sender.close()
    print 'message sent'


def receive_message_from_client(client_socket):
    message = client_socket.recv(1024)
    print message
    client_socket.close()
    return message


def main():
    server_socket = socket()
    server_socket.bind(('0.0.0.0', smtp_port))
    server_socket.listen(1)
    while True:
        client_socket, address = server_socket.accept()
        print 'client connected'
        message = receive_message_from_client(client_socket)
        send_to_imap_server(message)

    server_socket.close()


if __name__ == '__main__':
    main()