# Substitution Cipher Toolkit

This project is a toolkit for working with substitution ciphers. It includes functionalities for encryption, decryption, statistical analysis, and cryptanalysis using methods like Metropolis-Hastings.

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
   git clone https://github.com/yourusername/subcipher.git # Replace with actual URL
   cd subcipher
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
