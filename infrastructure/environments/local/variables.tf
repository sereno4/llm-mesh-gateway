variable "kubeconfig_path" {
  type    = string
  default = "~/.kube/config"
}

variable "kube_context" {
  type    = string
  default = "kind-ai-governance"
}

variable "grafana_admin_password" {
  type      = string
  sensitive = true
  default   = "admin"
}
