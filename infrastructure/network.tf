# data "aws_availability_zones" "aws-az" {
#   state = "available"
# }

# resource "aws_vpc" "aws-vpc" {
#   cidr_block           = "10.0.0.0/16"
#   enable_dns_hostnames = true
#   tags = {
#     Name        = "${var.app_name}-vpc"
#     Environment = var.app_environment
#   }
# }

# resource "aws_subnet" "aws-subnet" {
#   count                   = length(data.aws_availability_zones.aws-az.names)
#   vpc_id                  = aws_vpc.aws-vpc.id
#   cidr_block              = cidrsubnet(aws_vpc.aws-vpc.cidr_block, 8, count.index + 1)
#   availability_zone       = data.aws_availability_zones.aws-az.names[count.index]
#   map_public_ip_on_launch = true
#   tags = {
#     Name = "${var.app_name}-subnet-${count.index + 1}"
#   }
# }

# resource "aws_internet_gateway" "aws-igw" {
#   vpc_id = aws_vpc.aws-vpc.id
#   tags = {
#     Name        = "${var.app_name}-igw"
#     Environment = var.app_environment
#   }
# }

# resource "aws_route_table" "aws-route-table" {
#   vpc_id = aws_vpc.aws-vpc.id
#   route {
#     cidr_block = "0.0.0.0/0"
#     gateway_id = aws_internet_gateway.aws-igw.id
#   }
#   tags = {
#     Name        = "${var.app_name}-route-table"
#     Environment = var.app_environment
#   }
# }

# resource "aws_main_route_table_association" "aws-route-table-association" {
#   vpc_id         = aws_vpc.aws-vpc.id
#   route_table_id = aws_route_table.aws-route-table.id
# }

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "3.12.0"

  name = var.app_name
  cidr = "10.0.0.0/16"

  azs             = ["${local.region}a", "${local.region}b", "${local.region}c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_ipv6 = true

  enable_nat_gateway = true
  single_nat_gateway = false
  one_nat_gateway_per_az = false

  tags = {
    Terraform   = "true"
    Environment = "${var.app_environment}"
  }
}
