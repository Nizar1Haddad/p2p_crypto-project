from flask import Flask, request, jsonify, render_template
import socket
import threading
import sys
import os

# Allow importing from project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from crypto.validation import validate_input
from crypto.caesar import caesar_encrypt, caesar_decrypt
from crypto.affine import affine_encrypt, affine_decrypt
from crypto.vigenere import vigenere_encrypt, vigenere_decrypt
from crypto.transposition import transposition_encrypt, transposition_decrypt
from crypto.otp import otp_encrypt, otp_decrypt
from crypto.RSA_cipher import rsa_encrypt, rsa_decrypt

app = Flask(__name__)

PORT = 5005
received_messages = []


# =========================
# SOCKET RECEIVER (BACKGROUND)
# =========================
def start_receiver():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", PORT))
    server.listen(5)

    print("📥 Receiver running inside Flask app...")

    while True:
        conn, addr = server.accept()
        try:
            data = conn.recv(8192).decode()
            cipher, key, payload = data.split("|", 2)

            decrypted = ""

            if cipher == "caesar":
                decrypted = caesar_decrypt(payload, int(key))

            elif cipher == "affine":
                a, b = map(int, key.split(","))
                decrypted = affine_decrypt(payload, a, b)

            elif cipher == "vigenere":
                decrypted = vigenere_decrypt(payload, key)

            elif cipher == "transposition":
                decrypted = transposition_decrypt(payload, int(key))

            elif cipher == "otp":
                decrypted = otp_decrypt(payload, key)

            elif cipher == "rsa":
                d, n = map(int, key.split(","))
                cipher_list = list(map(int, payload.split(",")))
                decrypted = rsa_decrypt(cipher_list, d, n)

            else:
                decrypted = "Unknown cipher"

            decrypted = str(decrypted)

            print("Encrypted received:", payload)
            print("Decrypted message:", decrypted)
            print("-" * 40)

            received_messages.append({
                "from": addr[0],
                "encrypted": payload,
                "decrypted": decrypted
            })

        except Exception as e:
            print("Receiver error:", e)

        conn.close()


# =========================
# ROUTES
# =========================
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/send", methods=["POST"])
def send():
    data = request.get_json()
    cipher = data["cipher"]
    text = data["text"]
    key = data.get("key", "")
    ip = data["ip"]

    # ✅ VALIDATION MUST COME AFTER DATA EXTRACTION
    try:
        validate_input(cipher, key, text)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    if cipher == "caesar":
        encrypted = caesar_encrypt(text, int(key))

    elif cipher == "affine":
        a, b = map(int, key.split(","))
        encrypted = affine_encrypt(text, a, b)

    elif cipher == "vigenere":
        encrypted = vigenere_encrypt(text, key)

    elif cipher == "transposition":
        encrypted = transposition_encrypt(text, int(key))

    elif cipher == "otp":
        encrypted = otp_encrypt(text, key)

    elif cipher == "rsa":
        e, n = 17, 3233
        encrypted = ",".join(map(str, rsa_encrypt(text, e, n)))
        key = "2753,3233"

    else:
        return jsonify({"error": "Invalid cipher"}), 400

    message = f"{cipher}|{key}|{encrypted}"

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, PORT))
    sock.sendall(message.encode())
    sock.close()

    return jsonify({
        "status": "sent",
        "encrypted": encrypted
    })


@app.route("/inbox")
def inbox():
    return jsonify(received_messages)


# =========================
# START APP
# =========================
if __name__ == "__main__":
    threading.Thread(target=start_receiver, daemon=True).start()
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
