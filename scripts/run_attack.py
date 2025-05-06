"""
CLI script for running a cryptanalysis attack.
Example: python scripts/run_attack.py --input data/raw/cipher.txt --output exports/plaintext.txt
"""
import argparse

def main():
    parser = argparse.ArgumentParser(description="Run cryptanalysis attack.")
    parser.add_argument("--input", required=True, help="Path to the input ciphertext file.")
    parser.add_argument("--output", required=True, help="Path to save the output plaintext file.")
    # Add more arguments as needed (e.g., model path, algorithm parameters)
    args = parser.parse_args()

    print(f"Running attack on: {args.input}")
    print(f"Output will be saved to: {args.output}")

    # --- Placeholder for actual attack logic ---
    # 1. Load ciphertext from args.input
    # 2. Load any necessary models (e.g., bigram matrix)
    # 3. Run the Metropolis-Hastings (or other) algorithm
    # 4. Save the resulting plaintext to args.output
    # Example:
    # from subcipher.io import read_file, write_file
    # from subcipher.mh import run_metropolis_hastings # Assuming this function exists
    #
    # ciphertext = read_file(args.input)
    # # model = load_model(...)
    # # plaintext = run_metropolis_hastings(ciphertext, model, ...)
    # # write_file(args.output, plaintext)
    print("Attack logic not yet implemented.")
    # --- End Placeholder ---

if __name__ == "__main__":
    main()
