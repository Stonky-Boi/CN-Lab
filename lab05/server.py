import argparse
import logging
import socket
import threading

HOST = "127.0.0.1"

parser = argparse.ArgumentParser(description = "CS-313 Assignment 5")
parser.add_argument("port", type = int, help = "port number to listen on")
args = parser.parse_args()
if not 1 <= args.port <= 65535:
    parser.error("port must be between 1 and 65535")

PORT = args.port

logging.basicConfig(level = logging.INFO, format = "%(asctime)s | %(levelname)s | %(message)s", datefmt = "%H:%M:%S")
logger = logging.getLogger("server")

clients = {}
running = True

def handle_client(connection, address):
    username = None

    try:
        username = connection.recv(1024).decode().strip()
        if not username:
            connection.send("ERROR: Username cannot be empty.".encode())
            connection.close()
            return
        if username in clients:
            connection.send("ERROR: Username is already in use.".encode())
            connection.close()
            return
        clients[username] = connection
        logger.info("Client connected: %s (%s:%s)", username, address[0], address[1])
        connection.send(f"Welcome, {username}!".encode())

        while running:
            message = connection.recv(1024).decode()
            if not message:
                break
            logger.info("Message from %s: %s", username, message)

            if message.startswith("/all "):
                text = message[5:]
                for name, client in list(clients.items()):
                    if name != username:
                        client.send(f"{username}: {text}".encode())

            elif message.startswith("/to "):
                parts = message.split(" ", 2)
                if len(parts) < 3:
                    connection.send("ERROR: Usage: /to <username> <message>".encode())
                    continue
                target = parts[1]
                text = parts[2]
                if target not in clients:
                    connection.send(f"ERROR: User '{target}' not found.".encode())
                    logger.warning("Private message failed: %s -> %s", username, target)
                else:
                    clients[target].send(f"Private message from {username}: {text}".encode())
                    logger.info("Private message: %s -> %s", username, target)

            else:
                connection.send("ERROR: Use /all <message> or /to <username> <message>".encode())

    except ConnectionResetError:
        logger.warning("Connection lost: %s", username if username else address)
    except Exception as e:
        logger.error("Error handling %s: %s", username if username else address, e)

    finally:
        if username in clients and clients[username] == connection:
            del clients[username]
        connection.close()
        if username:
            logger.info("Client disconnected: %s", username)

def server_input():
    global running
    while running:
        command = input()
        if command.lower() == "quit":
            running = False
            logger.info("Shutting down server...")
            for client in list(clients.values()):
                try:
                    client.send("Server is shutting down.".encode())
                    client.close()
                except:
                    pass
            server.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    server.bind((HOST, PORT))
    server.listen()
except OSError as e:
    logger.error("Could not start server: %s", e)
    raise SystemExit(1)

logger.info("Server started on %s:%d", HOST, PORT)
logger.info("Waiting for clients...")
logger.info("Type 'quit' to stop the server.")

threading.Thread(target=server_input,daemon=True).start()
while running:
    try:
        connection, address = server.accept()
        threading.Thread(target = handle_client, args = (connection, address), daemon = True).start()
    except OSError:
        break
server.close()
logger.info("Server stopped.")