LLM Mesh Gateway Platform

[![License](https://img.shields.io/badge/license-MIT-green)]()
[![Python](https://img.shields.io/badge/python-3.12-blue)]()
[![Envoy](https://img.shields.io/badge/Envoy-proxy-326CE5)]()
[![OpenTofu](https://img.shields.io/badge/OpenTofu-IaC-7B56CC)]()

Plataforma completa para resiliência, observabilidade, governança e segurança de aplicações de IA Generativa em Kubernetes.

Visão Geral

Este projeto demonstra a construção de um AI Gateway corporativo baseado em Envoy Proxy, capaz de:

Realizar roteamento inteligente para múltiplos modelos
Implementar fallback automático entre provedores de IA
Executar canary releases de modelos
Aplicar autenticação JWT
Inspecionar prompts em tempo real
Detectar abuso de ferramentas
Detectar exfiltração de dados
Aplicar políticas OPA/Rego
Exportar métricas para Prometheus
Visualizar indicadores em Grafana
Gerar traces distribuídos com OpenTelemetry
Monitorar interações LLM no Arize Phoenix
Provisionar infraestrutura via OpenTofu
Arquitetura


llm-mesh-gateway/
│
├── 01-envoy-basico/
├── 02-fallback-externo/
├── 03-canary/
├── 04-jwt-auth/
│
├── infrastructure/
│   ├── environments/
│   ├── modules/
│   └── configs/
│
├── docs/
│   ├── architecture/
│   ├── screenshots/
│   ├── dashboards/
│   └── diagrams/
│
├── README.md
├── LICENSE
└── .gitignore


Observability Layer

OpenTelemetry
Prometheus
Grafana
Phoenix (Arize)
Technology Stack

Backend

Python
FastAPI

Observability

OpenTelemetry
Prometheus
Grafana
Phoenix (Arize)

Infrastructure

Kubernetes
OpenTofu
Envoy Proxy

Security

Risk Scoring
Policy Enforcement
Tool Abuse Detection
Data Exfiltration Detection
Use Cases
Enterprise AI Platforms
Internal Copilots
Autonomous Agents
Multi-LLM Gateways
Regulated Environments
AI Governance Platforms
Achievements
Infrastructure validated with OpenTofu
End-to-end observability
Distributed tracing
Real-time risk monitoring
Automated threat blocking
Production-ready cloud-native architecture
Roadmap
Multi-Provider Failover
Circuit Breaker
Adaptive Routing
Cost Tracking
AI FinOps
Runtime Security Analytics
Governance Dashboard

License

MIT License
