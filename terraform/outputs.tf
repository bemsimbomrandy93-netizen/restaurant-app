output "ec2_public_ip" {
  value = aws_instance.restaurant_ec2.public_ip
}
