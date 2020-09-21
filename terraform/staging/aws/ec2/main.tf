module "ec2" {
    source                   = "git::https://github.com/svanati/DataOps.git//terraform/modules/aws/ec2?ref=master"
    aws_instance_name        = "airflow-us-stage"
    aws_instance_type        = "t3.micro"
    aws_region               = "us-east-1"
    aws_security_cidr_blocks = "0.0.0.0/0"
    ssh_pem_file             = "AWS-DevOps"
}
