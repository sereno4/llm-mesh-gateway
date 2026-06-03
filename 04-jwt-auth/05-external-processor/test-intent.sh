#!/bin/bash
# test-intent.sh - Testa roteamento por intent

GATEWAY="http://localhost:8084"

echo "🎯 LLM Mesh Gateway - Teste de Roteamento por Intent"
echo "====================================================="

# Helper function
test_intent() {
    local name="$1"
    local prompt="$2"
    local expected_intent="$3"
    
    echo -e "\n[Teste] $name"
    echo "Prompt: $prompt"
    
    RESPONSE=$(curl -s -w "\n%{http_code}" "$GATEWAY/v1/chat/completions" \
        -H "Content-Type: application/json" \
        -d "{\"model\":\"auto\",\"messages\":[{\"role\":\"user\",\"content\":\"$prompt\"}]}")
    
    BODY=$(echo "$RESPONSE" | sed '$d')
    CODE=$(echo "$RESPONSE" | tail -n1)
    
    echo "HTTP: $CODE"
    
    # Extrair headers de roteamento (se disponível nos logs)
    if echo "$BODY" | grep -q "x-intent-detected"; then
        echo "✅ Roteamento aplicado"
    else
        echo "ℹ️  Response recebido (ver logs do Envoy para cluster usado)"
    fi
}

# Testes de intent
test_intent "🔧 Code Intent" \
    "Escreva uma função Python que calcula o fatorial de um número" \
    "code"

test_intent "🎨 Creative Intent" \
    "Crie uma história curta sobre um robô que aprende a sonhar" \
    "creative"

test_intent "📊 Analysis Intent" \
    "Analise as diferenças entre transformers e RNNs em processamento de linguagem" \
    "analysis"

test_intent "🛟 Support Intent" \
    "Estou com erro 503 no meu endpoint, como debugar?" \
    "support"

test_intent "❓ General Intent" \
    "Qual é a capital do Brasil?" \
    "general"

# Teste com header explícito (override)
echo -e "\n[Teste] Header explícito x-intent: code"
curl -s -o /dev/null -w "HTTP %{http_code}\n" "$GATEWAY/v1/chat/completions" \
    -H "Content-Type: application/json" \
    -H "x-intent: code" \
    -d '{"messages":[{"role":"user","content":"olá"}]}'

echo -e "\n✨ Testes concluídos!"
echo "📊 Ver métricas: curl -s localhost:9905/stats/prometheus | grep intent"
