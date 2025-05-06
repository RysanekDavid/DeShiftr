"""Modul s definicí abecedy a rychlými převody znak ↔ index."""

from __future__ import annotations

ALPHABET: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_"
ALPH_LEN: int = len(ALPHABET)

CHAR2IDX: dict[str, int] = {ch: i for i, ch in enumerate(ALPHABET)}
IDX2CHAR: dict[int, str] = {i: ch for ch, i in CHAR2IDX.items()}
