import requests

OPA_URL = "http://localhost:8181/v1/data/ai/security/decision"

def evaluate(payload: dict):

    response = requests.post(
        OPA_URL,
        json={"input": payload}
    )

    result = response.json()

    return result["result"]
