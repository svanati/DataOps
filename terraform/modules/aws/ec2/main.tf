provider "aws" {
  region = var.aws_region

  # Allow any 2.x version of the AWS provider
  version = "~> 2.0"
}

terraform {
  # Require any 0.12.x version of Terraform
  required_version = ">= 0.12"
}

resource "aws_instance" "airflow" {
  ami                    = var.aws_ami
  instance_type          = var.aws_instance_type
  key_name               = var.ssh_pem_file
  vpc_security_group_ids = [aws_security_group.airflow.id]

  tags = {
    Name = "${var.aws_instance_name}"
  }
}

resource "aws_security_group" "airflow" {
  name        = var.aws_security_group
  description = "This security group and the following security rules provide the required access to the Apache Airflow service(s)"
}

resource "aws_security_group_rule" "ssh" {
  type              = "ingress"
  from_port         = var.aws_security_ssh_port
  to_port           = var.aws_security_ssh_port
  protocol          = "tcp"
  cidr_blocks       = [var.aws_security_cidr_blocks]
  security_group_id = aws_security_group.airflow.id
}

resource "aws_security_group_rule" "app" {
  type              = "ingress"
  from_port         = var.aws_security_app_port
  to_port           = var.aws_security_app_port
  protocol          = "tcp"
  cidr_blocks       = [var.aws_security_cidr_blocks]
  security_group_id = aws_security_group.airflow.id
}
