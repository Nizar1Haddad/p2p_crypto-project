from flask import Flask, request, jsonify, render_template
import socket
import sys
import os

# Allow importing from project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crypto.caesar import caesar_encrypt
from crypto.affine import affine_encrypt
from crypto.vigenere import vigenere_encrypt
from crypto.transposition import transposition_encrypt
from crypto.otp import otp_encrypt
from crypto.RSA_cipher import rsa_encrypt

app = Flask(__name__)

# 🔴 CHANGE THIS to the receiver laptop IP when using two laptops
RECEIVER_IP = "127.0.0.1"
PORT = 5005


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/send", methods=["POST"])
def send():
    try:
        data = request.get_json()
        cipher = data["cipher"]
        text = data["text"]
        key = data["key"]

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
            e, n = map(int, key.split(","))
            encrypted = ",".join(map(str, rsa_encrypt(text, e, n)))

        else:
            return jsonify({"error": "Invalid cipher type"}), 400

        # Protocol: cipher|key|payload
        msg = f"{cipher}|{key}|{encrypted}"

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((RECEIVER_IP, PORT))
        sock.sendall(msg.encode())
        sock.close()

        return jsonify({
            "status": "sent",
            "encrypted": encrypted
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
