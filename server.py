from simple_websocket_server import WebSocketServer, WebSocket
import os

class Connect(WebSocket):
    def handle(self):
        x = self.data
        cmd = input(x)
        if 'cls' in cmd:
          self.send_message("cls")

          os.system("clear")
            
        elif len(cmd) > 0:
            self.send_message(cmd)




    def connected(self):
        print(self.address, 'connected')

    


    def handle_close(self):
        print(self.address, 'closed')


HOST = '127.0.0.1'
PORT = 80
server = WebSocketServer(HOST, PORT, Connect)
print(f"Listening on {HOST}:{PORT}...")
server.serve_forever()