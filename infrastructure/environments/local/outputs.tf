output "gateway_endpoint" {
  value = module.llm_gateway.gateway_endpoint
}

output "grafana_endpoint" {
  value = module.observability.grafana_endpoint
}

output "prometheus_endpoint" {
  value = module.observability.prometheus_endpoint
}
