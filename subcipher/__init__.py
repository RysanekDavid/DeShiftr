"""Substitution-cipher toolkit (encryption, decryption, cryptanalysis)."""

from importlib.metadata import version as _v

__all__ = [
    "ALPHABET",
    "CHAR2IDX",
    "IDX2CHAR",
    "encrypt",
    "decrypt",
    "transition_matrix",
    "plausibility",
    "crack",
    "export_result",
]

from .alphabet import ALPHABET, CHAR2IDX, IDX2CHAR
from .codec import encrypt, decrypt
from .stats import transition_matrix, plausibility
from .mh import crack
from .io import export_result

__version__: str = _v("subcipher") if __package__ else "0.0.0"
