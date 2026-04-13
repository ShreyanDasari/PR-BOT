# 1. PROVIDER CONFIGURATION
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1" # Ensure this matches your 'aws configure' region
}

# 2. IAM ROLE (The Bot's Identity)
resource "aws_iam_role" "aegis_role" {
  name = "AI_PR_Bot_Role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
    }]
  })
}

# 3. IAM POLICY (Granting Access to the "Brain" - Bedrock)
resource "aws_iam_role_policy" "bedrock_policy" {
  name = "BedrockInvokeAccess"
  role = aws_iam_role.aegis_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action   = ["bedrock:InvokeModel", "bedrock:ListFoundationModels"]
      Effect   = "Allow"
      Resource = "*" # Allows calling Claude/Llama on Bedrock
    }]
  })
}

resource "aws_iam_instance_profile" "aegis_profile" {
  name = "AI_PR_Bot_Profile"
  role = aws_iam_role.aegis_role.name
}

# 4. SECURITY GROUP (The Firewall)
resource "aws_security_group" "aegis_sg" {
  name        = "ai_pr_bot_sg"
  description = "Allow Streamlit (8501) and SSH (22)"

  # Streamlit Web UI Access
  ingress {
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Secure Shell Access
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow the bot to talk to the internet (to reach AWS Bedrock)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# 5. THE EC2 INSTANCE (The Server)
resource "aws_instance" "app_server" {
  ami           = "ami-0e86e20dae9224db8" # Amazon Linux 2023 AMI for us-east-1
  instance_type = "t3.micro"
  
  iam_instance_profile   = aws_iam_instance_profile.aegis_profile.name
  vpc_security_group_ids = [aws_security_group.aegis_sg.id]
  
  # IMPORTANT: Replace this with the name of your Key Pair created in AWS Console
  key_name = "PR-bot-key" 

  tags = {
    Name    = "AI_PR-Bot-Server"
    Project = "AI_PR-Bot"
  }
}

# 6. OUTPUTS
output "public_ip" {
  value       = aws_instance.app_server.public_ip
  description = "The public IP address of the bot server"
}