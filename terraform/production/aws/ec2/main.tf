module "ec2" {
    source = "git::https://github.com/svanati/DataOps.git//terraform/modules/aws/ec2?ref=master"
    aws_instance_name = "airflow-us"
    aws_region = "us-east-1"
    ssh_pem_file = "AWS-DevOps"
}
