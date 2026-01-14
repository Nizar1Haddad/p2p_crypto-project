from math import gcd

def affine_encrypt(text, a, b):
    if gcd(a, 26) != 1:
        raise ValueError("Invalid affine key (a must be coprime with 26)")

    result = ""
    for c in text:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            result += chr((a * (ord(c) - base) + b) % 26 + base)
        else:
            result += c
    return result


def affine_decrypt(text, a, b):
    for i in range(26):
        if (a * i) % 26 == 1:
            inv = i
            break
    else:
        raise ValueError("No modular inverse for a")

    result = ""
    for c in text:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            result += chr((inv * ((ord(c) - base) - b)) % 26 + base)
        else:
            result += c
    return result
