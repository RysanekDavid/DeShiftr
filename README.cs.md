[English version](README.md)

# Nástroje pro substituční šifru

Tento projekt je sada nástrojů pro práci se substitučními šiframi. Zahrnuje funkce pro šifrování, dešifrování, statistickou analýzu a kryptoanalýzu pomocí metod, jako je Metropolis-Hastings.

## Rychlý start

Tato sekce poskytuje minimální sadu příkazů pro rychlý začátek.

1.  **Klonování a instalace:**

    ```bash
    git clone https://github.com/RysanekDavid/DeShiftr.git
    cd DeShiftr
    pip install -e .[dev]
    ```

2.  **Sestavení bigramového modelu:**
    Budete potřebovat textový soubor korpusu (např. velký text v očekávaném jazyce šifrovaného textu). Pro tento příklad předpokládejme, že máte svůj korpus v `data/raw/krakatit.txt`.

    ```bash
    python scripts/build_bigram_model.py --input_file data/raw/krakatit.txt --output_model data/model/bigram_model.npy
    ```

    _(Poznámka: Pokud `build_bigram_model.py` očekává adresář textových souborů, můžete použít `--input_dir data/raw/corpus/` a umístit tam své soubory korpusu.)_

3.  **Spuštění útoku:**
    Tento příkaz používá model sestavený v předchozím kroku k pokusu o dešifrování vzorového šifrovaného textu.
    ```bash
    python scripts/run_attack.py --input_file data/test/text_250_sample_1_ciphertext.txt --model_path data/model/bigram_model.npy --output_file exports/solved_text_250_sample_1.txt
    ```
    Dešifrovaný text byste měli najít v `exports/solved_text_250_sample_1.txt`.

## Cíle projektu

- Poskytnout modulární knihovnu (`subcipher`) pro operace se substituční šifrou.
- Demonstrovat použití prostřednictvím Jupyter notebooků (`notebooks/`).
- Zajistit kvalitu kódu pomocí testů (`tests/`) a pre-commit hooků.
- Nabídnout skripty pro dávkové zpracování (`scripts/`).

## Začínáme

### Předpoklady

- Python 3.8+
- Pip

### Instalace

1. Klonujte repozitář:
   ```bash
   git clone https://github.com/RysanekDavid/DeShiftr.git
   cd DeShiftr
   ```
2. Nainstalujte balíček a jeho vývojové závislosti:
   ```bash
   pip install -e .[dev]
   ```
3. Nastavte pre-commit hooky (volitelné, ale doporučené):
   ```bash
   pre-commit install
   ```

## Spouštění testů

Pro spuštění sady testů:

```bash
pytest
```

Můžete také zkontrolovat pokrytí testy (ujistěte se, že máte nainstalovaný `pytest-cov`):

```bash
pytest --cov=subcipher
```

## Spouštění notebooků

1. Ujistěte se, že máte nainstalovaný Jupyter (je zahrnut ve vývojových závislostech).
2. Spusťte Jupyter server:
   ```bash
   jupyter notebook
   ```
3. Otevřete notebooky umístěné v adresáři `notebooks/` prostřednictvím rozhraní Jupyter ve vašem prohlížeči.

## Spouštění skriptů

Adresář `scripts/` obsahuje skripty pro dávkové operace. Například:

```bash
python scripts/run_attack.py --input data/raw/some_cipher_text.txt --output exports/solved_cipher.txt
python scripts/build_bigram_model.py --input_dir data/raw/corpus/ --output_model data/model/bigram_matrix.npy
```

(Poznámka: Toto jsou příklady příkazů; skutečné názvy skriptů a argumenty se mohou lišit.)

## Struktura projektu

(Zde může být přidán stručný přehled hlavních adresářů a jejich účelu, podobně jako v původním požadavku.)

## Přispívání

(Podrobnosti o tom, jak přispět, pokud je to relevantní.)

## Licence

Tento projekt je licencován pod licencí MIT - viz soubor [LICENSE](LICENSE) pro podrobnosti.
