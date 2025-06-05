variable "db_user" {
  description = "PostgreSQL database user"
  type        = string
  default     = "postgres"
}

variable "db_password" {
  description = "PostgreSQL database password"
  type        = string
  default     = "postgres"
}

variable "db_name" {
  description = "PostgreSQL database name"
  type        = string
  default     = "password_manager"
}

variable "web_app_port" {
  description = "Port for the web application"
  type        = number
  default     = 8000
}

variable "db_port" {
  description = "Port for the PostgreSQL database"
  type        = number
  default     = 5432
} 