def rsa_encrypt(text, e, n):
    return [pow(ord(c), e, n) for c in text]


def rsa_decrypt(cipher_list, d, n):
    return ''.join(chr(pow(int(c), d, n)) for c in cipher_list)
