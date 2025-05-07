"""Bigramová statistika a pravděpodobnostní funkce (likelihood)."""

from __future__ import annotations

import numpy as np

from .alphabet import ALPH_LEN, CHAR2IDX

__all__ = ["transition_matrix", "plausibility"]


def transition_matrix(text: str) -> np.ndarray:
    """Relativní bigramová matice (součet = 1).

    Nejprve se spočítají absolutní počty bigramů, pak se nulové počty nahradí pseudocountem 1,
    a až poté se matice normalizuje.
    """
    # 1. Absolutní matice četností bigramů
    mat = np.zeros((ALPH_LEN, ALPH_LEN), dtype=np.float64)
    idx = np.fromiter(
        (CHAR2IDX[ch] for ch in text if ch in CHAR2IDX), dtype=np.int8
    )

    if idx.size >= 2:
        # vektorová aktualizace bigramů
        np.add.at(mat, (idx[:-1], idx[1:]), 1)

    # 2. Nahrazení nul pseudocountem 1
    mat[mat == 0] = 1.0

    # 3. Normalizace
    # Pokud je součet matice nula (např. prázdný text nebo text bez platných bigramů
    # a všechny prvky byly původně 0, pak po pseudocountu budou všechny 1),
    # vrátíme rovnoměrné rozdělení.
    row_sums = mat.sum(axis=1, keepdims=True)
    # Abychom se vyhnuli dělení nulou, pokud by řádek měl součet 0 (po pseudocountu by to nemělo nastat,
    # pokud ALPH_LEN > 0, ale pro jistotu)
    # V případě, že text byl příliš krátký a matice zůstala nulová, po pseudocountu bude plná jedniček.
    if np.all(row_sums == 0): # Mělo by být mat.sum() == 0, ale kontrolujeme řádky pro normalizaci
        # Pokud je celá matice nulová (což by po pseudocountu nemělo být, pokud ALPH_LEN > 0),
        # vrátíme uniformní matici.
        # Po pseudocountu, pokud byl text krátký, bude matice plná jedniček.
        # Normalizace pak proběhne korektně.
        pass # Normalizace níže to pokryje

    # Normalizujeme každý řádek zvlášť, aby součet každého řádku byl 1
    # (standardní definice přechodové matice)
    # Pokud je součet řádku 0 (což by po pseudocountu nemělo nastat),
    # necháme řádek tak, jak je (plný pseudocountů), a normalizace níže
    # by měla vytvořit uniformní rozdělení pro ten řádek.
    # Nicméně, standardní je normalizovat celou matici tak, aby její celkový součet byl 1.
    # Zadání říká "Relativní bigramová matice (součet = 1)" globálně.

    total_sum = mat.sum()
    if total_sum == 0: # Může nastat jen pokud ALPH_LEN = 0, což je nepravděpodobné
        # Vytvoříme uniformní matici, pokud je to možné
        if ALPH_LEN > 0:
            return np.full((ALPH_LEN, ALPH_LEN), 1.0 / (ALPH_LEN * ALPH_LEN), dtype=np.float64)
        else:
            return mat # Prázdná matice

    mat /= total_sum
    return mat


def plausibility(text: str, tm_ref: np.ndarray) -> float:
    """Log‑likelihood textu vzhledem k referenční matici."""
    tm_obs = transition_matrix(text)
    return float(np.sum(tm_obs * np.log(tm_ref)))
