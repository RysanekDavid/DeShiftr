"""Export výsledků do struktury požadované zadáním."""

# Importy
from __future__ import annotations
from pathlib import Path


def export_result(
    plaintext: str,
    key: str,
    *,
    length: int,
    sample_id: int,
    dest: str | Path = "exports",
) -> None:
    """Uloží otevřený text a klíč do správně pojmenovaných souborů."""
    if length != len(plaintext):
        raise ValueError(
            f"Zadaná délka ({length}) neodpovídá skutečné délce otevřeného textu ({len(plaintext)})."
        )
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True) # Vytvoří adresář, pokud neexistuje

    # Uložení otevřeného textu
    (dest / f"text_{length}_sample_{sample_id}_plaintext.txt").write_text(
        plaintext, encoding="utf-8"
    )
    # Uložení klíče
    (dest / f"text_{length}_sample_{sample_id}_key.txt").write_text(
        key, encoding="utf-8"
    )
