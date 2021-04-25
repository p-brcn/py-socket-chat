
import threading
import socket

username = input('choose a username: ')
if username == 'admin':
    password = input('Enter password for admin: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

stop_thread = False


def receive():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NAME':
                client.send(username.encode('ascii'))
                next_message = client.recv(1024).decode('ascii')
                if next_message == 'PASS':
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii') == 'REFUSE':
                        print('Connection was refused.')
                        stop_thread = True
                elif next_message == 'BAN':
                    print('Connection refused caus u banned.')
                    client.close()
                    stop_thread = True
            else:
                print(message)
        except:
            print('An error occurred.')
            client.close()
            break


def write():
    while True:
        if stop_thread:
            break
        message = f'{username}: {input("")}'
        if message[len(username) + 2 :].startswith('/'):
            if username == 'admin':
                if message[len(username) + 2 :].startswith('/kick'):
                    client.send(
                        f'KICK{message[len(username)+2+6]}'.encode('ascii'))
                elif message[len(username) + 2 :].startswith('/ban'):
                    client.send(
                        f'KICK{message[len(username)+2+5]}'.encode('ascii'))
            else:
                print('must be admin.')
        else:
            client.send(message.encode('ascii'))
        print('>>')


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
