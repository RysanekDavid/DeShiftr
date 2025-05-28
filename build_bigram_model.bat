@echo off
echo Vytvarim referencni bigramovy model...

python scripts/build_bigram_model.py ^
    --input_dir data/raw/corpus ^
    --output_model data/model/reference_tm.npy

echo.
echo Tvorba modelu dokoncena.
pause