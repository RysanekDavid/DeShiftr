"""
CLI skript pro spuštění kryptoanalytického útoku pomocí subcipher.
Příklad:
python scripts/run_attack.py \
    --ciphertext_file data/raw/teacher_cipher.txt \
    --model_path data/model/reference_tm.npy \
    --output_dir exports/run01 \
    --length 1000 \
    --sample_id 1 \
    --iters 20000
"""
# Importy
import argparse
import numpy as np
from pathlib import Path

# Importy z projektu subcipher
from subcipher.mh import crack
from subcipher.io import export_result
from subcipher.text_utils import clean_text

def main():
    # Zpracování argumentů příkazové řádky
    parser = argparse.ArgumentParser(description="Spustí kryptoanalytický útok subcipher.")
    parser.add_argument("--ciphertext_file", required=True, type=Path,
                        help="Cesta k vstupnímu souboru se šifrovým textem.")
    parser.add_argument("--model_path", type=Path, default=Path("data/model/reference_tm.npy"),
                        help="Cesta k referenční matici přechodů (.npy soubor).")
    parser.add_argument("--output_dir", type=Path, default=Path("exports/attack_results"),
                        help="Adresář pro uložení výstupního otevřeného textu a klíče.")
    
    # Parametry pro export_result (pojmenování výstupních souborů)
    parser.add_argument("--length", required=True, type=int,
                        help="Parametr délky pro pojmenování výstupních souborů (např. délka původního textu).")
    parser.add_argument("--sample_id", required=True, type=int,
                        help="ID vzorku pro pojmenování výstupních souborů.")

    # Parametry pro funkci crack (Metropolis-Hastings)
    parser.add_argument("--iters", type=int, default=20_000,
                        help="Počet iterací pro Metropolis-Hastings.")
    parser.add_argument("--temp", type=float, default=1.0,
                        help="Teplota pro Metropolis-Hastings.")
    parser.add_argument("--seed", type=int, default=None,
                        help="Random seed pro Metropolis-Hastings.")
    parser.add_argument("--start_key", type=str, default=None,
                        help="Volitelný počáteční klíč pro Metropolis-Hastings.")

    args = parser.parse_args()

    print(f"Spouštění útoku s následujícími parametry:")
    print(f"  Soubor se šifrovým textem: {args.ciphertext_file}")
    print(f"  Referenční model: {args.model_path}")
    print(f"  Výstupní adresář: {args.output_dir}")
    print(f"  ID délky výstupu: {args.length}")
    print(f"  ID vzorku výstupu: {args.sample_id}")
    print(f"  Počet iterací (crack): {args.iters}")
    print(f"  Teplota (crack): {args.temp}")
    print(f"  Seed (crack): {args.seed}")
    print(f"  Počáteční klíč (crack): {args.start_key if args.start_key else 'Náhodný'}")

    # Načtení šifrového textu
    if not args.ciphertext_file.is_file():
        print(f"Chyba: Soubor se šifrovým textem '{args.ciphertext_file}' nebyl nalezen.")
        return
    try:
        with open(args.ciphertext_file, 'r', encoding='utf-8') as f:
            ciphertext = f.read()
        print(f"Šifrový text úspěšně načten (délka: {len(ciphertext)}).")
    except Exception as e:
        print(f"Chyba při čtení souboru se šifrovým textem {args.ciphertext_file}: {e}")
        return

    # Čištění šifrového textu (doporučeno pro konzistenci s modelem)
    cleaned_ciphertext = clean_text(ciphertext)
    if len(cleaned_ciphertext) != len(ciphertext):
        print(f"Šifrový text byl vyčištěn. Původní délka: {len(ciphertext)}, Vyčištěná délka: {len(cleaned_ciphertext)}")
    
    if not cleaned_ciphertext:
        print("Šifrový text je po vyčištění prázdný. Nelze pokračovat.")
        return

    # Načtení referenčního modelu
    if not args.model_path.is_file():
        print(f"Chyba: Soubor s referenčním modelem '{args.model_path}' nebyl nalezen.")
        return
    try:
        tm_ref = np.load(args.model_path)
        print(f"Referenční matice přechodů úspěšně načtena z '{args.model_path}'.")
    except Exception as e:
        print(f"Chyba při načítání referenčního modelu {args.model_path}: {e}")
        return

    # Spuštění kryptoanalýzy
    print("Spouštění kryptoanalýzy (funkce crack)...")
    try:
        best_key, plaintext, best_ll = crack(
            cleaned_ciphertext,
            tm_ref,
            iters=args.iters,
            start_key=args.start_key,
            temp=args.temp,
            seed=args.seed
        )
        print(f"Kryptoanalýza dokončena. Nejlepší log-věrohodnost: {best_ll:.3f}")
        print(f"Nalezený klíč: {best_key}")

    except Exception as e:
        print(f"Chyba během kryptoanalýzy: {e}")
        return

    # Export výsledků
    print(f"Export výsledků do adresáře: {args.output_dir}")
    try:
        args.output_dir.mkdir(parents=True, exist_ok=True) # Vytvoření cílového adresáře, pokud neexistuje
        export_result(
            plaintext=plaintext,
            key=best_key,
            length=args.length, # Použití args.length pro konzistenci s pojmenováním
            sample_id=args.sample_id,
            dest=args.output_dir
        )
        print("Výsledky úspěšně exportovány.")
    except Exception as e:
        print(f"Chyba při exportu výsledků: {e}")

if __name__ == "__main__":
    main()
