"""Prolomení substituční šifry pomocí algoritmu Metropolis-Hastings."""

# Importy
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
    """Generátor náhodných permutací abecedy."""
    while True:
        yield "".join(rng.permutation(list(ALPHABET)))


def crack(
    cipher: str,
    tm_ref: np.ndarray,
    *,
    iters: int = 20_000,  # Počet iterací M-H
    start_key: str | None = None, # Počáteční klíč
    temp: float = 1.0,  # Teplota pro M-H (vyšší = více explorace)
    seed: int | None = None, # Seed pro generátor náhodných čísel
) -> tuple[str, str, float]:
    """Vrátí (nejlepší_klíč, otevřený_text, log_věrohodnost)."""
    rng = np.random.default_rng(seed)
    key = start_key or next(_random_keys(rng))

    plain = decrypt(cipher, key)
    ll = plausibility(plain, tm_ref) # Log-věrohodnost
    best_key, best_ll = key, ll

    key_list = list(key)

    for i in range(iters):
        # Navrhni nový klíč prohozením dvou znaků
        a, b = rng.choice(ALPH_LEN, 2, replace=False)
        key_list[a], key_list[b] = key_list[b], key_list[a]
        cand_key = "".join(key_list)

        cand_plain = decrypt(cipher, cand_key)
        cand_ll = plausibility(cand_plain, tm_ref)

        # Akceptační kritérium Metropolis-Hastings
        delta_ll = cand_ll - ll
        accept = False

        if temp <= 0:  # Hladový přístup pro temp <= 0
            if delta_ll >= 0:
                accept = True
        else:
            # Standardní Metropolis-Hastings s teplotou
            accept_ratio = np.exp(delta_ll / temp)
            accept = accept_ratio > 1 or rng.random() < accept_ratio

        if accept:
            key, ll, plain = cand_key, cand_ll, cand_plain
            if ll > best_ll: # Aktualizace nejlepšího nalezeného klíče
                best_key, best_ll = key, ll
        else:
            # Vrácení změny, pokud kandidát nebyl přijat
            key_list[a], key_list[b] = key_list[b], key_list[a]

        if i % 50 == 0:
            log.debug("iter=%5d  logL=%12.3f", i, ll)

    return best_key, decrypt(cipher, best_key), best_ll
