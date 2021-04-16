from simple_websocket_server import WebSocketServer, WebSocket


class Connect(WebSocket):
    def handle(self):
        print(f"{self.data}", end="")
        cmd = input()
        if len(cmd) > 0:
            self.send_message(cmd)
            print(self.data)


    def connected(self):
        print(self.address, 'connected')

    

    
    def handle_close(self):
        print(self.address, 'closed')

LHOST = '127.0.0.1'
LPORT = 5050
server = WebSocketServer(LHOST, LPORT, Connect)
print("Listening on {LHOST}:{LPORT}")
server.serve_forever()