import socket
import threading
from collections import deque

HOST = "127.0.0.1"
PORT = 5001

num_clients = int(input("Enter number of clients: "))
requests_per_client = int(input("Enter requests per client: "))

total_requests = num_clients * requests_per_client
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(num_clients)
print("\nServer started...")
print("Waiting for clients...\n")

queue = deque()
access_order = []
lock = threading.Lock()
served = 0

def handle_client(connection, address):
    global served

    while True:
        message = connection.recv(1024).decode()
        if not message:
            break

        if message == "REQUEST":
            with lock:
                queue.append((connection, address))
            while True:
                with lock:
                    if queue[0][0] == connection:
                        queue.popleft()
                        break
            with open("file.txt", "r") as file:
                data = file.read()
            connection.send(data.encode())

            response = connection.recv(1024).decode()
            if response == "RETURNED":
                with lock:
                    access_order.append(address)
                    served += 1
                    print("Request served:", served, "/", total_requests)
                    if served == total_requests:
                        print("\nFCFS Access Order:")
                        for i, client in enumerate(access_order, 1):
                            print(i, "->", client)

        elif message == "DONE":
            break

    connection.close()

threads = []

for i in range(num_clients):
    connection, address = server.accept()
    print("Client connected:", address)
    t = threading.Thread(target = handle_client, args = (connection, address))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
print("\nAll requests have been served.")
print("Server closed.")
server.close()