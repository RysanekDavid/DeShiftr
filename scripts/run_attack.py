"""
CLI script for running a cryptanalysis attack using subcipher.
Example:
python scripts/run_attack.py \
    --ciphertext_file data/raw/teacher_cipher.txt \
    --model_path data/model/reference_tm.npy \
    --output_dir exports/run01 \
    --length 1000 \
    --sample_id 1 \
    --iters 20000
"""
import argparse
import numpy as np
from pathlib import Path

from subcipher.mh import crack
from subcipher.io import export_result
from subcipher.text_utils import clean_text

def main():
    parser = argparse.ArgumentParser(description="Run subcipher cryptanalysis attack.")
    parser.add_argument("--ciphertext_file", required=True, type=Path,
                        help="Path to the input ciphertext file.")
    parser.add_argument("--model_path", type=Path, default=Path("data/model/reference_tm.npy"),
                        help="Path to the reference transition matrix (.npy file).")
    parser.add_argument("--output_dir", type=Path, default=Path("exports/attack_results"),
                        help="Directory to save the output plaintext and key.")
    
    # Parameters for export_result
    parser.add_argument("--length", required=True, type=int,
                        help="Length parameter for naming output files (e.g., length of original text).")
    parser.add_argument("--sample_id", required=True, type=int,
                        help="Sample ID for naming output files.")

    # Parameters for crack function
    parser.add_argument("--iters", type=int, default=20_000,
                        help="Number of iterations for Metropolis-Hastings.")
    parser.add_argument("--temp", type=float, default=1.0,
                        help="Temperature for softmax in M-H.")
    parser.add_argument("--seed", type=int, default=None,
                        help="Random seed for M-H.")
    parser.add_argument("--start_key", type=str, default=None,
                        help="Optional starting key for M-H.")

    args = parser.parse_args()

    print(f"Running attack with the following parameters:")
    print(f"  Ciphertext file: {args.ciphertext_file}")
    print(f"  Reference model: {args.model_path}")
    print(f"  Output directory: {args.output_dir}")
    print(f"  Output length ID: {args.length}")
    print(f"  Output sample ID: {args.sample_id}")
    print(f"  Crack iterations: {args.iters}")
    print(f"  Crack temperature: {args.temp}")
    print(f"  Crack seed: {args.seed}")
    print(f"  Crack start_key: {args.start_key if args.start_key else 'Random'}")

    if not args.ciphertext_file.is_file():
        print(f"Error: Ciphertext file '{args.ciphertext_file}' not found.")
        return
    try:
        with open(args.ciphertext_file, 'r', encoding='utf-8') as f:
            ciphertext = f.read()
        print(f"Successfully loaded ciphertext (length: {len(ciphertext)}).")
    except Exception as e:
        print(f"Error reading ciphertext file {args.ciphertext_file}: {e}")
        return

    # It's good practice to clean the ciphertext to ensure it matches the alphabet
    # used for the reference model.
    # If the ciphertext is guaranteed to be clean, this step can be skipped.
    cleaned_ciphertext = clean_text(ciphertext)
    if len(cleaned_ciphertext) != len(ciphertext):
        print(f"Ciphertext was cleaned. Original length: {len(ciphertext)}, Cleaned length: {len(cleaned_ciphertext)}")
    
    if not cleaned_ciphertext:
        print("Ciphertext is empty after cleaning. Cannot proceed.")
        return

    if not args.model_path.is_file():
        print(f"Error: Reference model file '{args.model_path}' not found.")
        return
    try:
        tm_ref = np.load(args.model_path)
        print(f"Successfully loaded reference transition matrix from '{args.model_path}'.")
    except Exception as e:
        print(f"Error loading reference model {args.model_path}: {e}")
        return

    print("Starting cryptanalysis (crack function)...")
    try:
        best_key, plaintext, best_ll = crack(
            cleaned_ciphertext,
            tm_ref,
            iters=args.iters,
            start_key=args.start_key,
            temp=args.temp,
            seed=args.seed
        )
        print(f"Cryptanalysis finished. Best log-likelihood: {best_ll:.3f}")
        print(f"Found key: {best_key}")

    except Exception as e:
        print(f"Error during cryptanalysis: {e}")
        return

    print(f"Exporting results to directory: {args.output_dir}")
    try:
        export_result(
            plaintext=plaintext,
            key=best_key,
            length=args.length,
            sample_id=args.sample_id,
            dest=args.output_dir
        )
        print("Results exported successfully.")
    except Exception as e:
        print(f"Error exporting results: {e}")

if __name__ == "__main__":
    main()
