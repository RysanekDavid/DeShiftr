import numpy as np

from subcipher.alphabet import ALPHABET
from subcipher.codec import encrypt, decrypt
from subcipher.stats import transition_matrix
from subcipher.mh import crack


def test_crack_short_text():
    rng = np.random.default_rng(0)
    key_true = "".join(rng.permutation(list(ALPHABET)))
    plaintext = "".join(rng.choice(list(ALPHABET), 2000))
    cipher = encrypt(plaintext, key_true)

    tm_ref = transition_matrix(plaintext)  # pro unit‑test si pomůžeme
    key_found, plain_found, _ = crack(cipher, tm_ref, iters=5000, seed=1)

    # alespoň 90 % znaků správně
    matches = sum(p == q for p, q in zip(plaintext, plain_found))
    assert matches / len(plaintext) > 0.9, "MH selhal na krátkém textu"
    assert decrypt(cipher, key_found) == plain_found
