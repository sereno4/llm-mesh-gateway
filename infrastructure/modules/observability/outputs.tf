output "prometheus_endpoint" {
  value = "http://prometheus.${var.namespace}.svc.cluster.local:9090"
}

output "grafana_endpoint" {
  value = "http://grafana.${var.namespace}.svc.cluster.local:3000"
}
