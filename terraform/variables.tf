variable "aws_region" {
  default = "us-east-1"
}

variable "ami_id" {
  description = "Ubuntu 22.04 AMI"
  default     = "ami-0c7217cdde317cfec"
}

variable "key_name" {
  description = "Your AWS key pair name"
}
