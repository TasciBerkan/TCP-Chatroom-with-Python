import threading
import socket
import sys

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

nickname = input("Choose your nickname: ")
secret = input("Choose your secret value: ")

def receive():
    while True:
        try:
            # Receive Message From Server
            message = client.recv(1024).decode('utf-8')
            if message == 'nickname':
                client.send(nickname.encode('utf-8'))
            elif message == 'secret':
                client.send(secret.encode('utf-8'))
            elif message == 'alone':
                print('Waiting for someone to connect')
            elif message == 'notalone':
                print('You are being connected to another user')
            elif message == 'timeout':
                print("session timeout")
                client.close()
                break
            else:
                print(message)
        except:
            # Close Connection When Error
            print("ERROR OCCURRED!")
            client.close()
            break
    sys.exit(0)

# Sending Messages To Server
def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('utf-8'))

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()