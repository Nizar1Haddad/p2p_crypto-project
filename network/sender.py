import socket
from crypto.caesar import encrypt

HOST = "192.168.0.2"  # CHANGE to receiver IP
PORT = 5005

cipher = "caesar"
key = 3
text = "HELLO WORLD"

ciphertext = encrypt(text, key)
message = f"{cipher}|{key}|{ciphertext}"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
client.sendall(message.encode())
client.close()

print("Sent:", ciphertext)
