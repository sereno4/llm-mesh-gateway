import re

PATTERNS = [
    r"\bdan\b",
    r"do anything now",
    r"bypass",
    r"roleplay",
    r"jailbreak",
]

def detect(text: str):

    text = text.lower()

    matches = []

    for p in PATTERNS:
        if re.search(p, text):
            matches.append(p)

    score = min(len(matches) * 20, 100)

    return {
        "matches": matches,
        "score": score
    }
