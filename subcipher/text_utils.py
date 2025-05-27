"""Utility functions for text processing, including cleaning."""

from __future__ import annotations
from .alphabet import ALPHABET, CHAR2IDX # ALPHABET zde není striktně nutný, ale nevadí
import re # Přidán import pro regulární výrazy

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
    transliterated_text = []
    for char in text:
        transliterated_text.append(CZECH_TRANSLITERATION_MAP.get(char, char))
    return "".join(transliterated_text)

def clean_text(raw_text: str) -> str:
    """
    Cleans the input text to conform to the project's alphabet.
    - Transliterates common Czech diacritics.
    - Replaces whitespace sequences (space, tab, newline etc.) with a single underscore.
    - Converts text to uppercase.
    - Keeps only characters present in CHAR2IDX (A-Z, _), discards others.
    """
    transliterated = _transliterate_czech(raw_text)
    
    # Nahraď všechny sekvence jednoho či více bílých znaků (mezery, tabulátory, nové řádky atd.)
    # jedním podtržítkem.
    text_with_underscores = re.sub(r'\s+', '_', transliterated)
    
    cleaned_chars = []
    for char in text_with_underscores.upper(): # Nyní pracujeme s textem, kde mezery jsou již '_'
        if char in CHAR2IDX: # CHAR2IDX obsahuje A-Z a _
            cleaned_chars.append(char)
            
    final_text = "".join(cleaned_chars)
    
    # Volitelné: Pokud by re.sub z nějakého důvodu nechal vícenásobná podtržítka
    # a ty bys chtěl jen jedno, můžeš přidat tento krok.
    # Pro r'\s+' by to ale nemělo být nutné.
    # while "__" in final_text:
    #     final_text = final_text.replace("__", "_")
            
    # --- Přidáno pro debugování ---
    # print(f"DEBUG clean_text: Sample of cleaned_chars (first 500): {final_text[:500]}")
    # print(f"DEBUG clean_text: Count of '_' in cleaned_chars: {final_text.count('_')}")
    # --- Konec debugování ---
            
    return final_text