# ---------------------------------------------------------------------------------------------------------------------
# REQUIRED PARAMETERS
# You must provide a value for each of these parameters.
# ---------------------------------------------------------------------------------------------------------------------

variable "aws_instance_name" {
  description = "The instance name based on the current runtime environment"
  type        = string
}

variable "aws_instance_type" {
  description = "The EC2 instance type"
  type        = string
}

variable "aws_region" {
  description = "The AWS region"
  type        = string
}

variable "aws_security_app_port" {
  description = "The security rule port (Application)"
  type        = number
}

variable "aws_security_cidr_blocks" {
  description = "The security rule IP address range (CIDR)"
  type        = string
}

variable "aws_security_group" {
  description = "The access security group"
  type        = string
}

variable "ssh_pem_file" {
  description = "The SSH PEM file location"
  type        = string
}

# ---------------------------------------------------------------------------------------------------------------------
# OPTIONAL PARAMETERS
# These parameters have reasonable defaults.
# ---------------------------------------------------------------------------------------------------------------------

variable "aws_ami" {
  description = "The AWS AMI image id"
  type        = string
  default     = "ami-0c94855ba95c71c99"
}

variable "aws_security_ssh_port" {
  description = "The security rule port (SSH)"
  type        = number
  default     = 22
}
