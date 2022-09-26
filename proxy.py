import threading
import socket
import time
from collections import defaultdict

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists to store data
clients = []
nicknames = []
secretValues = defaultdict(lambda: 0)

# Message every client
def broadcast(message):
    for client in clients:
        client.send(message)

#Let the user know if they are alone or being connected to someone
def alone(client,secret):
    if secretValues.get(secret) <2:
        client.send('alone'.encode('utf-8'))
    else:
        client.send('notalone'.encode('utf-8'))

#Timeout after 30 seconds
def timer(client, nickname, secret):
    time.sleep(30)
    if secretValues.get(secret) < 2:
        print(f"{nickname}'s session timeout.")
        secretValues[secret] -= 1
        client.send('timeout'.encode('utf-8'))
        client.close()


# Handling client messages
def handle(client):
    while True:
        try:
            # Broadcasting messages
            message = client.recv(1024)
            print(message)
            broadcast(message)
        except:
            # Removing clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            #broadcast('{} left!'.format(nickname).encode('utf-8'))
            nicknames.remove(nickname)
            break

# Receiving / Listening Function
def recieve():
    while True:
        # Accept connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request and store names and secrets
        client.send('nickname'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')

        client.send('secret'.encode("utf-8"))
        secret = client.recv(1024).decode('utf-8')

        nicknames.append(nickname)
        clients.append(client)
        secretValues[secret] += 1

        # Print And Broadcast Nickname
        
        #print("Nickname is {}".format(nickname))
        #broadcast("{} joined!".format(nickname).encode('utf-8'))
        client.send('Connected to server!'.encode('utf-8'))



        timer_thread = threading.Thread(target=timer, args=(client, nickname, secret))
        timer_thread.start()

        alone_thread = threading.Thread(target=alone, args=(client,secret))
        alone_thread.start()

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is running")
recieve()
