def vigenere_encrypt(text, key):
    if not key or not key.isalpha():
        raise ValueError("Key must be a non-empty string containing only letters")

    result = []
    key = key.lower()
    k = 0

    for c in text:
        if c.isalpha():
            shift = ord(key[k % len(key)]) - ord('a')
            base = ord('A') if c.isupper() else ord('a')
            result.append(chr((ord(c) - base + shift) % 26 + base))
            k += 1
        else:
            result.append(c)

    return "".join(result)


def vigenere_decrypt(text, key):
    if not key or not key.isalpha():
        raise ValueError("Key must be a non-empty string containing only letters")

    result = []
    key = key.lower()
    k = 0

    for c in text:
        if c.isalpha():
            shift = ord(key[k % len(key)]) - ord('a')
            base = ord('A') if c.isupper() else ord('a')
            result.append(chr((ord(c) - base - shift) % 26 + base))
            k += 1
        else:
            result.append(c)

    return "".join(result)
