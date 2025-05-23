"""
CLI script for building a bigram model from a text corpus.
Example: python scripts/build_bigram_model.py --input_dir data/raw/corpus --output_model data/model/bigram_matrix.npy
"""
import argparse
import os
import numpy as np
from pathlib import Path

# Assuming subcipher is installed or PYTHONPATH is set correctly
from subcipher.stats import transition_matrix
from subcipher.text_utils import clean_text

def main():
    parser = argparse.ArgumentParser(description="Build a bigram model from a text corpus.")
    parser.add_argument("--input_dir", required=True, help="Directory containing raw text files for the corpus.")
    parser.add_argument("--output_model", required=True, help="Path to save the generated bigram model (e.g., .npy).")
    args = parser.parse_args()

    print(f"Building bigram model from corpus in: {args.input_dir}")
    print(f"Output model will be saved to: {args.output_model}")

    input_path = Path(args.input_dir)
    output_file_path = Path(args.output_model)

    corpus_texts = []
    if not input_path.is_dir():
        print(f"Error: Input directory '{args.input_dir}' not found or is not a directory.")
        return

    for item in input_path.iterdir():
        if item.is_file():
            try:
                with open(item, 'r', encoding='utf-8', errors='ignore') as f: # Specify encoding and error handling
                    corpus_texts.append(f.read())
                print(f"Read file: {item}")
            except Exception as e:
                print(f"Could not read file {item}: {e}")

    if not corpus_texts:
        print("No text files found in the input directory.")
        return

    full_corpus = "\n".join(corpus_texts)
    print(f"Total raw corpus length: {len(full_corpus)} characters.")

    print("Cleaning corpus...")
    cleaned_corpus = clean_text(full_corpus)
    print(f"Cleaned corpus length: {len(cleaned_corpus)} characters.")

    if not cleaned_corpus:
        print("Cleaned corpus is empty. Cannot build model.")
        return

    print("Calculating transition matrix...")
    tm = transition_matrix(cleaned_corpus)

    try:
        output_file_path.parent.mkdir(parents=True, exist_ok=True)
        np.save(output_file_path, tm)
        print(f"Bigram model saved successfully to: {args.output_model}")
    except Exception as e:
        print(f"Error saving model to {args.output_model}: {e}")

if __name__ == "__main__":
    main()
