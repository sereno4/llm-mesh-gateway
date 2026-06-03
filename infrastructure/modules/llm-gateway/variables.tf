variable "namespace" {
  description = "Kubernetes namespace para o LLM Gateway"
  type        = string
  default     = "llm-gateway"
}

variable "environment" {
  description = "Ambiente de deploy (local, staging, production)"
  type        = string
  validation {
    condition     = contains(["local", "staging", "production"], var.environment)
    error_message = "Environment deve ser local, staging ou production."
  }
}

variable "envoy_version" {
  description = "Versão da imagem do Envoy"
  type        = string
  default     = "v1.30-latest"
}

variable "replicas" {
  description = "Número de réplicas do gateway"
  type        = number
  default     = 2
}

variable "min_replicas" {
  description = "Mínimo de réplicas para o HPA"
  type        = number
  default     = 1
}

variable "max_replicas" {
  description = "Máximo de réplicas para o HPA"
  type        = number
  default     = 10
}

variable "cpu_request" {
  type    = string
  default = "100m"
}

variable "cpu_limit" {
  type    = string
  default = "500m"
}

variable "memory_request" {
  type    = string
  default = "128Mi"
}

variable "memory_limit" {
  type    = string
  default = "512Mi"
}
