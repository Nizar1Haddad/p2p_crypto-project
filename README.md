# P2P Crypto Messenger

This project is a peer-to-peer encrypted messaging application developed for a cryptography and networking capstone project. The system allows two devices connected to the same local network to exchange messages securely using a variety of classical and modern cryptographic algorithms.

The project demonstrates encryption and decryption, centralized input validation, cryptanalysis of classical ciphers, and secure communication through a web-based interface.


## Project Objectives

The main objectives of this project are:

- To implement multiple cryptographic algorithms correctly
- To apply encryption and decryption in a real communication scenario
- To design a centralized validation framework for cryptographic inputs
- To demonstrate cryptanalysis techniques for classical ciphers
- To build a secure web-based messaging system
- To understand peer-to-peer communication using TCP sockets


## Implemented Cryptographic Algorithms

The following cryptographic algorithms are implemented:

- Caesar Cipher
- Affine Cipher
- Vigenère Cipher
- Transposition Cipher
- One-Time Pad (OTP)
- RSA (public-key cryptography)

Each cipher supports both encryption and decryption. OTP and RSA are implemented according to their theoretical constraints.


## Project Structure

p2p_crypto/
│
├── crypto/
│ ├── caesar.py
│ ├── affine.py
│ ├── vigenere.py
│ ├── transposition.py
│ ├── otp.py
│ ├── RSA_cipher.py
│ ├── validation.py
│ └── cryptanalysis.py
│
├── network/
│ └── receiver.py
│
├── web/
│ ├── app.py
│ └── templates/
│ └── index.html
│
└── README.md



## System Architecture

The system consists of three main components:

### Frontend
The frontend is a web-based interface built using HTML, CSS, and JavaScript. It allows users to:
- Enter messages
- Select an encryption algorithm
- Provide the required key
- Specify the receiver’s IP address
- View encrypted and decrypted messages in a chat-style interface

No cryptographic operations are performed on the frontend.

### Backend
The backend is implemented using Flask. It is responsible for:
- Validating user input
- Encrypting outgoing messages
- Sending encrypted messages via TCP sockets
- Running a background receiver thread
- Exposing received messages through HTTP endpoints

All cryptographic operations are performed server-side.

### Receiver
The receiver is a TCP socket server that:
- Listens for incoming encrypted messages
- Parses the message format
- Decrypts messages using the appropriate cipher
- Stores encrypted and decrypted messages for display


## Message Flow

1. The user enters a message, selects a cipher, and provides a key.
2. The backend validates the input using a centralized validation framework.
3. The message is encrypted server-side.
4. The encrypted message is sent to the peer device using a TCP socket.
5. The receiver decrypts the message.
6. Both encrypted and decrypted messages are stored.
7. The frontend periodically fetches new messages and updates the interface.


## Input Validation

A centralized validation framework is implemented in `validation.py`.  
It enforces cipher-specific constraints, including:

- Caesar key range (0–25)
- Affine key format and coprime condition
- Vigenère key alphabetic constraint
- Transposition key positivity
- OTP key length and alphabetic constraint
- RSA key handling on the server side

Validation is performed before encryption to prevent invalid cryptographic operations.


## Cryptanalysis

Cryptanalysis techniques are implemented for classical ciphers in `cryptanalysis.py` to demonstrate their weaknesses and analyze encrypted messages without prior knowledge of the key.

### Caesar Cipher
The Caesar cipher is analyzed using:
- Brute-force cryptanalysis by testing all possible shifts
- Letter frequency analysis by exploiting known English letter distributions

### Affine Cipher
The Affine cipher is analyzed using brute-force cryptanalysis over all valid key pairs. Frequency analysis concepts are used to evaluate the plausibility of decrypted outputs.

### Vigenère Cipher
Multiple classical cryptanalysis techniques are applied:
- Kasiski examination to estimate key length using repeated patterns
- Index of Coincidence to identify likely key lengths based on statistical properties
- Column-wise frequency analysis, treating each column as a Caesar cipher
- Brute-force attacks for short key lengths

### Transposition Cipher
The Transposition cipher is analyzed using:
- Structural analysis
- Testing different key lengths
- Recognition of readable English text and common digraphs

### One-Time Pad (OTP)
The One-Time Pad is excluded from cryptanalysis because it provides perfect secrecy when used correctly. Statistical attacks are not feasible.

### RSA
RSA cryptanalysis is not attempted, as breaking RSA requires factoring large integers, which is computationally infeasible for secure key sizes. RSA is included for educational purposes only.


## How to Run the Project

# Requirements
- Python 3.9 or higher
- Flask

Install Flask if needed:

'''
pip install flask
Running the Application
Both devices must be connected to the same local network.

On each device, run:

python web/app.py

Then open a browser and navigate to:

http://<device-ip>:5000

To send a message, enter the IP address of the other device, choose a cipher, enter the message and key, and send.

Example Test
Cipher: Caesar
Message: hello
Key: 3

Encrypted output:
khoor

Decrypted output:
hello


### Security Considerations
This project is intended for educational purposes. Classical ciphers are not secure for real-world applications. The One-Time Pad is secure only if the key is truly random, used once, and kept secret. The RSA implementation is simplified and intended for demonstration and learning.


### Conclusion
This project demonstrates the practical application of cryptography and networking concepts in a peer-to-peer communication system. It integrates encryption, decryption, cryptanalysis, input validation, and a secure web-based interface, fulfilling all the requirements of the capstone project