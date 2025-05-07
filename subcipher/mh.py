"""Metropolis‑Hastings prolomení substituční šifry."""

from __future__ import annotations

import logging
from collections.abc import Generator # Changed from typing.Generator
from typing import Tuple

import numpy as np

from .alphabet import ALPHABET, ALPH_LEN
from .codec import decrypt
from .stats import plausibility

__all__ = ["crack"]

log = logging.getLogger(__name__)


def _random_keys(rng: np.random.Generator) -> Generator[str, None, None]:
    """Nekonečný generátor náhodných permutací abecedy."""
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
) -> tuple[str, str, float]: # Changed from typing.Tuple
    """Vrať (nejlepší_klíč, plaintext, log_L).

    Parametry
    ----------
    iters : int
        Počet iterací M‑H.
    temp : float
        Teplota pro M‑H (vyšší = víc zkoumání prostoru, nižší = rychlejší konvergence k lokálnímu optimu).
    """
    rng = np.random.default_rng(seed)
    key = start_key or next(_random_keys(rng))

    plain = decrypt(cipher, key)
    ll = plausibility(plain, tm_ref)
    best_key, best_ll = key, ll

    key_list = list(key)

    for i in range(iters):
        # Návrh: prohodíme 2 znaky
        a, b = rng.choice(ALPH_LEN, 2, replace=False)
        key_list[a], key_list[b] = key_list[b], key_list[a]
        cand_key = "".join(key_list)

        cand_plain = decrypt(cipher, cand_key)
        cand_ll = plausibility(cand_plain, tm_ref)

        # Metropolis-Hastings acceptance criterion
        # Based on p_candidate/p_current = exp((log_p_candidate - log_p_current) / temp)
        
        delta_ll = cand_ll - ll
        accept = False # Initialize accept to False

        if temp <= 0:  # Greedy approach for temp = 0 or non-positive temp
            if delta_ll >= 0: # Accept if candidate is better or equal
                accept = True
        else:
            # Standard Metropolis-Hastings with temperature, following user-provided structure
            accept_ratio = np.exp(delta_ll / temp)
            # Accept if candidate is better (accept_ratio > 1),
            # or if candidate is worse, accept with probability accept_ratio.
            if accept_ratio > 1 or rng.random() < accept_ratio:
                accept = True

        if accept:
            key, ll, plain = cand_key, cand_ll, cand_plain
            if ll > best_ll:
                best_key, best_ll = key, ll
        else:
            # vrátíme prohození zpět
            key_list[a], key_list[b] = key_list[b], key_list[a]

        if i % 50 == 0:
            log.debug("iter=%5d  logL=%12.3f", i, ll)

    return best_key, decrypt(cipher, best_key), best_ll
