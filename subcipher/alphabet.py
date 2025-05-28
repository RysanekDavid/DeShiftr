"""Definice abecedy a převodních tabulek znak ↔ index."""

# Importy
from __future__ import annotations

# Definice abecedy
ALPHABET: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_"
ALPH_LEN: int = len(ALPHABET)

# Převodní tabulky
CHAR2IDX: dict[str, int] = {ch: i for i, ch in enumerate(ALPHABET)}
IDX2CHAR: dict[int, str] = {i: ch for ch, i in CHAR2IDX.items()}
