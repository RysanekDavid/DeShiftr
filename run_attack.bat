@echo off
echo Spoustim utok...

python scripts/run_attack.py ^
    --ciphertext_file data/test/text_1000_sample_1_ciphertext.txt ^
    --model_path data/model/reference_tm.npy ^
    --output_dir exports/script_attack_results ^
    --length 1000 ^
    --sample_id 1 ^
    --iters 20000 ^
    --temp 1.0 ^
    --seed 112000

echo.
echo Utok dokoncen. Vystupy jsou ve slozce exports/script_attack_results
pause