resource "aws_iam_role" "dev_bg_util_batch_svc_role" {
  name        = "dev-bg-util-batch-svc-role"
  description = "Service role for AWS Batch"

  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Action" : "sts:AssumeRole",
        "Effect" : "Allow",
        "Principal" : {
          "Service" : "batch.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "dev_bg_util_batch_svc_role_attach_batch_service_role" {
  role       = aws_iam_role.dev_bg_util_batch_svc_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBatchServiceRole"
}

resource "aws_security_group" "dev_bg_util_batch_compute_env_sg" {
  name   = "dev-bg-util-batch-compute-sg"
  vpc_id = module.vpc.vpc_id

  # egress {
  #   from_port        = 0
  #   to_port          = 0
  #   protocol         = "-1"
  #   cidr_blocks      = ["0.0.0.0/0"]
  #   ipv6_cidr_blocks = ["::/0"]
  # }
}

resource "aws_batch_compute_environment" "dev_bg_util_batch_compute_env" {
  compute_environment_name = "dev-bg-util"

  compute_resources {
    max_vcpus = 2

    security_group_ids = [
      aws_security_group.dev_bg_util_batch_compute_env_sg.id
    ]

    subnets = module.vpc.private_subnets
    type    = "FARGATE"
  }

  service_role = aws_iam_role.dev_bg_util_batch_svc_role.arn
  type         = "MANAGED"
  depends_on   = [aws_iam_role_policy_attachment.dev_bg_util_batch_svc_role_attach_batch_service_role]
}

resource "aws_iam_role" "dev_bg_util_task_execution_role" {
  name = "dev-bg-util-task-exec-role"
  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Action" : "sts:AssumeRole",
        "Effect" : "Allow",
        "Principal" : {
          "Service" : "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "dev_bg_util_task_exec_role_attach_cloudwatch_policy" {
  role       = aws_iam_role.dev_bg_util_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchFullAccess"
}

resource "aws_batch_job_definition" "dev_bg_util_batch_job_def" {
  name = "dev-bg-util"
  type = "container"
  platform_capabilities = [
    "FARGATE"
  ]
  container_properties = jsonencode({
    "command" : ["echo", "test"],
    "image" : "busybox",
    "fargatePlatformConfiguration" : {
      "platformVersion" : "LATEST"
    },
    "resourceRequirements" : [
      { "type" : "VCPU", "value" : "0.25" },
      { "type" : "MEMORY", "value" : "512" }
    ],
    "executionRoleArn" : "${aws_iam_role.dev_bg_util_task_execution_role.arn}"
  })
}

resource "aws_batch_job_queue" "dev_bg_util_batch_job_q" {
  name     = "dev-bg-util-batch-job-q"
  state    = "ENABLED"
  priority = 1
  compute_environments = [
    aws_batch_compute_environment.dev_bg_util_batch_compute_env.arn
  ]
}

resource "aws_cloudwatch_log_group" "aws_batch_job_log_group" {
  name              = "/aws/batch/job"
  retention_in_days = 5
}
