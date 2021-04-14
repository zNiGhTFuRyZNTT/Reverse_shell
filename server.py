import socket
import sys

def send_commands(s, conn):
    """Get a command from the user and send it to the client."""
    print("\nCtrl + C to kill the connection.\n")
    # test 
    data1 = conn.recv(4096).decode()
    
    # ------
    print(f"{data1}", end="")
    while True:
        try:
            cmd = input()
            if len(cmd) > 0:
                conn.sendall(cmd.encode())
                data = conn.recv(4096) # avaz nashe, high capacity
                print(data.decode("utf-8"), end="")
        except KeyboardInterrupt:
            print("\nGoodbye.")
            conn.close()
            sys.exit()
        except Exception as e:
            print(e)
            conn.close()
            e.close()
            sys.exit()

def server(address):
    """Initialize a socket server and wait for connections."""
    try:
        s = socket.socket()
        s.bind(address)
        s.listen()
        print("Server Initialized. I'm listening...")
    except Exception as e:
        print("\nIt seems like something went wrong.")
        print(e)
        restart = input("\nDo you want me to reinitialize the server? y/n ")
        if restart.lower() == "y" or restart.lower() == "yes":
            print("\nRoger That. Reinitializing the server...\n")
            server(address)
        else:
            print("\nSo Long, and Thanks for All the Fish.\n")
            sys.exit()
    conn, client_addr = s.accept()
    print(f"Connection Established: {client_addr}")
    send_commands(s, conn)

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5050
    server((host, port))
        