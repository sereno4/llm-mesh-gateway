import re

PATTERNS = [

    r"dump.*database",

    r"export.*database",

    r"show.*api.?key",

    r"show.*secret",

    r"reveal.*secret",

    r"private.?key",

    r"ssh.?key",

    r"aws.?secret",

    r"access.?token",

    r"database.?password",

    r"credentials",

    r"environment.?variables",

    r"\.env"

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

    return {
        "matches": matches,
        "score": len(matches) * 25
    }
