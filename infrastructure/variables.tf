variable "region" {
  type    = string
  default = "us-east-1"
}
variable "app_name" {
  type    = string
  default = "runner"
}

variable "app_env" {
  type    = string
  default = "dev"
}

variable "app_image" {
  type    = string
  default = "busybox"
}
