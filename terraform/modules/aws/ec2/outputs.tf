output "airflow_private_ip" {
  value       = "${aws_instance.airflow.private_ip}"
  description = "Private IP for the Airflow instance"
}

output "airflow_public_dns" {
  value       = "${aws_instance.airflow.public_dns}"
  description = "Public DNS for the Airflow instance"
}

output "airflow_public_ip" {
  value       = "${aws_instance.airflow.public_ip}"
  description = "Public IP address for the Airflow instance"
}
