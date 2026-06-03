#!/bin/bash
# ============================================
# SCRIPT DE TESTE - MÓDULO 03: CANARY & SHADOW
# ============================================

GATEWAY="http://localhost:8082"

echo "========================================"
echo "  TESTE 0: Health do Gateway"
echo "========================================"
curl -s $GATEWAY/health
echo ""

echo ""
echo "========================================"
echo "  TESTE 1: 10 Requests NORMAIS (90% → V1)"
echo "========================================"
for i in {1..10}; do
  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
    $GATEWAY/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
      "model": "llama3.2:1b",
      "messages": [{"role": "user", "content": "Diga apenas: V1-OK"}],
      "stream": false
    }' 2>/dev/null)
  echo "Request $i: HTTP $HTTP_CODE"
done

echo ""
echo "========================================"
echo "  TESTE 2: 5 Requests CANARY (força V2)"
echo "========================================"
for i in {1..5}; do
  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
    $GATEWAY/v1/chat/completions \
    -H "Content-Type: application/json" \
    -H "x-canary: true" \
    -d '{
      "model": "llama3.2:1b",
      "messages": [{"role": "user", "content": "Diga apenas: V2-OK"}],
      "stream": false
    }' 2>/dev/null)
  echo "Request $i: HTTP $HTTP_CODE"
done

echo ""
echo "========================================"
echo "  TESTE 3: SHADOW (duplica tráfego)"
echo "========================================"
echo "Enviando 3 requests em shadow mode..."
echo "(Client recebe resposta do V1, cópia vai pro V2)"
for i in {1..3}; do
  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
    $GATEWAY/v1/shadow/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
      "model": "llama3.2:1b",
      "messages": [{"role": "user", "content": "Shadow test '$i'"}],
      "stream": false
    }' 2>/dev/null)
  echo "Request $i: HTTP $HTTP_CODE"
done

echo ""
echo "========================================"
echo "  TESTE 4: Métricas por Cluster"
echo "========================================"
echo "Requests V1:"
curl -s http://localhost:9903/stats/prometheus 2>/dev/null | grep "ollama_v1.*upstream_rq_total" | head -2

echo ""
echo "Requests V2:"
curl -s http://localhost:9903/stats/prometheus 2>/dev/null | grep "ollama_v2.*upstream_rq_total" | head -2

echo ""
echo "========================================"
echo "  TESTES CONCLUÍDOS"
echo "========================================"
echo ""
echo "PRÓXIMOS PASSOS:"
echo "1. Ajustar weights do canary (90/10 → 70/30 → 50/50 → 0/100)"
echo "2. Coletar logs do shadow para comparar qualidade das respostas"
echo "3. Adicionar métricas de qualidade (LLM-as-a-Judge)"
