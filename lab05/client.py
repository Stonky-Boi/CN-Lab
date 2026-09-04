import argparse
import logging
import socket
import threading

parser = argparse.ArgumentParser(description = "CS-313 Assignment 5")
parser.add_argument("server_ip", help = "IP address of the server")
parser.add_argument("port", type = int, help = "server port number")
args = parser.parse_args()
if not 1 <= args.port <= 65535:
    parser.error("port must be between 1 and 65535")

HOST = args.server_ip
PORT = args.port

logging.basicConfig(level=logging.INFO, format = "%(asctime)s | %(levelname)s | %(message)s", datefmt = "%H:%M:%S")
logger = logging.getLogger("client")

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()
            if not message:
                logger.warning("Server disconnected.")
                break
            print("\n" + message)
        except OSError:
            break

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((HOST, PORT))
except ConnectionRefusedError:
    logger.error("Could not connect to server at %s:%d", HOST, PORT)
    raise SystemExit(1)
except OSError as e:
    logger.error("Connection failed: %s", e)
    raise SystemExit(1)
logger.info("Connected to server.")

username = input("Enter username: ").strip()
if not username:
    logger.error("Username cannot be empty.")
    client.close()
    raise SystemExit(1)
client.send(username.encode())

threading.Thread(target = receive_messages, daemon = True).start()
while True:
    try:
        message = input("> ")
        if message.lower() == "quit":
            logger.info("Disconnecting...")
            break
        client.send(message.encode())
    except (KeyboardInterrupt, EOFError):
        logger.info("Disconnecting...")
        break
    except OSError:
        logger.error("Connection to server lost.")
        break
client.close()