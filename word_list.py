import json
import random

with open("words.json", encoding="utf-8") as f:
    words = json.load(f)

def get_random_word(word_bank):
    theme = random.choice(list(word_bank))
    guess_word = random.choice(word_bank[theme])

    return theme, guess_word

