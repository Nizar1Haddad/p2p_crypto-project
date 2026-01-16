from collections import Counter
from math import gcd
from functools import reduce
from itertools import product

from crypto.caesar import caesar_decrypt
from crypto.affine import affine_decrypt
from crypto.vigenere import vigenere_decrypt
from crypto.transposition import transposition_decrypt


# =========================
# LETTER FREQUENCY ANALYSIS
# =========================
def letter_frequency(text):
    text = [c.lower() for c in text if c.isalpha()]
    total = len(text)
    freq = Counter(text)
    return {k: v / total for k, v in freq.items()}


# =========================
# CAESAR FREQUENCY ATTACK
# =========================
def caesar_frequency_attack(ciphertext):
    frequencies = letter_frequency(ciphertext)
    if not frequencies:
        return None

    most_common_letter = max(frequencies, key=frequencies.get)
    assumed_e = ord(most_common_letter) - ord('e')
    key = assumed_e % 26

    return {
        "method": "frequency_analysis",
        "key": key,
        "plaintext": caesar_decrypt(ciphertext, key)
    }


# =========================
# CAESAR BRUTE FORCE
# =========================
def caesar_bruteforce(ciphertext):
    return [
        {"key": k, "plaintext": caesar_decrypt(ciphertext, k)}
        for k in range(26)
    ]


# =========================
# AFFINE BRUTE FORCE
# =========================
def affine_bruteforce(ciphertext):
    results = []
    for a in range(1, 26):
        if gcd(a, 26) != 1:
            continue
        for b in range(26):
            try:
                plaintext = affine_decrypt(ciphertext, a, b)
                results.append({
                    "key": f"{a},{b}",
                    "plaintext": plaintext
                })
            except:
                pass
    return results


# =========================
# KASISKI EXAMINATION
# =========================
def kasiski_examination(ciphertext, min_len=3):
    distances = []

    for size in range(min_len, min_len + 3):
        seen = {}
        for i in range(len(ciphertext) - size):
            seq = ciphertext[i:i+size]
            if seq in seen:
                distances.append(i - seen[seq])
            else:
                seen[seq] = i

    if not distances:
        return []

    return list(set(reduce(gcd, distances, distances[0:1])))


# =========================
# INDEX OF COINCIDENCE
# =========================
def index_of_coincidence(text):
    text = [c.lower() for c in text if c.isalpha()]
    N = len(text)
    if N <= 1:
        return 0.0

    freq = Counter(text)
    return sum(v * (v - 1) for v in freq.values()) / (N * (N - 1))


# =========================
# VIGENERE KEY LENGTH TEST
# =========================
def vigenere_key_length_test(ciphertext, max_len=10):
    results = {}
    for k in range(1, max_len + 1):
        columns = [''.join(ciphertext[i::k]) for i in range(k)]
        ic_avg = sum(index_of_coincidence(col) for col in columns) / k
        results[k] = ic_avg
    return results


# =========================
# VIGENERE BRUTE FORCE (SHORT KEYS)
# =========================
def vigenere_bruteforce(ciphertext, max_key_length=3):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    results = []

    for key_len in range(1, max_key_length + 1):
        for key_tuple in product(alphabet, repeat=key_len):
            key = "".join(key_tuple)
            plaintext = vigenere_decrypt(ciphertext, key)
            results.append({
                "key": key,
                "plaintext": plaintext
            })
    return results


# =========================
# TRANSPOSITION BRUTE FORCE
# =========================
def transposition_bruteforce(ciphertext, max_key=10):
    results = []
    for key in range(2, max_key + 1):
        try:
            plaintext = transposition_decrypt(ciphertext, key)
            results.append({
                "key": key,
                "plaintext": plaintext
            })
        except:
            pass
    return results
