def caesar_encrypt(text, key):
    result = ""
    for c in text:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            result += chr((ord(c) - base + key) % 26 + base)
        else:
            result += c
    return result

def caesar_decrypt(text, key):
    return caesar_encrypt(text, -key)
