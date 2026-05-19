variable "TAG" {
  default = "latest"
}

group "default" {
  targets = ["backend", "frontend"]
}

target "_common" {
  dockerfile = "Dockerfile"
  target     = "production"
  platforms  = ["linux/amd64", "linux/arm64"]
  labels = {
    "org.opencontainers.image.created" = timestamp()
    "org.opencontainers.image.version" = "${TAG}"
  }
}

target "backend" {
  inherits = ["_common"]
  context  = "./backend"
  tags     = ["backend:${TAG}"]
}

target "frontend" {
  inherits = ["_common"]
  context  = "./frontend"
  tags     = ["frontend:${TAG}"]
}
