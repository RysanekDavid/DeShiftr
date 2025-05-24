"""Bigram statistics and likelihood function."""

from __future__ import annotations

import numpy as np

from .alphabet import ALPH_LEN, CHAR2IDX # Assuming ALPHABET is also available or not needed directly here

__all__ = ["transition_matrix", "plausibility"]


# --- Existing transition_matrix function remains unchanged ---
# Used for creating TM_ref, which is P_ref (globally normalized)
def transition_matrix(text: str) -> np.ndarray:
    """Relative bigram matrix (sum of all elements = 1).

    First, absolute bigram counts are calculated, then zero counts are replaced by a pseudocount of 1,
    and only then is the matrix normalized.
    Used for creating TM_ref.
    """
    mat = np.zeros((ALPH_LEN, ALPH_LEN), dtype=np.float64)
    idx = np.fromiter(
        (CHAR2IDX[ch] for ch in text if ch in CHAR2IDX), dtype=np.int8
    )

    if idx.size >= 2:
        np.add.at(mat, (idx[:-1], idx[1:]), 1)

    mat[mat == 0] = 1.0 # Laplace smoothing

    total_sum = mat.sum()
    if total_sum == 0:
        if ALPH_LEN > 0:
            return np.full((ALPH_LEN, ALPH_LEN), 1.0 / (ALPH_LEN * ALPH_LEN), dtype=np.float64)
        else:
            return mat # Should be an empty matrix if ALPH_LEN is 0

    mat /= total_sum # Global normalization
    return mat

# --- New helper function for obtaining smoothed counts ---
def _get_smoothed_bigram_counts(text: str) -> np.ndarray:
    """
    Calculates absolute bigram counts from text, with zeros replaced by a pseudocount of 1.
    This corresponds to the PDF's pseudocode for transition_matrix when used for TM_obs.
    """
    mat = np.zeros((ALPH_LEN, ALPH_LEN), dtype=np.float64)
    idx = np.fromiter(
        (CHAR2IDX[ch] for ch in text if ch in CHAR2IDX), dtype=np.int8
    )

    if idx.size >= 2:
        np.add.at(mat, (idx[:-1], idx[1:]), 1)

    mat[mat == 0] = 1.0 # Laplace smoothing
    return mat

# --- Modified plausibility function ---
def plausibility(text: str, tm_ref: np.ndarray) -> float:
    """
    Log-likelihood of text given a reference probability matrix (tm_ref).
    tm_ref is expected to be a globally normalized probability matrix (sum of elements = 1).
    The observed matrix from 'text' will be smoothed counts.
    """
    # Get smoothed absolute counts for the observed text, as per PDF pseudocode for TM_obs
    tm_obs_counts_smoothed = _get_smoothed_bigram_counts(text)

    # tm_ref should already have non-zero probabilities due to smoothing before its normalization.
    # Taking log directly. Values should be < 0.
    # Add a small epsilon to tm_ref before log to prevent log(0) if any tm_ref element is exactly zero,
    # which ideally shouldn't happen if tm_ref was also smoothed before normalization.
    epsilon = np.finfo(np.float64).eps # Smallest representable positive number
    log_tm_ref = np.log(tm_ref + epsilon)


    # The original feedback included a more complex handling for -inf in log_tm_ref.
    # Adding epsilon should prevent exact zeros in tm_ref from causing -inf.
    # If tm_ref can still have zeros due to its generation process (e.g., if it wasn't smoothed),
    # then the more robust -inf handling might be needed.
    # For now, relying on tm_ref being well-behaved (smoothed before normalization).

    # Calculate sum of C_obs * log(P_ref)
    likelihood = np.sum(tm_obs_counts_smoothed * log_tm_ref)
    
    return float(likelihood)
