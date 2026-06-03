#!/bin/bash
set -e

echo "=== 1. Backup do arquivo correto ==="
cp envoy-observability.yaml envoy-observability.yaml.bak

echo ""
echo "=== 2. Corrigindo upstream_protocol_options → explicit_http_config ==="
sed -i 's/upstream_protocol_options:/explicit_http_config:/g' envoy-observability.yaml

echo ""
echo "=== 3. Validando a correção ==="
grep -n -A5 "explicit_http_config" envoy-observability.yaml

echo ""
echo "=== 4. Verificando Docker ==="
if ! docker ps &>/dev/null; then
    echo "Docker não está rodando. Iniciando..."
    sudo service docker start || sudo dockerd > /tmp/dockerd.log 2>&1 &
    sleep 5
fi

echo ""
echo "=== 5. Subindo stack MLOps ==="
docker compose -f docker-compose.mlops.yml down 2>/dev/null || true
docker compose -f docker-compose.mlops.yml up -d

echo ""
echo "=== 6. Aguardando 10s ==="
sleep 10

echo ""
echo "=== 7. Verificando se Envoy subiu ==="
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep envoy

echo ""
echo "=== 8. Logs do Envoy (últimas 20 linhas) ==="
docker logs envoy-llm-mlops --tail 20 2>&1

echo ""
echo "=== 9. Teste na porta 8084 ==="
curl -s --max-time 10 http://localhost:8084/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "x-intent: code" \
  -d '{"model":"llama3.2:1b","messages":[{"role":"user","content":"hello"}],"stream":false}' | head -c 300
