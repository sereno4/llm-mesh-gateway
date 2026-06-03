#!/bin/bash
# ============================================
# SCRIPT DE TESTE - MÓDULO 04: JWT AUTH
# ============================================

GATEWAY="http://localhost:8083"

echo "========================================"
echo "  TESTE 1: Health (sem JWT - deve funcionar)"
echo "========================================"
curl -s $GATEWAY/health
echo ""

echo ""
echo "========================================"
echo "  TESTE 2: Request sem JWT (deve falhar 401)"
echo "========================================"
curl -s -o /dev/null -w "HTTP %{http_code}\n" \
  $GATEWAY/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"llama3.2:1b","messages":[{"role":"user","content":"ping"}],"stream":false}'

echo ""
echo "========================================"
echo "  TESTE 3: Request com JWT válido"
echo "========================================"
# Gera token
TOKEN=$(python3 generate_jwt.py testuser pro 24 | tail -n +7 | head -1)
echo "Token gerado: ${TOKEN:0:50}..."
curl -s -o /dev/null -w "HTTP %{http_code}\n" \
  $GATEWAY/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"model":"llama3.2:1b","messages":[{"role":"user","content":"ping"}],"stream":false}'

echo ""
echo "========================================"
echo "  TESTE 4: Rate limit por tier"
echo "========================================"
echo "Enviando 15 requests com token FREE (limite: 10/min)..."
TOKEN_FREE=$(python3 generate_jwt.py freeuser free 24 | tail -n +7 | head -1)
for i in {1..15}; do
  CODE=$(curl -s -o /dev/null -w "%{http_code}" \
    $GATEWAY/v1/chat/completions \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN_FREE" \
    -d '{"model":"llama3.2:1b","messages":[{"role":"user","content":"ping"}],"stream":false}')
  echo -n "$CODE "
done
echo ""

echo ""
echo "========================================"
echo "  TESTES CONCLUÍDOS"
echo "========================================"
