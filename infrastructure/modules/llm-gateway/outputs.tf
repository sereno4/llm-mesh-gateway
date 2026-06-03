output "namespace" {
  description = "Namespace criado para o LLM Gateway"
  value       = kubernetes_namespace.llm_gateway.metadata[0].name
}

output "gateway_service_name" {
  description = "Nome do service do Envoy Gateway"
  value       = kubernetes_service.envoy_gateway.metadata[0].name
}

output "gateway_endpoint" {
  description = "Endpoint interno do gateway"
  value       = "${kubernetes_service.envoy_gateway.metadata[0].name}.${kubernetes_namespace.llm_gateway.metadata[0].name}.svc.cluster.local:8080"
}
