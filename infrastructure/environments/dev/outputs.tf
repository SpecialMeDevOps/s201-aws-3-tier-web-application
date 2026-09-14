output "vpc_id" {
  value = aws_vpc.main.id
}

output "public_subnet_ids" {
  value = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  value = aws_subnet.private[*].id
}

output "load_balancer_url" {
  value = "http://${aws_lb.app.dns_name}"
}

output "ecr_repository_url" {
  value = aws_ecr_repository.backend.repository_url
}

output "aurora_endpoint" {
  value     = aws_rds_cluster.aurora.endpoint
  sensitive = true
}