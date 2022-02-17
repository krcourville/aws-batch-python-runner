# module "lambda" {
#   source  = "terraform-aws-modules/lambda/aws"
#   version = "2.34.0"

#   function_name = "${var.app_environment}-${var.app_name}"
#   handler       = "index.lambda_handler"
#   runtime       = "python3.8"
#   source_path   = "../src"
# }
