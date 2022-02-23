resource "random_pet" "batch_bucket_suffix" {
  keepers = {
    app_prefix = local.prefix
  }
}

resource "aws_s3_bucket" "batch_bucket" {
  bucket = "${local.prefix}-${random_pet.batch_bucket_suffix.id}"
}
