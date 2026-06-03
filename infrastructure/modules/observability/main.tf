resource "kubernetes_namespace" "observability" {
metadata {
name = var.namespace

labels = {
  "app.kubernetes.io/managed-by" = "opentofu"
  "component"                    = "observability"
}

}
}

resource "kubernetes_config_map" "prometheus_config" {
metadata {
name      = "prometheus-config"
namespace = kubernetes_namespace.observability.metadata[0].name
}

data = {
"prometheus.yml" = templatefile("${path.module}/templates/prometheus.yml.tpl", {
gateway_namespace = var.gateway_namespace
scrape_interval   = var.scrape_interval
})
}
}

resource "kubernetes_deployment" "prometheus" {
metadata {
name      = "prometheus"
namespace = kubernetes_namespace.observability.metadata[0].name
}

spec {
replicas = 1

selector {
  match_labels = {
    app = "prometheus"
  }
}

template {
  metadata {
    labels = {
      app = "prometheus"
    }
  }

  spec {
    container {
      name  = "prometheus"
      image = "prom/prometheus:${var.prometheus_version}"

      args = [
        "--config.file=/etc/prometheus/prometheus.yml",
        "--web.enable-lifecycle"
      ]

      port {
        container_port = 9090
      }

      volume_mount {
        name       = "prometheus-config"
        mount_path = "/etc/prometheus"
      }

      volume_mount {
        name       = "prometheus-data"
        mount_path = "/prometheus"
      }
    }

    volume {
      name = "prometheus-config"

      config_map {
        name = kubernetes_config_map.prometheus_config.metadata[0].name
      }
    }

    volume {
      name = "prometheus-data"

      empty_dir {}
    }
  }
}

}
}

resource "kubernetes_service" "prometheus" {
metadata {
name      = "prometheus"
namespace = kubernetes_namespace.observability.metadata[0].name
}

spec {
selector = {
app = "prometheus"
}

port {
  port        = 9090
  target_port = 9090
}

type = "ClusterIP"

}
}

resource "kubernetes_secret" "grafana_credentials" {
metadata {
name      = "grafana-credentials"
namespace = kubernetes_namespace.observability.metadata[0].name
}

data = {
"admin-password" = var.grafana_admin_password
}

type = "Opaque"
}

resource "kubernetes_deployment" "grafana" {
metadata {
name      = "grafana"
namespace = kubernetes_namespace.observability.metadata[0].name
}

spec {
replicas = 1

selector {
  match_labels = {
    app = "grafana"
  }
}

template {
  metadata {
    labels = {
      app = "grafana"
    }
  }

  spec {
    container {
      name  = "grafana"
      image = "grafana/grafana:${var.grafana_version}"

      port {
        container_port = 3000
      }

      env {
        name = "GF_SECURITY_ADMIN_PASSWORD"

        value_from {
          secret_key_ref {
            name = kubernetes_secret.grafana_credentials.metadata[0].name
            key  = "admin-password"
          }
        }
      }
    }
  }
}

}
}

resource "kubernetes_service" "grafana" {
metadata {
name      = "grafana"
namespace = kubernetes_namespace.observability.metadata[0].name
}

spec {
selector = {
app = "grafana"
}

port {
  port        = 3000
  target_port = 3000
}

type = "ClusterIP"

}
}
