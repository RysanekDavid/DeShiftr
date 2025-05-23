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
    mat = np.zeros((ALPH_LEN, ALPH_LEN), dtype=np.float64)
    idx = np.fromiter(
        (CHAR2IDX[ch] for ch in text if ch in CHAR2IDX), dtype=np.int8
    )

    if idx.size >= 2:
        np.add.at(mat, (idx[:-1], idx[1:]), 1)

    mat[mat == 0] = 1.0

    row_sums = mat.sum(axis=1, keepdims=True)
    if np.all(row_sums == 0):
        pass

    # Normalizujeme každý řádek zvlášť, aby součet každého řádku byl 1
    # Pokud je součet řádku 0 (což by po pseudocountu nemělo nastat),
    # necháme řádek tak, jak je (plný pseudocountů), a normalizace níže
    # by měla vytvořit uniformní rozdělení pro ten řádek.
    
    total_sum = mat.sum()
    if total_sum == 0:
        if ALPH_LEN > 0:
            return np.full((ALPH_LEN, ALPH_LEN), 1.0 / (ALPH_LEN * ALPH_LEN), dtype=np.float64)
        else:
            return mat

    mat /= total_sum
    return mat


def plausibility(text: str, tm_ref: np.ndarray) -> float:
    """Log‑likelihood textu vzhledem k referenční matici."""
    tm_obs = transition_matrix(text)
    return float(np.sum(tm_obs * np.log(tm_ref)))
