import json
import re

# ---------- 1. Load domain vocabulary ----------
with open("data.json", "r", encoding="utf-8") as f:
    DOMAIN_DICT = json.load(f)

# ---------- 2. Roman spelling normalizer ----------
def normalize_roman(word: str) -> str:
    word = word.lower().strip()

    # collapse repeated characters (aaa → a, jj → j)
    word = re.sub(r'(.)\1+', r'\1', word)

    # normalize aspirated consonants
    replacements = {
        "th": "t",
        "dh": "d",
        "ph": "p",
        "bh": "b",
        "gh": "g",
        "kh": "k",
        "jh": "j",
        "chh": "ch"
    }

    for k, v in replacements.items():
        word = word.replace(k, v)

    # normalize long vowels
    word = re.sub(r'aa+', 'a', word)
    word = re.sub(r'ii+', 'i', word)
    word = re.sub(r'oo+', 'o', word)
    word = re.sub(r'ee+', 'e', word)
    word = re.sub(r'uu+', 'u', word)

    # keep only alphanumeric
    word = re.sub(r'[^a-z0-9]', '', word)

    return word

# ---------- 3. Normalize one token ----------
def normalize_token(token: str) -> str:
    token = normalize_roman(token)
    return DOMAIN_DICT.get(token, token)

# ---------- 4. Normalize full query (MULTI-WORD) ----------
def normalize_query(query: str) -> str:
    tokens = query.split()
    normalized_tokens = [normalize_token(t) for t in tokens]
    return " ".join(normalized_tokens)

# ---------- 5. Demo ----------
if __name__ == "__main__":
    while True:
        query = input("\nSearch query (or 'exit'): ")
        if query.lower() == "exit":
            break

        result = normalize_query(query)
        print("Normalized output:", result)
