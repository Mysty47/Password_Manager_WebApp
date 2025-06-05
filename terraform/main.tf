terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

# Create a Docker network
resource "docker_network" "password_manager_network" {
  name = "password_manager_network"
}

# Create a Docker volume for the database
resource "docker_volume" "db_volume" {
  name = "password_manager_db_volume"
}

# Create the database container
resource "docker_container" "db" {
  name  = "password_manager_db"
  image = "postgres:latest"
  
  env = [
    "POSTGRES_USER=${var.db_user}",
    "POSTGRES_PASSWORD=${var.db_password}",
    "POSTGRES_DB=${var.db_name}"
  ]
  
  networks_advanced {
    name = docker_network.password_manager_network.name
  }
  
  volumes {
    volume_name    = docker_volume.db_volume.name
    container_path = "/var/lib/postgresql/data"
  }
  
  ports {
    internal = 5432
    external = var.db_port
  }
}

# Create the web application container
resource "docker_container" "web_app" {
  name  = "password_manager_web"
  image = "password_manager_web:latest"
  
  networks_advanced {
    name = docker_network.password_manager_network.name
  }
  
  ports {
    internal = 8000
    external = var.web_app_port
  }
  
  depends_on = [docker_container.db]
} 