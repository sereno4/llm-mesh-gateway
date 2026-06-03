#!/usr/bin/env python3
"""
LLM Mesh Gateway - Client Inteligente com Fallback
Demonstra o padrão de mercado: client detecta falha e re-tenta com cluster alternativo
"""

import sys
import json
import urllib.request
import urllib.error
import os

GATEWAY = os.getenv("LLM_GATEWAY", "http://localhost:8081")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "SUA_CHAVE_AQUI")

def ask_ollama(prompt: str) -> dict:
    """Tenta Ollama local (cluster padrão, sem header)"""
    req = urllib.request.Request(
        f"{GATEWAY}/v1/chat/completions",
        data=json.dumps({
            "model": "llama3.2:1b",
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())

def ask_groq(prompt: str) -> dict:
    """Fallback para Groq (header x-target-cluster: groq)"""
    req = urllib.request.Request(
        f"{GATEWAY}/v1/chat/completions",
        data=json.dumps({
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }).encode(),
        headers={
            "Content-Type": "application/json",
            "x-target-cluster": "groq",
            "Authorization": f"Bearer {GROQ_API_KEY}"
        },
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())

def smart_chat(prompt: str) -> str:
    """
    Padrão de fallback inteligente:
    1. Tenta Ollama local (custo zero, latência baixa)
    2. Se falhar (503, timeout, connection refused) → Groq
    3. Se Groq falhar → erro controlado
    """
    print(f"[FALLBACK] Prompt: {prompt[:50]}...")
    
    # TENTATIVA 1: Ollama local
    try:
        print("[FALLBACK] → Tentando Ollama local...")
        result = ask_ollama(prompt)
        content = result["choices"][0]["message"]["content"]
        print(f"[FALLBACK] ✅ Ollama respondeu ({result.get('model', 'unknown')})")
        return f"[LOCAL] {content}"
    except urllib.error.HTTPError as e:
        if e.code == 503:
            print(f"[FALLBACK] ⚠️ Ollama indisponível (503)")
        else:
            print(f"[FALLBACK] ⚠️ Ollama erro HTTP {e.code}")
    except urllib.error.URLError as e:
        print(f"[FALLBACK] ⚠️ Ollama connection error: {e.reason}")
    except Exception as e:
        print(f"[FALLBACK] ⚠️ Ollama erro: {e}")

    # TENTATIVA 2: Groq (fallback)
    try:
        print("[FALLBACK] → Fallback para Groq...")
        result = ask_groq(prompt)
        content = result["choices"][0]["message"]["content"]
        print(f"[FALLBACK] ✅ Groq respondeu ({result.get('model', 'unknown')})")
        return f"[FALLBACK] {content}"
    except Exception as e:
        print(f"[FALLBACK] ❌ Groq também falhou: {e}")
        return "[ERRO] Todos os clusters indisponíveis. Tente novamente mais tarde."

if __name__ == "__main__":
    if len(sys.argv) < 2:
        prompt = "Explique o que é um fallback em 1 frase"
    else:
        prompt = " ".join(sys.argv[1:])
    
    resposta = smart_chat(prompt)
    print(f"\n{'='*60}")
    print(resposta)
    print(f"{'='*60}")
