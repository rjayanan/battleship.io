import asyncio
import websockets
import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 5570

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

async def start_game(conn1, addr1, conn2, addr2):
    await conn1.send("Another Player has been found... Game is starting")
    await conn2.send("Another Player has been found... Game is starting")

async def handle_client(websocket, path):
    print(f"[NEW CONNECTION] {websocket} connected.")

    connected = True
    while connected:
        msg = await websocket.recv()
        if msg == DISCONNECT_MSG:
            connected = False
        if msg == READY_MSG:
            print(f"[{websocket}] is ready to play")
            await websocket.send("You are Ready... Please Wait In Queue until Another Player Joins")
            global PLAYERS_READY
            PLAYERS_READY += 1
            global conn1
            global conn2
            global addr1
            global addr2
            if conn1 is not None:
                conn2 = websocket
                addr2 = path
            conn1 = websocket
            addr1 = path

        print(f"[{websocket}] {msg}")
        # msg = f"Msg received: {msg}"

        await websocket.send(msg)

    await websocket.close()

async def main():
    print("[STARTING] Server is starting...")
    server = websockets.serve(handle_client, IP, PORT)
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    async with server:
        while True:
            await asyncio.sleep(100)
            global PLAYERS_READY
            global conn1
            global conn2
            global addr1
            global addr2
            if PLAYERS_READY > 2:
                print("starting game for two clients")
                await start_game()
                PLAYERS_READY = 0
                conn1 = None
                conn2 = None
                addr1 = None
                addr2 = None

asyncio.run(main())
