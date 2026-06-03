# LLM Gateway — Kubernetes resources
resource "kubernetes_namespace" "llm_gateway" {
  metadata {
    name = var.namespace
    labels = {
      "app.kubernetes.io/managed-by" = "opentofu"
      "env"                          = var.environment
      "component"                    = "llm-gateway"
    }
  }
}

resource "kubernetes_deployment" "envoy_gateway" {
  metadata {
    name      = "envoy-gateway"
    namespace = kubernetes_namespace.llm_gateway.metadata[0].name
    labels = {
      "app"     = "envoy-gateway"
      "version" = var.envoy_version
    }
  }
  spec {
    replicas = var.replicas
    selector {
      match_labels = { "app" = "envoy-gateway" }
    }
    template {
      metadata {
        labels = { "app" = "envoy-gateway" }
        annotations = {
          "prometheus.io/scrape" = "true"
          "prometheus.io/port"   = "9901"
          "prometheus.io/path"   = "/stats/prometheus"
        }
      }
      spec {
        container {
          name  = "envoy"
          image = "envoyproxy/envoy:${var.envoy_version}"
          args  = ["envoy", "-c", "/etc/envoy/envoy.yaml", "--log-level", "info"]
          port {
            name           = "gateway"
            container_port = 8080
          }
          port {
            name           = "admin"
            container_port = 9901
          }
          volume_mount {
            name       = "envoy-config"
            mount_path = "/etc/envoy"
            read_only  = true
          }
          resources {
            requests = {
              cpu    = var.cpu_request
              memory = var.memory_request
            }
            limits = {
              cpu    = var.cpu_limit
              memory = var.memory_limit
            }
          }
          liveness_probe {
            http_get {
              path = "/ready"
              port = 9901
            }
            initial_delay_seconds = 10
            period_seconds        = 15
          }
        }
        volume {
          name = "envoy-config"
          config_map {
            name = kubernetes_config_map.envoy_config.metadata[0].name
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "envoy_gateway" {
  metadata {
    name      = "envoy-gateway"
    namespace = kubernetes_namespace.llm_gateway.metadata[0].name
  }
  spec {
    selector = { "app" = "envoy-gateway" }
    port {
      name        = "gateway"
      port        = 8080
      target_port = 8080
    }
    port {
      name        = "admin"
      port        = 9901
      target_port = 9901
    }
    type = "ClusterIP"
  }
}

resource "kubernetes_config_map" "envoy_config" {
  metadata {
    name      = "envoy-config"
    namespace = kubernetes_namespace.llm_gateway.metadata[0].name
  }
  data = {
    "envoy.yaml" = file("${path.module}/../../configs/envoy.yaml")
  }
}

resource "kubernetes_horizontal_pod_autoscaler_v2" "envoy_hpa" {
  metadata {
    name      = "envoy-gateway-hpa"
    namespace = kubernetes_namespace.llm_gateway.metadata[0].name
  }
  spec {
    scale_target_ref {
      api_version = "apps/v1"
      kind        = "Deployment"
      name        = kubernetes_deployment.envoy_gateway.metadata[0].name
    }
    min_replicas = var.min_replicas
    max_replicas = var.max_replicas
    metric {
      type = "Resource"
      resource {
        name = "cpu"
        target {
          type                = "Utilization"
          average_utilization = 70
        }
      }
    }
  }
}
