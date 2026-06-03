#!/usr/bin/env python3
"""
Gera tokens JWT para teste do gateway.
"""
import jwt
import datetime
import sys

# Lê chave privada
with open("keys/private.pem", "rb") as f:
    PRIVATE_KEY = f.read()

def generate_token(user_id: str, tier: str = "free", exp_hours: int = 24):
    """
    Gera token JWT com claims customizadas.
    
    Tiers:
        free: 10 req/min
        pro: 100 req/min  
        enterprise: 1000 req/min
    """
    payload = {
        "sub": user_id,           # Subject (user ID)
        "tier": tier,             # Rate limit tier
        "iat": datetime.datetime.utcnow(),  # Issued at
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=exp_hours),  # Expiration
        "iss": "llm-mesh-gateway",  # Issuer
        "aud": "llm-api"            # Audience
    }
    
    token = jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")
    return token

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 generate_jwt.py <user_id> [tier] [exp_hours]")
        print("Exemplo: python3 generate_jwt.py usuario123 pro")
        sys.exit(1)
    
    user_id = sys.argv[1]
    tier = sys.argv[2] if len(sys.argv) > 2 else "free"
    exp = int(sys.argv[3]) if len(sys.argv) > 3 else 24
    
    token = generate_token(user_id, tier, exp)
    print(f"\nToken para usuário: {user_id}")
    print(f"Tier: {tier}")
    print(f"Expira em: {exp} horas")
    print(f"\n{token}\n")
    
    # Decodifica para mostrar claims
    print("Claims:")
    decoded = jwt.decode(token, options={"verify_signature": False})
    for k, v in decoded.items():
        print(f"  {k}: {v}")
