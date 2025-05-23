"""Metropolis-Hastings cracking of substitution cipher."""

from __future__ import annotations

import logging
from collections.abc import Generator
from typing import Tuple

import numpy as np

from .alphabet import ALPHABET, ALPH_LEN
from .codec import decrypt
from .stats import plausibility

__all__ = ["crack"]

log = logging.getLogger(__name__)


def _random_keys(rng: np.random.Generator) -> Generator[str, None, None]:
    """Infinite generator of random alphabet permutations."""
    while True:
        yield "".join(rng.permutation(list(ALPHABET)))


def crack(
    cipher: str,
    tm_ref: np.ndarray,
    *,
    iters: int = 20_000,
    start_key: str | None = None,
    temp: float = 1.0,
    seed: int | None = None,
) -> tuple[str, str, float]:
    """Return (best_key, plaintext, log_L).

    Parameters
    ----------
    iters : int
        Number of M-H iterations.
    temp : float
        Temperature for M-H (higher = more exploration, lower = faster convergence to local optimum).
    """
    rng = np.random.default_rng(seed)
    key = start_key or next(_random_keys(rng))

    plain = decrypt(cipher, key)
    ll = plausibility(plain, tm_ref)
    best_key, best_ll = key, ll

    key_list = list(key)

    for i in range(iters):
        a, b = rng.choice(ALPH_LEN, 2, replace=False)
        key_list[a], key_list[b] = key_list[b], key_list[a]
        cand_key = "".join(key_list)

        cand_plain = decrypt(cipher, cand_key)
        cand_ll = plausibility(cand_plain, tm_ref)

        # Metropolis-Hastings acceptance criterion
        # Based on p_candidate/p_current = exp((log_p_candidate - log_p_current) / temp)
        
        delta_ll = cand_ll - ll
        accept = False

        if temp <= 0:  # Greedy approach for temp = 0 or non-positive temp
            if delta_ll >= 0:
                accept = True
        else:
            # Standard Metropolis-Hastings with temperature, following user-provided structure
            accept_ratio = np.exp(delta_ll / temp)
            # Accept if candidate is better (accept_ratio > 1),
            # or if candidate is worse, accept with probability accept_ratio.
            accept = accept_ratio > 1 or rng.random() < accept_ratio

        if accept:
            key, ll, plain = cand_key, cand_ll, cand_plain
            if ll > best_ll:
                best_key, best_ll = key, ll
        else:
            key_list[a], key_list[b] = key_list[b], key_list[a]

        if i % 50 == 0:
            log.debug("iter=%5d  logL=%12.3f", i, ll)

    return best_key, decrypt(cipher, best_key), best_ll
