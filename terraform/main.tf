resource "docker_network" "password_manager_network" {
  name = "password_manager_network"
}

resource "docker_volume" "db_volume" {
  name = "password_manager_db_volume"
}

resource "docker_container" "db" {
  name  = "password_manager_db"
  image = "mysql:8.0"

  env = [
    "MYSQL_ROOT_PASSWORD=parola1",
    "MYSQL_DATABASE=login_info"
  ]

  networks_advanced {
    name = docker_network.password_manager_network.name
  }

  volumes {
    volume_name    = docker_volume.db_volume.name
    container_path = "/var/lib/mysql"
  }

  ports {
    internal = 3306
    external = 3306
  }
}

resource "docker_container" "web_app" {
  name  = "password_manager_web"
  image = "password_manager_web:latest"

  env = [
    "DB_HOST=password_manager_db",
    "DB_PORT=3306",
    "DB_USER=root",
    "DB_PASSWORD=parola1",
    "DB_NAME=login_info"
  ]

  networks_advanced {
    name = docker_network.password_manager_network.name
  }

  ports {
    internal = 8000
    external = 8000
  }

  depends_on = [docker_container.db]
}