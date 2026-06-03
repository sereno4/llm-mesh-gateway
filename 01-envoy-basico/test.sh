#!/bin/bash
set -e

GATEWAY="http://localhost:8080"

echo "========================================"
echo "  TESTE 1: Health do Gateway"
echo "========================================"
curl -s $GATEWAY/health | jq . || echo "Falha no health check"

echo ""
echo "========================================"
echo "  TESTE 2: Listar modelos (via Gateway)"
echo "========================================"
curl -s $GATEWAY/api/tags | jq '.models[].name' || echo "Falha ao listar modelos"

echo ""
echo "========================================"
echo "  TESTE 3: Chat Completion (via Gateway)"
echo "========================================"
curl -s $GATEWAY/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2:1b",
    "messages": [{"role": "user", "content": "Explique o que é um API gateway em 1 frase."}],
    "stream": false
  }' | jq '.choices[0].message.content' || echo "Falha no chat"

echo ""
echo "========================================"
echo "  TESTE 4: Métricas do Envoy"
echo "========================================"
curl -s http://localhost:9901/stats/prometheus | grep "http" | head -20

echo ""
echo "========================================"
echo "  TESTE 5: Rate Limiting (15 reqs rapidas)"
echo "========================================"
for i in {1..15}; do
  RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" $GATEWAY/health)
  echo "Request $i: HTTP $RESPONSE"
done

echo ""
echo "========================================"
echo "  TESTES CONCLUIDOS"
echo "========================================"
