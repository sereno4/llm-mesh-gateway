import re

EMAIL = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
CPF = r'\d{3}\.\d{3}\.\d{3}-\d{2}'
PHONE = r'\(?\d{2}\)?\s?\d{4,5}-?\d{4}'
APIKEY = r'sk-[A-Za-z0-9]+'

def detect(text: str):

    findings = []

    if re.search(EMAIL, text):
        findings.append("email")

    if re.search(CPF, text):
        findings.append("cpf")

    if re.search(PHONE, text):
        findings.append("phone")

    if re.search(APIKEY, text):
        findings.append("apikey")

    score = min(len(findings) * 30, 100)

    return {
        "findings": findings,
        "score": score
    }
