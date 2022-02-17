# variable "vpc_id" {
#   type = string
# }

# variable "subnet_id" {
#   type = string
# }

variable "app_name" {
  type    = string
  default = "gb-util"
}

variable "app_environment" {
  type    = string
  default = "dev"
}
