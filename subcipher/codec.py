"""Šifrování a dešifrování klasickou substituční šifrou."""

from __future__ import annotations

from .alphabet import ALPHABET, CHAR2IDX, IDX2CHAR

__all__ = ["encrypt", "decrypt"]


def _perm_to_map(key: str, *, decrypt: bool = False) -> dict[str, str]:
    """Vytvoř mapování znak → znak podle zadaného klíče (permutace).

    Raises
    ------
    ValueError
        Pokud klíč není permutací 27 povolených znaků.
    """
    if len(key) != len(ALPHABET) or set(key) != set(ALPHABET):
        raise ValueError("Key must be a permutation of the 27‑char alphabet.")
    return (
        {p: k for p, k in zip(ALPHABET, key)}
        if not decrypt
        else {k: p for p, k in zip(ALPHABET, key)}
    )


def encrypt(plaintext: str, key: str) -> str:
    """Vrátí zašifrovaný text."""
    m = _perm_to_map(key, decrypt=False)
    return "".join(m.get(ch, ch) for ch in plaintext)


def decrypt(ciphertext: str, key: str) -> str:
    """Vrátí dešifrovaný text."""
    m = _perm_to_map(key, decrypt=True)
    return "".join(m.get(ch, ch) for ch in ciphertext)
