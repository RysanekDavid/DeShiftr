"""Pomocné funkce pro zpracování a čištění textu."""

# Importy
from __future__ import annotations
from .alphabet import CHAR2IDX # ALPHABET zde není striktně nutný
import re

__all__ = ["clean_text"]

# Manuální transliterační mapa pro české znaky
CZECH_TRANSLITERATION_MAP = {
    'Á': 'A', 'Č': 'C', 'Ď': 'D', 'É': 'E', 'Ě': 'E',
    'Í': 'I', 'Ň': 'N', 'Ó': 'O', 'Ř': 'R', 'Š': 'S',
    'Ť': 'T', 'Ú': 'U', 'Ů': 'U', 'Ý': 'Y', 'Ž': 'Z',
    'á': 'a', 'č': 'c', 'ď': 'd', 'é': 'e', 'ě': 'e',
    'í': 'i', 'ň': 'n', 'ó': 'o', 'ř': 'r', 'š': 's',
    'ť': 't', 'ú': 'u', 'ů': 'u', 'ý': 'y', 'ž': 'z',
}

def _transliterate_czech(text: str) -> str:
    """Převede běžnou českou diakritiku na ekvivalenty bez diakritiky."""
    transliterated_text = []
    for char in text:
        transliterated_text.append(CZECH_TRANSLITERATION_MAP.get(char, char))
    return "".join(transliterated_text)

def clean_text(raw_text: str) -> str:
    """Vyčistí vstupní text tak, aby odpovídal abecedě projektu.
    
    Kroky čištění:
    - Transliteruje českou diakritiku.
    - Nahradí sekvence bílých znaků jedním podtržítkem.
    - Převede text na velká písmena.
    - Ponechá pouze znaky přítomné v CHAR2IDX (A-Z, _), ostatní zahodí.
    """
    transliterated = _transliterate_czech(raw_text)
    
    # Nahradí všechny sekvence jednoho či více bílých znaků jedním podtržítkem.
    text_with_underscores = re.sub(r'\s+', '_', transliterated)
    
    cleaned_chars = []
    # Převede na velká písmena a filtruje znaky
    for char in text_with_underscores.upper():
        if char in CHAR2IDX: # CHAR2IDX obsahuje A-Z a _
            cleaned_chars.append(char)
            
    final_text = "".join(cleaned_chars)
            
    return final_text