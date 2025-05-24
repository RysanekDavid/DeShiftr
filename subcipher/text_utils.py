"""Utility functions for text processing, including cleaning."""

from __future__ import annotations
from .alphabet import ALPHABET, CHAR2IDX # ALPHABET is not strictly needed here but good for context

__all__ = ["clean_text"]

# Manual transliteration map for Czech characters
CZECH_TRANSLITERATION_MAP = {
    'Á': 'A', 'Č': 'C', 'Ď': 'D', 'É': 'E', 'Ě': 'E',
    'Í': 'I', 'Ň': 'N', 'Ó': 'O', 'Ř': 'R', 'Š': 'S',
    'Ť': 'T', 'Ú': 'U', 'Ů': 'U', 'Ý': 'Y', 'Ž': 'Z',
    'á': 'a', 'č': 'c', 'ď': 'd', 'é': 'e', 'ě': 'e',
    'í': 'i', 'ň': 'n', 'ó': 'o', 'ř': 'r', 'š': 's',
    'ť': 't', 'ú': 'u', 'ů': 'u', 'ý': 'y', 'ž': 'z',
}

def _transliterate_czech(text: str) -> str:
    """Converts common Czech diacritics to their non-diacritic ASCII equivalents."""
    # This is a simplified transliteration. For more comprehensive handling,
    # a library like unidecode would be better, but this covers common cases.
    transliterated_text = []
    for char in text:
        transliterated_text.append(CZECH_TRANSLITERATION_MAP.get(char, char))
    return "".join(transliterated_text)

def clean_text(raw_text: str) -> str:
    """
    Cleans the input text to conform to the project's alphabet.
    - Transliterates common Czech diacritics.
    - Converts text to uppercase.
    - Discards characters not in ALPHABET (A-Z, _).
    - Keeps characters already in ALPHABET.
    """
    transliterated = _transliterate_czech(raw_text)
    cleaned_chars = []
    # Convert to uppercase AFTER transliteration to handle lowercase diacritics correctly
    for char in transliterated.upper(): 
        if char in CHAR2IDX: # CHAR2IDX contains uppercase A-Z and _
            cleaned_chars.append(char)
    return "".join(cleaned_chars)
