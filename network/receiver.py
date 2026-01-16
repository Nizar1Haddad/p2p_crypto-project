import socket
import sys
import os

# Allow importing crypto modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crypto.caesar import caesar_decrypt
from crypto.affine import affine_decrypt
from crypto.vigenere import vigenere_decrypt
from crypto.transposition import transposition_decrypt
from crypto.otp import otp_decrypt
from crypto.RSA_cipher import rsa_decrypt

HOST = "0.0.0.0"
PORT = 5005

# Inbox to store received messages
inbox = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

print("📥 Receiver running on port", PORT)
print("Waiting for incoming encrypted messages...\n")

while True:
    conn, addr = server.accept()
    print("Connection from", addr)

    try:
        data = conn.recv(8192).decode()
        cipher, key, payload = data.split("|", 2)

        plaintext = ""

        if cipher == "caesar":
            plaintext = caesar_decrypt(payload, int(key))

        elif cipher == "affine":
            a, b = map(int, key.split(","))
            plaintext = affine_decrypt(payload, a, b)

        elif cipher == "vigenere":
            plaintext = vigenere_decrypt(payload, key)

        elif cipher == "transposition":
            plaintext = transposition_decrypt(payload, int(key))

        elif cipher == "otp":
            plaintext = otp_decrypt(payload, key)

        elif cipher == "rsa":
            d, n = map(int, key.split(","))
            cipher_list = list(map(int, payload.split(",")))
            plaintext = rsa_decrypt(cipher_list, d, n)

        else:
            plaintext = "Unknown cipher"

        # ✅ FORCE plaintext to always be a string
        plaintext = str(plaintext)

        # Debug output (VERY IMPORTANT)
        print("Encrypted received:", payload)
        print("Decrypted message:", plaintext)
        print("-" * 40)

        # Store message in inbox
        inbox.append({
            "from": addr[0],
            "encrypted": payload,
            "decrypted": plaintext
        })

    except Exception as e:
        print("Error handling message:", e)

    conn.close()
