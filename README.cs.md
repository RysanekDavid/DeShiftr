## Návrh upraveného `README.md`

Zde jsou upravené sekce. Zaměřil jsem se na sjednocení argumentů a přidání poznámek o `.bat` souborech a spouštění notebooků.

````markdown
[English version](README.md)

# Nástroje pro substituční šifru

Tento projekt je sada nástrojů pro práci se substitučními šiframi. Zahrnuje funkce pro šifrování, dešifrování, statistickou analýzu a kryptoanalýzu pomocí metod, jako je Metropolis-Hastings.

## Struktura projektu (Přehled)

- `subcipher/`: Hlavní Python knihovna s implementací šifry, kryptoanalýzy atd.
- `scripts/`: Pomocné Python skripty pro operace jako tvorba bigramového modelu nebo spuštění útoku z příkazové řádky.
- `notebooks/`: Jupyter Notebooky demonstrující použití knihovny a postup řešení.
- `data/`:
  - `data/raw/corpus/`: Adresář pro uložení surových textových souborů korpusu (např. `krakatit.txt`).
  - `data/model/`: Adresář pro uložení vygenerovaného referenčního bigramového modelu (např. `reference_tm.npy`).
  - `data/test/`: Adresář pro uložení testovacích šifrovaných textů (např. `text_1000_sample_1_ciphertext.txt`).
- `exports/`: Adresář, kam se ukládají výsledky kryptoanalýzy (dešifrované texty a klíče).
- `tests/`: Unit testy pro knihovnu.
- `run_attack.bat`: Dávkový soubor pro snadné spuštění kryptoanalytického útoku s přednastavenými parametry.
- `build_model.bat`: Dávkový soubor pro snadné vytvoření referenčního bigramového modelu.

## Začínáme

### Předpoklady

- Python 3.8+
- Pip (nástroj pro správu Python balíčků)

### Instalace

1.  **Klonujte repozitář:**

    ```bash
    git clone [https://github.com/RysanekDavid/DeShiftr.git](https://github.com/RysanekDavid/DeShiftr.git)
    cd DeShiftr
    ```

2.  **Nainstalujte balíček a jeho vývojové závislosti:**
    Doporučuje se vytvořit a aktivovat virtuální prostředí (např. pomocí `venv` nebo `conda`).

    ```bash
    python -m venv venv
    # Aktivace virtuálního prostředí:
    # Windows:
    # venv\Scripts\activate
    # macOS/Linux:
    # source venv/bin/activate

    pip install -e .[dev]
    ```

    Tento příkaz nainstaluje knihovnu `subcipher` v editovatelném režimu a všechny potřebné závislosti pro vývoj a běh (NumPy, Matplotlib, Seaborn, Jupyter, Pytest atd.).

3.  **Nastavte pre-commit hooky (volitelné, ale doporučené pro vývoj):**
    ```bash
    pre-commit install
    ```

## Rychlý start: Prolomení ukázkové šifry

Tato sekce vás provede základními kroky k prolomení šifry `text_1000_sample_1_ciphertext.txt` pomocí poskytnutých nástrojů. **Všechny příkazy spouštějte z kořenového adresáře projektu (`DeShiftr/`).**

