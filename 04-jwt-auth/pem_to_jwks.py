#!/usr/bin/env python3
import json
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

# Ler chave pública PEM
with open("keys/public.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read(), backend=default_backend())

# Extrair números
public_numbers = public_key.public_numbers()
n = public_numbers.n
e = public_numbers.e

# Converter para base64url
def base64url_encode(value):
    if isinstance(value, int):
        value = value.to_bytes((value.bit_length() + 7) // 8, byteorder='big')
    return base64.urlsafe_b64encode(value).rstrip(b'=').decode('ascii')

# Criar JWKS
jwks = {
    "keys": [
        {
            "kty": "RSA",
            "alg": "RS256",
            "use": "sig",
            "kid": "llm-key-1",
            "n": base64url_encode(n),
            "e": base64url_encode(e)
        }
    ]
}

# Salvar
with open("keys/jwks.json", "w") as f:
    json.dump(jwks, f, indent=2)

print("JWKS criado em keys/jwks.json")
print(json.dumps(jwks, indent=2))
