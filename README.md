[Česká verze](README.cs.md)

# Substitution Cipher Tools

This project is a set of tools for working with substitution ciphers. It includes functions for encryption, decryption, statistical analysis, and cryptanalysis using methods such as Metropolis-Hastings.

## Project Structure (Overview)

- `subcipher/`: Main Python library with implementation of cipher, cryptanalysis, etc.
- `scripts/`: Helper Python scripts for operations like creating a bigram model or running an attack from the command line.
- `notebooks/`: Jupyter Notebooks demonstrating the use of the library and the solution process.
- `data/`:
  - `data/raw/corpus/`: Directory for storing raw text corpus files (e.g., `krakatit.txt`).
  - `data/model/`: Directory for storing the generated reference bigram model (e.g., `reference_tm.npy`).
  - `data/test/`: Directory for storing test encrypted texts (e.g., `text_1000_sample_1_ciphertext.txt`).
- `exports/`: Directory where cryptanalysis results (decrypted texts and keys) are saved.
- `tests/`: Unit tests for the library.
- `run_attack.bat`: Batch file for easily running a cryptanalytic attack with preset parameters.
- `build_model.bat`: Batch file for easily creating a reference bigram model.

## Getting Started

### Prerequisites

- Python 3.8+
- Pip (Python package management tool)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/RysanekDavid/DeShiftr.git
    cd DeShiftr
    ```

2.  **Install the package and its development dependencies:**
    It is recommended to create and activate a virtual environment (e.g., using `venv` or `conda`).

    ```bash
    python -m venv venv
    # Activate virtual environment:
    # Windows:
    # venv\Scripts\activate
    # macOS/Linux:
    # source venv/bin/activate

    pip install -e .[dev]
    ```

    This command installs the `subcipher` library in editable mode and all necessary dependencies for development and execution (NumPy, Matplotlib, Seaborn, Jupyter, Pytest, etc.).

3.  **Set up pre-commit hooks (optional, but recommended for development):**
    ```bash
    pre-commit install
    ```

## Quick Start: Breaking a Sample Cipher

This section will guide you through the basic steps to break the `text_1000_sample_1_ciphertext.txt` cipher using the provided tools. **Run all commands from the root directory of the project (`DeShiftr/`).**

1.  **Corpus Preparation:**

    - Download a large Czech text file that will serve as the basis for the statistical language model. We recommend the text of the book "Krakatit" by Karel Čapek from [Wikisource](https://cs.wikisource.org/wiki/Krakatit).
    - Save this file as `krakatit.txt` in the `data/raw/corpus/` directory in your project. (If the `data/raw/corpus/` directories do not exist, create them).

2.  **Building the Reference Bigram Model:**
    This step creates the `data/model/reference_tm.npy` file, which is necessary for cryptanalysis.

    - **Option A: Using a batch file (recommended for simplicity):**
      ```bash
      build_model.bat
      ```
    - **Option B: Running the Python script directly:**
      ```bash
      python scripts/build_bigram_model.py --input_dir data/raw/corpus/ --output_model data/model/reference_tm.npy
      ```
      After successful execution, you should see the message "Bigram model successfully saved to: data/model/reference_tm.npy" and debug outputs from the `transition_matrix` function, confirming the model's quality (e.g., `Max probability ... ~0.019` or higher).

3.  **Running the Cryptanalytic Attack:**
    Now we will break the `text_1000_sample_1_ciphertext.txt` cipher. Make sure this file is located in `data/test/`.

    - **Option A: Using a batch file (recommended for simplicity with verified parameters):**
      ```bash
      run_attack.bat
      ```
      This file is preset for `text_1000_sample_1_ciphertext.txt` with parameters (`iters=120000`, `seed=12345`) that led to good results.
    - **Option B: Running the Python script directly with custom parameters:**
      ```bash
      python scripts/run_attack.py --ciphertext_file data/test/text_1000_sample_1_ciphertext.txt --length 1000 --sample_id 1 --iters 120000 --seed 12345
      ```
      You can experiment with the `--iters` and `--seed` values (or omit `seed` for a random start). A higher number of iterations usually leads to better results.
    - **Option C: Using the Jupyter Notebook `notebooks/03_attack.ipynb`:**
      Open this notebook (see the "Running Notebooks" section) and run the cells sequentially. The notebook is set up to dynamically determine paths and should load the correct files. You can easily change parameters like `iters` and `seed` in it.

    The resulting decrypted text and key will be saved in the `exports/script_attack_results/` folder (for script/bat) or `exports/notebook_attack_results/` folder (for notebook). Compare the result with the reference solution from the `zadani.pdf` file.

## Running Tests

To run the test suite (from the project root directory):

```bash
pytest
```

To check test coverage (requires `pytest-cov`):

```bash
pytest --cov=subcipher
```

## Running Notebooks

1.  Make sure you have Jupyter installed (it is included in the development dependencies – see the Installation section).
2.  **Run Jupyter from the project root directory:**
    ```bash
    jupyter notebook
    ```
    Or if you prefer JupyterLab:
    ```bash
    jupyter lab
    ```
3.  In the Jupyter web interface, navigate to the `notebooks/` folder and open the desired notebook (`01_demo.ipynb`, `02_bigram_model.ipynb`, `03_attack.ipynb`). The notebooks contain code to dynamically determine paths to data files, so they should work correctly if Jupyter is run from the project root.

## Running Scripts from the Command Line (Advanced)

In addition to `.bat` files, you can also run scripts directly. The following commands are run from the project root directory:

- **Creating a reference bigram model:**

  ```bash
  python scripts/build_bigram_model.py --input_dir data/raw/corpus/ --output_model data/model/reference_tm.npy
  ```

  Required arguments:

  - `--input_dir`: Directory with corpus texts (e.g., `data/raw/corpus/`).
  - `--output_model`: Path to save the resulting `.npy` file (e.g., `data/model/reference_tm.npy`).

- **Running a cryptanalytic attack:**

  ```bash
  python scripts/run_attack.py --ciphertext_file <path_to_cipher> --length <length> --sample_id <id> [other_optional_arguments]
  ```

  Required arguments:

  - `--ciphertext_file`: Path to the ciphertext file (e.g., `data/test/text_1000_sample_1_ciphertext.txt`).
  - `--length`: Nominal length of the text for naming output files.
  - `--sample_id`: Sample ID for naming output files.

  Optional arguments (have default values):

  - `--model_path`: Path to `reference_tm.npy` (default: `data/model/reference_tm.npy`).
  - `--output_dir`: Directory for exporting results (default: `exports/attack_results_script/`).
  - `--iters`: Number of M-H iterations (default: 20000).
  - `--temp`: Temperature for M-H (default: 1.0).
  - `--seed`: Seed for the random number generator (default: None).
  - `--start_key`: Initial key (default: None, i.e., random).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
