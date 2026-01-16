from math import gcd

def validate_input(cipher, key, text):
    if not text:
        raise ValueError("Message cannot be empty")

    if cipher == "caesar":
        if not key.isdigit():
            raise ValueError("Caesar key must be an integer")
        k = int(key)
        if k < 0 or k > 25:
            raise ValueError("Caesar key must be between 0 and 25")

    elif cipher == "affine":
        try:
            a, b = map(int, key.split(","))
        except:
            raise ValueError("Affine key must be in format a,b")

        if gcd(a, 26) != 1:
            raise ValueError("Affine key 'a' must be coprime with 26")

    elif cipher == "vigenere":
        if not key.isalpha():
            raise ValueError("Vigenere key must contain only letters")

    elif cipher == "transposition":
        if not key.isdigit() or int(key) <= 0:
            raise ValueError("Transposition key must be a positive integer")

    elif cipher == "otp":
        if len(key) != len(text):
            raise ValueError("OTP key must be the same length as the message")
        if not key.isalpha():
            raise ValueError("OTP key must contain only letters")

    elif cipher == "rsa":
        pass  # RSA keys are auto-generated

    else:
        raise ValueError("Unknown cipher")

    return True
