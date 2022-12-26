import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 5566

ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "quit"
READY_MSG = "ready"
PLAYERS_READY = 0

conn1 = None
conn2 = None
addr1 = None
addr2 = None
def start_game(conn1, addr1, conn2, addr2):
    conn1.send("Another Player has been found... Game is starting".encode(FORMAT))
    conn2.send("Another Player has been found... Game is starting".encode(FORMAT))

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg = conn.recv(SIZE).decode(FORMAT)
        if msg:
            if msg == DISCONNECT_MSG:
                connected = False
            if msg == READY_MSG:
                print(f"[{addr}] is ready to play")
                conn.send("You are Ready... Please Wait In Queue until Another Player Joins".encode(FORMAT))
                global PLAYERS_READY
                PLAYERS_READY+=1
                global conn1
                global conn2
                global addr1
                global addr2
                if(conn1!=None):
                    conn2 = conn
                    addr2= addr
                conn1=conn
                addr1= addr

            print(f"[{addr}] {msg}")
            # msg = f"Msg received: {msg}"
            
            conn.send(msg.encode(FORMAT))


    conn.close()

def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # For debugging on server side, we can just close server here so we don't create more than one socket to the IP and violate protocol
    #server.close()
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
        global PLAYERS_READY
        global conn1
        global conn2
        global addr1
        global addr2
        if(PLAYERS_READY > 2):
            print('starting game for two clients')
            start_game()
            PLAYERS_READY=0
            conn1 = None
            conn2 = None
            addr1 = None
            addr2 = None

if __name__ == "__main__":
    main()