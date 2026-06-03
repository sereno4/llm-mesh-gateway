variable "namespace" {
  type    = string
  default = "observability"
}

variable "gateway_namespace" {
  type    = string
  default = "llm-gateway"
}

variable "prometheus_version" {
  type    = string
  default = "latest"
}

variable "grafana_version" {
  type    = string
  default = "latest"
}

variable "grafana_admin_password" {
  type      = string
  sensitive = true
}

variable "scrape_interval" {
  type    = string
  default = "15s"
}
