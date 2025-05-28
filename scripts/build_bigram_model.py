"""
CLI skript pro vytvoření bigramového modelu z textového korpusu.
Příklad: python scripts/build_bigram_model.py --input_dir data/raw/corpus --output_model data/model/bigram_matrix.npy
"""
# Importy
import argparse
import os
import numpy as np
from pathlib import Path

# Importy z projektu subcipher
from subcipher.stats import transition_matrix
from subcipher.text_utils import clean_text

def main():
    # Zpracování argumentů příkazové řádky
    parser = argparse.ArgumentParser(description="Vytvoří bigramový model z textového korpusu.")
    parser.add_argument("--input_dir", required=True, help="Adresář obsahující surové textové soubory pro korpus.")
    parser.add_argument("--output_model", required=True, help="Cesta pro uložení vygenerovaného bigramového modelu (např. .npy).")
    args = parser.parse_args()

    print(f"Vytváření bigramového modelu z korpusu v: {args.input_dir}")
    print(f"Výstupní model bude uložen do: {args.output_model}")

    input_path = Path(args.input_dir)
    output_file_path = Path(args.output_model)

    corpus_texts = []
    if not input_path.is_dir():
        print(f"Chyba: Vstupní adresář '{args.input_dir}' nebyl nalezen nebo není adresář.")
        return

    # Načtení textů z korpusu
    for item in input_path.iterdir():
        if item.is_file():
            try:
                with open(item, 'r', encoding='utf-8', errors='ignore') as f: # Specifikace kódování a ošetření chyb
                    corpus_texts.append(f.read())
                print(f"Načten soubor: {item}")
            except Exception as e:
                print(f"Nepodařilo se načíst soubor {item}: {e}")

    if not corpus_texts:
        print("Ve vstupním adresáři nebyly nalezeny žádné textové soubory.")
        return

    full_corpus = "\n".join(corpus_texts)
    print(f"Celková délka surového korpusu: {len(full_corpus)} znaků.")

    # Čištění korpusu
    print("Čištění korpusu...")
    cleaned_corpus = clean_text(full_corpus)
    print(f"Délka vyčištěného korpusu: {len(cleaned_corpus)} znaků.")

    if not cleaned_corpus:
        print("Vyčištěný korpus je prázdný. Model nelze vytvořit.")
        return

    # Výpočet matice přechodů
    print("Výpočet matice přechodů...")
    tm = transition_matrix(cleaned_corpus)

    # Uložení modelu
    try:
        output_file_path.parent.mkdir(parents=True, exist_ok=True) # Vytvoření cílového adresáře, pokud neexistuje
        np.save(output_file_path, tm)
        print(f"Bigramový model úspěšně uložen do: {args.output_model}")
    except Exception as e:
        print(f"Chyba při ukládání modelu do {args.output_model}: {e}")

if __name__ == "__main__":
    main()
