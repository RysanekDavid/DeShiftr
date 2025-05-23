"""Bigram statistics and likelihood function."""

from __future__ import annotations

import numpy as np

from .alphabet import ALPH_LEN, CHAR2IDX

__all__ = ["transition_matrix", "plausibility"]


def transition_matrix(text: str) -> np.ndarray:
    """Relative bigram matrix (sum = 1).

    First, absolute bigram counts are calculated, then zero counts are replaced by a pseudocount of 1,
    and only then is the matrix normalized.
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

    # We could normalize each row separately so that the sum of each row is 1
    # (standard definition of a transition matrix).
    # If the sum of a row were 0 (which shouldn't happen after applying pseudocounts),
    # we would leave the row as is (full of pseudocounts), and the normalization below
    # would aim to create a uniform distribution for that row.
    # However, the standard approach here is to normalize the entire matrix so that its total sum is 1.
    # The project assignment specifies "Relative bigram matrix (sum = 1)" globally.
    
    total_sum = mat.sum()
    if total_sum == 0:
        if ALPH_LEN > 0:
            return np.full((ALPH_LEN, ALPH_LEN), 1.0 / (ALPH_LEN * ALPH_LEN), dtype=np.float64)
        else:
            return mat

    mat /= total_sum
    return mat


def plausibility(text: str, tm_ref: np.ndarray) -> float:
    """Log-likelihood of text given a reference matrix."""
    tm_obs = transition_matrix(text)
    return float(np.sum(tm_obs * np.log(tm_ref)))
