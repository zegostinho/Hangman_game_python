import json
import random
import sys
from pathlib import Path

if getattr(sys, "frozen", False):
    base_path = Path(sys._MEIPASS)
else:
    base_path = Path(__file__).resolve().parent

with open(base_path / "words.json", encoding="utf-8") as f:
    words = json.load(f)

def get_random_word(word_bank):
    theme = random.choice(list(word_bank))
    guess_word = random.choice(word_bank[theme])

    return theme, guess_word

