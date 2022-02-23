# role assigned to Batch Compute Environment
resource "aws_iam_role" "runner_batch_svc_role" {
  name = "${local.prefix}-batch-svc-role"

  assume_role_policy = jsonencode({
    Version : "2012-10-17"
    Statement : [
      {
        Action : "sts:AssumeRole"
        Effect : "Allow"
        Principal : {
          Service : "batch.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "runner_batch_svc_role_attach_batch_service_role" {
  role       = aws_iam_role.runner_batch_svc_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBatchServiceRole"
}

# role assigned to ECS container
resource "aws_iam_role" "runner_task_exec_role" {
  name = "${local.prefix}-task-exec-role"
  assume_role_policy = jsonencode({
    Version : "2012-10-17"
    Statement : [
      {
        Action : "sts:AssumeRole"
        Effect : "Allow"
        Principal : {
          Service : "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "runner_task_exec_role_attach_ecs_task_exec_role" {
  role       = aws_iam_role.runner_task_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# role assigned to job definition
resource "aws_iam_role" "runner_job_role" {
  name = "${local.prefix}-job-role"
  assume_role_policy = jsonencode({
    Version : "2012-10-17"
    Statement : [
      {
        Action : "sts:AssumeRole"
        Effect : "Allow"
        Principal : {
          Service : "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
  inline_policy {
    name = "${local.prefix}-resource-access"
    policy = jsonencode({
      Version : "2012-10-17"
      Statement = [
        {
          Action = ["s3:*"]
          Effect = "Allow"
          Resource : [
            aws_s3_bucket.batch_bucket.arn,
            "${aws_s3_bucket.batch_bucket.arn}/*"
          ]
        }
      ]
    })
  }
}
