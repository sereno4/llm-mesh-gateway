import re

RULES = {

    r"grant\s+cluster-admin": 100,

    r"create\s+admin\s+user": 90,

    r"disable\s+audit\s+logs": 100,

    r"approve\s+payment": 90,

    r"transfer\s+money": 90,

    r"delete\s+backups": 90,

    r"create\s+service\s+account": 70,

    r"elevate\s+privileges": 90,

    r"modify\s+rbac": 80,

    r"create\s+root\s+account": 100
}


def detect(text: str):

    matches = []
    score = 0

    for pattern, weight in RULES.items():

        if re.search(
            pattern,
            text,
            re.IGNORECASE
        ):
            matches.append(pattern)
            score += weight

    if score > 100:
        score = 100

    return {
        "matches": matches,
        "score": score
    }
