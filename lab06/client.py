import socket
import time
import random

HOST = "127.0.0.1"
PORT = 5001

client_no = int(input("Enter client number: "))
num_requests = int(input("Enter number of requests: "))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

for i in range(num_requests):
    if i > 0:
        delay = random.randint(1, 5)
        print("Waiting", delay, "seconds...")
        time.sleep(delay)

    print("Requesting file...")
    client.send("REQUEST".encode())
    data = client.recv(4096).decode()
    print("File received:")
    print(data)
    client.send("RETURNED".encode())
    print("Request", i + 1, "completed.\n")

client.send("DONE".encode())
client.close()
print("Client", client_no, "finished.")