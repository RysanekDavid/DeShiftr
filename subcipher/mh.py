"""Metropolis‑Hastings prolomení substituční šifry."""

from __future__ import annotations

import logging
from typing import Tuple, Generator

import numpy as np

from .alphabet import ALPHABET, ALPH_LEN
from .codec import decrypt
from .stats import plausibility

__all__ = ["crack"]

log = logging.getLogger(__name__)
DEFAULT_P_BAD = 0.01


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
    p_bad: float = DEFAULT_P_BAD,
    temp: float = 1.0,
    seed: int | None = None,
) -> Tuple[str, str, float]:
    """Vrať (nejlepší_klíč, plaintext, log_L).

    Parametry
    ----------
    iters : int
        Počet iterací M‑H.
    p_bad : float
        Pravděpodobnost, že přijmeme horší klíč (analog „skok přes bariéru“).
    temp : float
        Teplota pro soft‑max (vyšší = víc zkoumání prostoru).
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

        accept = False
        if cand_ll > ll:  # Candidate is better
            accept = True
        elif rng.random() < p_bad:  # Candidate is worse, accept with p_bad probability
            accept = True
        # Note: The 'temp' parameter is not used in this acceptance logic if p_bad is a fixed chance.
        # If 'temp' should be used, the logic would be:
        # accept_ratio = np.exp((cand_ll - ll) / temp)
        # if accept_ratio > 1 or rng.random() < accept_ratio * (some_factor_if_p_bad_is_not_fixed_chance)
        # For now, strictly following the user's pseudocode for the ELSE IF part.
        # The pseudocode implies p_bad is a fixed chance for any worse state.

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
