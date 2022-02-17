# NOTE: this resource will already exist.
# It should be imported so that retention can be applied.
resource "aws_cloudwatch_log_group" "aws_batch_job_log_group" {
  name              = "/aws/batch/job"
  retention_in_days = 5
}

resource "aws_iam_role" "runner_batch_svc_role" {
  name = "${local.prefix}-batch-svc-role"

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

resource "aws_iam_role_policy_attachment" "runner_batch_svc_role_attach_batch_service_role" {
  role       = aws_iam_role.runner_batch_svc_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBatchServiceRole"
}

resource "aws_security_group" "runner_batch_compute_sg" {
  name   = "${local.prefix}-runner-batch-compute-sg"
  vpc_id = module.vpc.vpc_id

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
}

resource "aws_batch_compute_environment" "runner_batch_compute_env" {
  compute_environment_name = local.prefix

  compute_resources {
    max_vcpus = 16

    security_group_ids = [
      aws_security_group.runner_batch_compute_sg.id
    ]

    subnets = module.vpc.private_subnets
    type    = "FARGATE"
  }

  service_role = aws_iam_role.runner_batch_svc_role.arn
  type         = "MANAGED"
  depends_on   = [aws_iam_role_policy_attachment.runner_batch_svc_role_attach_batch_service_role]
}

resource "aws_iam_role" "runner_task_exec_role" {
  name = "${local.prefix}-runner-task-exec-role"
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

resource "aws_iam_role_policy_attachment" "runner_task_exec_role_attach_cw_policy" {
  role       = aws_iam_role.runner_task_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchFullAccess"
}

resource "aws_batch_job_definition" "dev_bg_util_batch_job_def" {
  name = local.prefix
  type = "container"
  platform_capabilities = [
    "FARGATE"
  ]
  container_properties = jsonencode({
    "command" : ["echo", "test"],
    "image" : var.app_image,
    "fargatePlatformConfiguration" : {
      "platformVersion" : "LATEST"
    },
    "resourceRequirements" : [
      { "type" : "VCPU", "value" : "0.25" },
      { "type" : "MEMORY", "value" : "512" }
    ],
    "executionRoleArn" : aws_iam_role.runner_task_exec_role.arn
  })
}

resource "aws_batch_job_queue" "runner_general_q" {
  name     = "${local.prefix}-general-q"
  state    = "ENABLED"
  priority = 1
  compute_environments = [
    aws_batch_compute_environment.runner_batch_compute_env.arn
  ]
}
