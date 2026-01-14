def otp_encrypt(text, key):
    if not key or not key.isalpha():
        raise ValueError("Key must contain only letters")

    letters_needed = sum(c.isalpha() for c in text)
    if len(key) < letters_needed:
        raise ValueError("Key must be at least as long as the number of letters in the text")

    result = []
    key = key.lower()
    i = 0

    for c in text:
        if c.isalpha():
            shift = ord(key[i]) - ord('a')
            base = ord('A') if c.isupper() else ord('a')
            result.append(chr((ord(c) - base + shift) % 26 + base))
            i += 1
        else:
            result.append(c)

    return "".join(result)


def otp_decrypt(text, key):
    if not key or not key.isalpha():
        raise ValueError("Key must contain only letters")

    letters_needed = sum(c.isalpha() for c in text)
    if len(key) < letters_needed:
        raise ValueError("Key must be at least as long as the number of letters in the text")

    result = []
    key = key.lower()
    i = 0

    for c in text:
        if c.isalpha():
            shift = ord(key[i]) - ord('a')
            base = ord('A') if c.isupper() else ord('a')
            result.append(chr((ord(c) - base - shift) % 26 + base))
            i += 1
        else:
            result.append(c)

    return "".join(result)
