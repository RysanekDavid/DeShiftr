"""Encryption and decryption using a classical substitution cipher."""

from __future__ import annotations

from .alphabet import ALPHABET

__all__ = ["encrypt", "decrypt"]


def _perm_to_map(key: str, *, decrypt: bool = False) -> dict[str, str]:
    """Create char → char mapping based on the provided key (permutation).

    Raises
    ------
    ValueError
        If the key is not a permutation of the 27 allowed characters.
    """
    if len(key) != len(ALPHABET) or set(key) != set(ALPHABET):
        raise ValueError("Key must be a permutation of the 27‑char alphabet.")
    return (
        {p: k for p, k in zip(ALPHABET, key)}
        if not decrypt
        else {k: p for p, k in zip(ALPHABET, key)}
    )


def encrypt(plaintext: str, key: str) -> str:
    """Returns the encrypted text."""
    m = _perm_to_map(key, decrypt=False)
    return "".join(m.get(ch, ch) for ch in plaintext)


def decrypt(ciphertext: str, key: str) -> str:
    """Returns the decrypted text."""
    m = _perm_to_map(key, decrypt=True)
    return "".join(m.get(ch, ch) for ch in ciphertext)
