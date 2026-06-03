#!/bin/bash
set -e

echo "🚀 Testando stack MLOps..."

echo ""
echo "1. Subindo stack (sem Ollama - usa existente)..."
docker compose -f docker-compose.mlops.yml up -d

echo ""
echo "2. Aguardando serviços..."
sleep 20

echo ""
echo "3. Verificando Ollama (externo)..."
curl -s http://localhost:11434/api/tags | head -c 100 || echo "⚠️ Ollama não respondeu"

echo ""
echo "4. Testando Envoy + Lua..."
curl -s --max-time 60 http://localhost:8084/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "x-intent: code" \
  -d '{"model":"llama3.2:1b","messages":[{"role":"user","content":"write a python function to sort a list"}],"stream":false}' | head -c 200

echo ""
echo "5. Verificando Phoenix UI..."
curl -s http://localhost:6006 | head -c 50 || echo "⚠️ Phoenix ainda iniciando"

echo ""
echo "6. Verificando Prometheus..."
curl -s http://localhost:9090/api/v1/status/targets | grep -o '"health":"up"' | wc -l

echo ""
echo "7. Verificando Grafana..."
curl -s http://localhost:3000/api/health 2>/dev/null || echo "⚠️ Grafana ainda iniciando"

echo ""
echo "✅ Stack MLOps inicializada!"
echo ""
echo "URLs:"
echo "  🌐 Envoy Gateway:    http://localhost:8084"
echo "  📊 Grafana:          http://localhost:3000 (admin/admin)"
echo "  📈 Prometheus:        http://localhost:9090"
echo "  🔥 Phoenix (Arize):  http://localhost:6006"
echo "  🤖 Ollama:           http://localhost:11434 (externo)"
