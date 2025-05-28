"""Šifrování a dešifrování klasickou substituční šifrou."""

# Importy
from __future__ import annotations
from .alphabet import ALPHABET

__all__ = ["encrypt", "decrypt"]


def _perm_to_map(key: str, *, decrypt: bool = False) -> dict[str, str]:
    """Vytvoří mapování znak -> znak na základě klíče (permutace).
    
    Vyvolá ValueError, pokud klíč není permutací 27 povolených znaků.
    """
    if len(key) != len(ALPHABET) or set(key) != set(ALPHABET):
        raise ValueError("Klíč musí být permutací 27-znakové abecedy.")
    return (
        {p: k for p, k in zip(ALPHABET, key)}  # Mapa pro šifrování
        if not decrypt
        else {k: p for p, k in zip(ALPHABET, key)}  # Mapa pro dešifrování
    )


def encrypt(plaintext: str, key: str) -> str:
    """Zašifruje text."""
    m = _perm_to_map(key, decrypt=False)
    return "".join(m.get(ch, ch) for ch in plaintext)


def decrypt(ciphertext: str, key: str) -> str:
    """Dešifruje text."""
    m = _perm_to_map(key, decrypt=True)
    return "".join(m.get(ch, ch) for ch in ciphertext)
