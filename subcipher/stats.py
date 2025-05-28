"""Statistiky bigramů a funkce věrohodnosti."""

# Importy
from __future__ import annotations
import numpy as np
from .alphabet import ALPH_LEN, CHAR2IDX

__all__ = ["transition_matrix", "plausibility"]


def transition_matrix(text: str) -> np.ndarray:
    """Vytvoří matici přechodů bigramů (relativní četnosti).
    
    Nejprve se spočítají absolutní počty bigramů, poté se nulové počty nahradí pseudopočtem 1 (Laplace smoothing)
    a nakonec se matice normalizuje tak, aby součet všech prvků byl 1.
    Používá se pro vytvoření referenční matice (TM_ref).
    """
    mat = np.zeros((ALPH_LEN, ALPH_LEN), dtype=np.float64)
    # Převede text na pole indexů znaků
    idx = np.fromiter(
        (CHAR2IDX[ch] for ch in text if ch in CHAR2IDX), dtype=np.int8
    )

    if idx.size >= 2: # Započítá bigramy
        np.add.at(mat, (idx[:-1], idx[1:]), 1)
    
    mat[mat == 0] = 1.0 # Laplace smoothing (pseudopočet 1 pro nulové výskyty)

    total_sum = mat.sum()

    if total_sum == 0: # Ošetření pro prázdný nebo velmi krátký text
        if ALPH_LEN > 0:
            # Vrátí uniformní distribuci, pokud je abeceda definována
            return np.full((ALPH_LEN, ALPH_LEN), 1.0 / (ALPH_LEN * ALPH_LEN), dtype=np.float64)
        else:
            # Vrátí prázdnou matici, pokud není definována abeceda (nemělo by nastat)
            return mat

    mat /= total_sum # Normalizace matice (globální)
    return mat

def _get_smoothed_bigram_counts(text: str) -> np.ndarray:
    """Spočítá absolutní počty bigramů z textu s Laplaceovým vyhlazováním.
    
    Nulové počty jsou nahrazeny pseudopočtem 1.
    Používá se pro výpočet pozorované matice (TM_obs) ve funkci plausibility.
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
    """Vypočítá log-věrohodnost textu vzhledem k referenční matici pravděpodobností (tm_ref).
    
    tm_ref by měla být globálně normalizovaná matice pravděpodobností (součet prvků = 1).
    Pozorovaná matice z 'text' bude mít vyhlazené počty.
    """
    # Získání matice pozorovaných bigramů s vyhlazením
    tm_obs_counts_smoothed = _get_smoothed_bigram_counts(text)

    # Přidání malé epsilon konstanty pro numerickou stabilitu při logaritmování
    epsilon = np.finfo(np.float64).eps
    log_tm_ref = np.log(tm_ref + epsilon)

    # Výpočet log-věrohodnosti jako součin pozorovaných počtů a logaritmu referenčních pravděpodobností
    likelihood = np.sum(tm_obs_counts_smoothed * log_tm_ref)
    
    return float(likelihood)