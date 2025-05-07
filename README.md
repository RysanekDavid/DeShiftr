[Česká verze](README.cs.md)

# Substitution Cipher Toolkit

This project is a toolkit for working with substitution ciphers. It includes functionalities for encryption, decryption, statistical analysis, and cryptanalysis using methods like Metropolis-Hastings.

## Quick start

This section provides a minimal set of commands to get you started quickly.

1.  **Clone and Install:**

    ```bash
    git clone https://github.com/RysanekDavid/DeShiftr.git
    cd DeShiftr
    pip install -e .[dev]
    ```

2.  **Build Bigram Model:**
    You'll need a corpus text file (e.g., a large text in the expected language of the ciphertext). For this example, let's assume you have your corpus at `data/raw/krakatit.txt`.

    ```bash
    python scripts/build_bigram_model.py --input_file data/raw/krakatit.txt --output_model data/model/bigram_model.npy
    ```

    _(Note: If `build_bigram_model.py` expects a directory of text files, you might use `--input_dir data/raw/corpus/` and place your corpus files there.)_

3.  **Run Attack:**
    This command uses the model built in the previous step to attempt to decrypt a sample ciphertext.
    ```bash
    python scripts/run_attack.py --input_file data/test/text_250_sample_1_ciphertext.txt --model_path data/model/bigram_model.npy --output_file exports/solved_text_250_sample_1.txt
    ```
    You should find the decrypted text in `exports/solved_text_250_sample_1.txt`.

## Project Goals

- Provide a modular library (`subcipher`) for substitution cipher operations.
- Demonstrate usage through Jupyter notebooks (`notebooks/`).
- Ensure code quality with tests (`tests/`) and pre-commit hooks.
- Offer scripts for batch processing (`scripts/`).

## Getting Started

### Prerequisites

- Python 3.8+
- Pip

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/RysanekDavid/DeShiftr.git
   cd DeShiftr
   ```
2. Install the package and its development dependencies:
   ```bash
   pip install -e .[dev]
   ```
3. Set up pre-commit hooks (optional but recommended):
   ```bash
   pre-commit install
   ```

## Running Tests

To run the test suite:

```bash
pytest
```

You can also check test coverage (ensure `pytest-cov` is installed):

```bash
pytest --cov=subcipher
```

## Running Notebooks

1. Ensure you have Jupyter installed (it's included in the `dev` dependencies).
2. Start the Jupyter server:
   ```bash
   jupyter notebook
   ```
3. Open the notebooks located in the `notebooks/` directory via the Jupyter interface in your browser.

## Running Scripts

The `scripts/` directory contains scripts for batch operations. For example:

```bash
python scripts/run_attack.py --input data/raw/some_cipher_text.txt --output exports/solved_cipher.txt
python scripts/build_bigram_model.py --input_dir data/raw/corpus/ --output_model data/model/bigram_matrix.npy
```

(Note: These are example commands; actual script names and arguments may vary.)

## Project Structure

(A brief overview of the main directories and their purpose can be added here, similar to the initial request.)

## Contributing

(Details on how to contribute if applicable.)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
