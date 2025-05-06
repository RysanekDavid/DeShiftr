"""Bigramová statistika a pravděpodobnostní funkce (likelihood)."""

from __future__ import annotations

import numpy as np

from .alphabet import ALPH_LEN, CHAR2IDX

__all__ = ["transition_matrix", "plausibility"]


def transition_matrix(text: str) -> np.ndarray:
    """Relativní bigramová matice (součet = 1).

    Pseudocount 1 se přičte *ještě před* normalizací, aby mizely nuly.
    """
    mat = np.ones((ALPH_LEN, ALPH_LEN), dtype=np.float64)  # pseudocount = 1
    idx = np.fromiter(
        (CHAR2IDX[ch] for ch in text if ch in CHAR2IDX), dtype=np.int8
    )
    if idx.size < 2:  # ochrana na příliš krátké texty
        return mat / mat.sum()

    # vektorová aktualizace bigramů
    np.add.at(mat, (idx[:-1], idx[1:]), 1)
    mat /= mat.sum()
    return mat


def plausibility(text: str, tm_ref: np.ndarray) -> float:
    """Log‑likelihood textu vzhledem k referenční matici."""
    tm_obs = transition_matrix(text)
    return float(np.sum(tm_obs * np.log(tm_ref)))
