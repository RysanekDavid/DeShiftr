import random
import string

import pytest

from subcipher.alphabet import ALPHABET
from subcipher.codec import encrypt, decrypt


def random_plaintext(n=200):
    letters = ALPHABET + " .,!?;"
    return "".join(random.choice(letters) for _ in range(n))


@pytest.mark.parametrize("length", [10, 200, 500])
def test_roundtrip(length):
    plain = random_plaintext(length)
    key = "".join(random.sample(ALPHABET, len(ALPHABET)))
    assert decrypt(encrypt(plain, key), key) == plain
