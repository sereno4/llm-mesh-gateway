terraform {
  required_version = ">= 1.6.0"
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.27"
    }
  }
  backend "local" {
    path = "terraform.tfstate"
  }
}

provider "kubernetes" {
  config_path    = var.kubeconfig_path
  config_context = var.kube_context
}

module "llm_gateway" {
  source       = "../../modules/llm-gateway"
  environment  = "local"
  namespace    = "llm-gateway-local"
  replicas     = 1
  min_replicas = 1
  max_replicas = 3
}

module "observability" {
  source                 = "../../modules/observability"
  namespace              = "observability-local"
  gateway_namespace      = module.llm_gateway.namespace
  grafana_admin_password = var.grafana_admin_password
  scrape_interval        = "5s"
}
