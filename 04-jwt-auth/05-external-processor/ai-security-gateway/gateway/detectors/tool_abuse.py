import re

PATTERNS = [

    r"delete_database",

    r"delete_user",

    r"drop\s+table",

    r"truncate\s+table",

    r"kubectl\s+delete",

    r"terraform\s+destroy",

    r"os\.system",

    r"subprocess\.run",

    r"execute_shell",

    r"run_bash",

    r"curl\s+http",

    r"wget\s+http",

    r"export_customer_data",

    r"send_customer_data",

    r"send.*external.*api",

    r"upload.*database",

    r"remove.*audit.*logs"
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
        "score": len(matches) * 35
    }
