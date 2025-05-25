"""Bigram statistics and likelihood function."""

from __future__ import annotations

import numpy as np

# Ujisti se, že importuješ i ALPHABET, pokud ho budeš používat v debugovacích printech
from .alphabet import ALPH_LEN, CHAR2IDX, ALPHABET # Přidán ALPHABET

__all__ = ["transition_matrix", "plausibility"]


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
    
    # --- ZAČÁTEK PŘIDANÝCH DEBUGOVACÍCH VÝPISŮ ---
    print(f"DEBUG transition_matrix: Max count in matrix AFTER raw counting: {np.max(mat)}")
    print(f"DEBUG transition_matrix: Sum of raw counts (should be len(text)-1): {np.sum(mat)}")

    print("\nDEBUG transition_matrix: Raw counts for some expected frequent bigrams (before smoothing):")
    frequent_bigrams_to_check = ["E_", "A_", "_S", "ST", "PO", "N_", "NI", "OV"] # Přidej/změň dle potřeby
    for bigram_str in frequent_bigrams_to_check:
        if len(bigram_str) == 2 and bigram_str[0] in CHAR2IDX and bigram_str[1] in CHAR2IDX:
            try:
                count = mat[CHAR2IDX[bigram_str[0]], CHAR2IDX[bigram_str[1]]]
                print(f"  Count for '{bigram_str}': {count}")
            except KeyError: # Nemělo by nastat, pokud jsou znaky v ALPHABET
                print(f"  Error accessing bigram '{bigram_str}'")
        else:
            print(f"  Skipping invalid bigram string for debug: '{bigram_str}'")
    # --- KONEC PŘIDANÝCH DEBUGOVACÍCH VÝPISŮ ---

    mat[mat == 0] = 1.0 # Laplace smoothing
    # print(f"DEBUG transition_matrix: Max value in matrix AFTER pseudocounts: {np.max(mat)}") # Tento můžeš nechat
    # print(f"DEBUG transition_matrix: Sum of matrix AFTER pseudocounts: {np.sum(mat)}") # Tento můžeš nechat

    total_sum = mat.sum()
    # print(f"DEBUG transition_matrix: Total sum used for normalization: {total_sum}") # Tento můžeš nechat

    if total_sum == 0:
        if ALPH_LEN > 0:
            # print("DEBUG transition_matrix: total_sum is 0, returning uniform matrix.") # Tento můžeš nechat
            return np.full((ALPH_LEN, ALPH_LEN), 1.0 / (ALPH_LEN * ALPH_LEN), dtype=np.float64)
        else:
            # print("DEBUG transition_matrix: total_sum is 0 and ALPH_LEN is 0, returning empty mat.") # Tento můžeš nechat
            return mat 

    mat /= total_sum # Global normalization
    # print(f"DEBUG transition_matrix: Max probability in matrix AFTER normalization: {np.max(mat)}") # Tento můžeš nechat
    # print(f"DEBUG transition_matrix: Sum of matrix AFTER normalization: {np.sum(mat)}") # Tento můžeš nechat
    return mat

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

def plausibility(text: str, tm_ref: np.ndarray) -> float:
    """
    Log-likelihood of text given a reference probability matrix (tm_ref).
    tm_ref is expected to be a globally normalized probability matrix (sum of elements = 1).
    The observed matrix from 'text' will be smoothed counts.
    """
    tm_obs_counts_smoothed = _get_smoothed_bigram_counts(text)

    epsilon = np.finfo(np.float64).eps 
    log_tm_ref = np.log(tm_ref + epsilon)

    likelihood = np.sum(tm_obs_counts_smoothed * log_tm_ref)
    
    return float(likelihood)