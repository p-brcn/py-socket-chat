"""Server Host."""
import threading
import socket

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
usernames = []


def main():
    """Initialize server."""
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    print('Server started.')


def broadcast(message):
    """Broadcast  messages between clients."""
    print(f'{message}')
    for client in clients:
        client.send(message)


def handle(client):
    """Handle clients."""
    while True:
        try:
            msg = message = client.recv(1024)
            if msg.decode('ascii').startswith('KICK'):
                if usernames[clients.index(client)] == 'admin':
                    user_to_kick = msg.decode('ascii')[5:]
                    kick_user(user_to_kick)
                else:
                    client.send('command was refused'.encode('ascii'))
            elif msg.decode('ascii').startswith('BAN'):
                if usernames[clients.index(client)] == 'admin':
                    user_to_ban = msg.decode('ascii')[4:]
                    kick_user(user_to_ban)
                    with open('bans.txt', 'a') as f:
                        f.write(f'{user_to_ban}\n')
                    print(f'{user_to_ban} was banned.')
                else:
                    client.send('command was refused'.encode('ascii'))
            else:
                broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close
            username = usernames[index]
            broadcast(f'{username} left the chat.'.encode('ascii'))
            usernames.remove(username)
            break


def receive():
    """Recive messages from clients."""
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        client.send('NAME'.encode('ascii'))

        username = client.recv(1024).decode('ascii')

        with open('bans.txt', 'r') as f:
            bans = f.readlines()
        
        if username + '\n' in bans:
            client.send('BAN'.encode('ascii'))
            client.close()
            continue

        if username == 'admin':
            client.send('PASS'.encode('ascii'))
            password = client.recv(1024).decode('ascii')

            if password != 'password':
                client.send('REFUSE'.encode('ascii'))
                client.close()
                continue

        usernames.append(username)
        clients.append(client)

        print(f'Username of the client is {username}.')
        broadcast(f'{username} has joined the chat.'.encode('ascii'))
        client.send('Connected to the server.'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


def kick_user(user):
    if user in usernames:
        user_index = usernames.index(user)
        client_to_kick = clients[user_index]
        clients.remove(client_to_kick)
        client_to_kick.send(
            'You were kicked by an admin loser.'.encode('ascii'))
        usernames.remove(user)
        broadcast(f'{name} was kicked by an admin.'.encode('ascii'))


if __name__ == "__main__":
    main()
