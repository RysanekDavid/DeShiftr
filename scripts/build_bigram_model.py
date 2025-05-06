"""
CLI script for building a bigram model from a text corpus.
Example: python scripts/build_bigram_model.py --input_dir data/raw/corpus --output_model data/model/bigram_matrix.npy
"""
import argparse
import os
# import numpy as np # Placeholder
# from subcipher.stats import calculate_bigram_frequencies # Placeholder
# from subcipher.io import save_numpy_array # Placeholder

def main():
    parser = argparse.ArgumentParser(description="Build a bigram model from a text corpus.")
    parser.add_argument("--input_dir", required=True, help="Directory containing raw text files for the corpus.")
    parser.add_argument("--output_model", required=True, help="Path to save the generated bigram model (e.g., .npy or .pkl).")
    # Add more arguments as needed (e.g., alphabet, cleaning options)
    args = parser.parse_args()

    print(f"Building bigram model from corpus in: {args.input_dir}")
    print(f"Output model will be saved to: {args.output_model}")

    corpus_texts = []
    if not os.path.isdir(args.input_dir):
        print(f"Error: Input directory '{args.input_dir}' not found.")
        return

    for filename in os.listdir(args.input_dir):
        filepath = os.path.join(args.input_dir, filename)
        if os.path.isfile(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f: # Specify encoding
                    corpus_texts.append(f.read())
                print(f"Read file: {filepath}")
            except Exception as e:
                print(f"Could not read file {filepath}: {e}")

    if not corpus_texts:
        print("No text files found in the input directory.")
        return

    full_corpus = "\\n".join(corpus_texts) # Join with newlines, or just concatenate

    # --- Placeholder for actual model building logic ---
    # 1. Preprocess/clean the full_corpus (e.g., remove punctuation, normalize case)
    # 2. Calculate bigram frequencies using subcipher.stats
    # 3. Convert frequencies to a transition matrix (e.g., numpy array)
    # 4. Save the matrix to args.output_model using subcipher.io
    # Example:
    # cleaned_corpus = preprocess_text(full_corpus) # Assuming this function exists
    # bigram_matrix = calculate_bigram_frequencies(cleaned_corpus, alphabet) # Assuming alphabet is defined
    # save_numpy_array(args.output_model, bigram_matrix)
    print(f"Corpus length: {len(full_corpus)} characters.")
    print("Bigram model building logic not yet implemented.")
    # --- End Placeholder ---

if __name__ == "__main__":
    main()