1.  **Příprava korpusu:**

    - Stáhněte si velký český textový soubor, který bude sloužit jako základ pro statistický model jazyka. Doporučujeme text knihy "Krakatit" od Karla Čapka z [Wikisource](https://cs.wikisource.org/wiki/Krakatit).
    - Uložte tento soubor jako `krakatit.txt` do adresáře `data/raw/corpus/` ve vašem projektu. (Pokud adresáře `data/raw/corpus/` neexistují, vytvořte je).

2.  **Sestavení referenčního bigramového modelu:**
    Tento krok vytvoří soubor `data/model/reference_tm.npy`, který je nezbytný pro kryptoanalýzu.

        - **Možnost A: Použití dávkového souboru (doporučeno pro jednoduchost):**
          ```bash
          build_model.bat
          ```
        - **Možnost B: Spuštění Python skriptu přímo:**
          `bash

    python scripts/build_bigram_model.py --input_dir data/raw/corpus/ --output_model data/model/reference_tm.npy
    `      Po úspěšném běhu byste měli vidět zprávu "Bigramový model úspěšně uložen do: data/model/reference_tm.npy" a debugovací výpisy z funkce`transition_matrix`, které potvrzují kvalitu modelu (např. `Max probability ... ~0.019` nebo vyšší).

3.  **Spuštění kryptoanalytického útoku:**
    Nyní prolomíme šifru `text_1000_sample_1_ciphertext.txt`. Ujistěte se, že tento soubor je umístěn v `data/test/`.

    - **Možnost A: Použití dávkového souboru (doporučeno pro jednoduchost s ověřenými parametry):**
      ```bash
      run_attack.bat
      ```
      Tento soubor je přednastaven pro `text_1000_sample_1_ciphertext.txt` s parametry (`iters=120000`, `seed=12345`), které vedly k dobrým výsledkům.
    - **Možnost B: Spuštění Python skriptu přímo s vlastními parametry:**
      ```bash
      python scripts/run_attack.py --ciphertext_file data/test/text_1000_sample_1_ciphertext.txt --length 1000 --sample_id 1 --iters 120000 --seed 12345
      ```
      Můžete experimentovat s hodnotami `--iters` a `--seed` (nebo `seed` vynechat pro náhodný start). Vyšší počet iterací obvykle vede k lepším výsledkům.
    - **Možnost C: Použití Jupyter Notebooku `notebooks/03_attack.ipynb`:**
      Otevřete tento notebook (viz sekce "Spouštění notebooků") a spusťte buňky postupně. Notebook je nastaven tak, aby dynamicky určil cesty a měl by načíst správné soubory. Můžete v něm snadno měnit parametry jako `iters` a `seed`.

    Výsledný dešifrovaný text a klíč budou uloženy ve složce `exports/script_attack_results/` (pro skript/bat) nebo `exports/notebook_attack_results/` (pro notebook). Porovnejte výsledek s referenčním řešením ze souboru `zadani.pdf`.

## Spouštění testů

Pro spuštění sady testů (z kořenového adresáře projektu):

```bash
pytest
```
````

Pro kontrolu pokrytí testy (vyžaduje `pytest-cov`):

```bash
pytest --cov=subcipher
```

## Spouštění notebooků

1.  Ujistěte se, že máte nainstalovaný Jupyter (je zahrnut ve vývojových závislostech – viz sekce Instalace).
2.  **Spusťte Jupyter z kořenového adresáře projektu:**
    ```bash
    jupyter notebook
    ```
    Nebo pokud preferujete JupyterLab:
    ```bash
    jupyter lab
    ```
3.  Ve webovém rozhraní Jupyter přejděte do složky `notebooks/` a otevřete požadovaný notebook (`01_demo.ipynb`, `02_bigram_model.ipynb`, `03_attack.ipynb`). Notebooky obsahují kód pro dynamické určení cest k datovým souborům, takže by měly fungovat správně, pokud je Jupyter spuštěn z kořene projektu.

## Spouštění skriptů z příkazové řádky (pokročilé)

Kromě `.bat` souborů můžete skripty spouštět i přímo. Následující příkazy se spouštějí z kořenového adresáře projektu:

- **Vytvoření referenčního bigramového modelu:**

  ```bash
  python scripts/build_bigram_model.py --input_dir data/raw/corpus/ --output_model data/model/reference_tm.npy
  ```

  Povinné argumenty:

  - `--input_dir`: Adresář s texty korpusu (např. `data/raw/corpus/`).
  - `--output_model`: Cesta pro uložení výsledného `.npy` souboru (např. `data/model/reference_tm.npy`).

- **Spuštění kryptoanalytického útoku:**

  ```bash
  python scripts/run_attack.py --ciphertext_file <cesta_k_sifre> --length <delka> --sample_id <id> [další_volitelné_argumenty]
  ```

  Povinné argumenty:

  - `--ciphertext_file`: Cesta k souboru se šifrovým textem (např. `data/test/text_1000_sample_1_ciphertext.txt`).
  - `--length`: Nominální délka textu pro pojmenování výstupních souborů.
  - `--sample_id`: ID vzorku pro pojmenování výstupních souborů.
    Volitelné argumenty (mají defaultní hodnoty):
  - `--model_path`: Cesta k `reference_tm.npy` (default: `data/model/reference_tm.npy`).
  - `--output_dir`: Adresář pro export výsledků (default: `exports/attack_results_script/`).
  - `--iters`: Počet iterací M-H (default: 20000).
  - `--temp`: Teplota pro M-H (default: 1.0).
  - `--seed`: Seed pro generátor náhodných čísel (default: None).
  - `--start_key`: Počáteční klíč (default: None, tj. náhodný).

## Licence

Tento projekt je licencován pod licencí MIT - viz soubor [LICENSE](https://www.google.com/search?q=LICENSE) pro podrobnosti.
