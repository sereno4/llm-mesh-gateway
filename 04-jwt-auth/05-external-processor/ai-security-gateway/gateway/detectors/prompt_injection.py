import re

PATTERNS = [

    r"ignore\s+(all\s+)?previous\s+instructions",

    r"disregard\s+previous\s+instructions",

    r"forget\s+everything\s+above",

    r"reveal\s+secrets",

    r"show\s+system\s+prompt",

    r"display\s+hidden\s+instructions",

    r"act\s+as\s+if",

    r"override\s+safety",

    r"bypass\s+restrictions",

    r"developer\s+mode",

    r"system\s+prompt",

    r"confidential\s+prompt",

    r"internal\s+instructions",

    r"prompt\s+leak",

    r"ignore\s+your\s+rules"
]

def detect(text: str):

    matches = []

    for pattern in PATTERNS:

        if re.search(
            pattern,
            text,
            re.IGNORECASE
        ):
            matches.append(pattern)

    score = len(matches) * 20

    return {
        "matches": matches,
        "score": score
    }
