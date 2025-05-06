"""Utility functions for text processing, including cleaning."""

from __future__ import annotations
from .alphabet import ALPHABET, CHAR2IDX

def clean_text(raw_text: str) -> str:
    """
    Cleans the input text to conform to the project's alphabet.
    - Converts text to uppercase.
    - Replaces characters not in ALPHABET with '_'.
    - Keeps characters already in ALPHABET.
    """
    cleaned_chars = []
    for char in raw_text.upper():
        if char in CHAR2IDX:
            cleaned_chars.append(char)
        else:
            cleaned_chars.append("_")  # Replace unknown chars with underscore
    return "".join(cleaned_chars)
