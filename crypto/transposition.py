import math

def transposition_encrypt(text, key):
    if key <= 0:
        raise ValueError("Key must be a positive integer")

    result = []
    for col in range(key):
        i = col
        while i < len(text):
            result.append(text[i])
            i += key
    return "".join(result)


def transposition_decrypt(ciphertext, key):
    if key <= 0:
        raise ValueError("Key must be a positive integer")

    num_cols = math.ceil(len(ciphertext) / key)
    num_rows = key
    num_shaded = num_cols * num_rows - len(ciphertext)

    plaintext = [""] * num_cols
    col = 0
    row = 0

    for c in ciphertext:
        plaintext[col] += c
        col += 1

        if col == num_cols or (col == num_cols - 1 and row >= num_rows - num_shaded):
            col = 0
            row += 1

    return "".join(plaintext)
