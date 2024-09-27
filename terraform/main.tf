provider "kubernetes" {
  config_path = "~/.kube/config"
}

resource "kubernetes_deployment" "app" {
  metadata {
    name = "regression-model"
  }

  spec {
    replicas = 2
    selector {
      match_labels = {
        app = "regression-model"
      }
    }

    template {
      metadata {
        labels = {
          app = "regression-model"
        }
      }

      spec {
        container {
          image = "your-dockerhub-user/regression-model:latest"
          name  = "regression-model"
          port {
            container_port = 8000
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "app" {
  metadata {
    name = "regression-model-service"
  }

  spec {
    selector = {
      app = "regression-model"
    }

    port {
      port        = 80
      target_port = 8000
    }

    type = "LoadBalancer"
  }
}
