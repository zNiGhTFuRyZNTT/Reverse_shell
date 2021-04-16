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

server = WebSocketServer('127.0.0.1', 5050, Connect)
server.serve_forever()