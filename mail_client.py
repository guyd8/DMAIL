__author__ = 'Guy Davidovich'

from socket import *

smtp_port = 587
server_ip = '127.0.0.1'
imap_port = 143


def receive_messages():
    username = raw_input('Enter your name\n')
    receiver_client = socket()
    receiver_client.connect((server_ip, imap_port))
    receiver_client.send(username)
    number_of_messages = int(receiver_client.recv(1024))
    for i in range(number_of_messages):
        message = receiver_client.recv(1024)
        print message
    receiver_client.close()


def send_message(message):
    sender_client = socket()
    sender_client.connect((server_ip, smtp_port))
    sender_client.send(message)
    sender_client.close()


def build_message():
    message = ''
    message += 'From: ' + raw_input('Enter your name\n') + '\n'
    message += 'To: ' + raw_input('Enter the recipient\'s name\n') + '\n'
    message += 'Title: ' + raw_input('Enter title\n') + '\n'
    message += 'Content: ' + raw_input('Enter message content\n') + '\n'
    print message
    print message.split('\n')
    send_message(message)


def main():
    response = raw_input('Would you like to send a message or receive a message?\n')
    if response == 'send':
        build_message()
    elif response == 'receive':
        receive_messages()

if __name__ == '__main__':
    main()