terraform {
  required_providers {
    aws = ">=4.51.0"
  }
  backend "s3" {
    bucket  = "carsten-remote-state"
    key     = "terraform.tfstate"
    region  = "us-east-1"
    profile = "pmp"
  }
}

provider "aws" {
  profile = "pmp"
  region  = "us-east-1"
}

data "aws_ami" "carsten_node_ami" {
  owners = [
    "self"
  ]
  name_regex  = "carsten_node"
  most_recent = true
}

resource "aws_vpc" "carsten_vpc" {
  tags = {
    Name = "carsten_vpc"
  }
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
}

resource "aws_subnet" "public_subnet" {
  cidr_block              = "10.0.0.0/24"
  vpc_id                  = aws_vpc.carsten_vpc.id
  map_public_ip_on_launch = true
  availability_zone       = "us-east-1b"
}

resource "aws_subnet" "db_subnet" {
  cidr_block              = "10.0.2.0/24"
  vpc_id                  = aws_vpc.carsten_vpc.id
  map_public_ip_on_launch = true
  availability_zone       = "us-east-1a"
}

resource "aws_internet_gateway" "internet_gateway" {
  tags = {
    Name = "carsten_internet_gateway"
  }
  vpc_id = aws_vpc.carsten_vpc.id
}

resource "aws_route_table" "main_route_table" {
  vpc_id = aws_vpc.carsten_vpc.id
  tags   = {
    Name = "main_route_table"
  }
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.internet_gateway.id
  }
}

resource "aws_main_route_table_association" "main_route_table_association" {
  vpc_id         = aws_vpc.carsten_vpc.id
  route_table_id = aws_route_table.main_route_table.id
}

resource "aws_security_group" "carsten_security_group" {
  name = "carsten_security_group"
  tags = {
    Name = "carsten_security_group"
  }
  vpc_id = aws_vpc.carsten_vpc.id
  ingress {
    description = "Allow ssh from admin"
    from_port   = 22
    protocol    = "tcp"
    to_port     = 22
    cidr_blocks = [
      "181.199.46.132/32",
      "157.100.174.220/32"
    ]
  }
  ingress {
    description = "Allow postgres from admin and subnets"
    from_port   = 5432
    protocol    = "tcp"
    to_port     = 5432
    cidr_blocks = [
      "181.199.54.3/32",
      "10.0.0.0/24",
      "10.0.2.0/24"
    ]
  }
  egress {
    from_port   = 0
    protocol    = "-1"
    to_port     = 0
    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }
  egress {
    from_port        = 0
    protocol         = "-1"
    to_port          = 0
    ipv6_cidr_blocks = [
      "::/0"
    ]
  }
}

resource "aws_db_subnet_group" "carsten_db_subnet" {
  name       = "carsten_db_subnet"
  subnet_ids = [
    aws_subnet.public_subnet.id,
    aws_subnet.db_subnet.id
  ]
}

resource "aws_db_instance" "carsten_database" {
  allocated_storage      = 100
  db_name                = "carsten"
  engine                 = "postgres"
  engine_version         = "14.5"
  instance_class         = "db.t3.small"
  storage_type           = "gp2"
  publicly_accessible    = true
  deletion_protection    = true
  db_subnet_group_name   = "carsten_db_subnet"
  username               = "postgres"
  password               = "quwefhq83fmhxi8mh3zim2hrfix3yymrfmqymrfdmkqzuhecifxqhyfmixqhyfi8"
  skip_final_snapshot    = false
  vpc_security_group_ids = [
    aws_security_group.carsten_security_group.id
  ]
}

resource "aws_spot_instance_request" "carsten_node" {
  spot_price                  = "0.036"
  depends_on                  = [aws_db_instance.carsten_database]
  ami                         = data.aws_ami.carsten_node_ami.id
  instance_type               = "c6i.large"
  key_name                    = "pmp-server"
  associate_public_ip_address = true
  subnet_id                   = aws_subnet.public_subnet.id
  security_groups             = [
    aws_security_group.carsten_security_group.id
  ]
  root_block_device {
    volume_size = "40"
  }
  user_data = <<EOF
#!/bin/bash
touch /.env
echo "DB_HOST=${aws_db_instance.carsten_database.address}" >> /.env
echo "DB_PORT=${aws_db_instance.carsten_database.port}" >> /.env
echo "DB_NAME=carsten" >> /.env
echo "DB_USER=postgres" >> /.env
echo "DB_PASS=quwefhq83fmhxi8mh3zim2hrfix3yymrfmqymrfdmkqzuhecifxqhyfmixqhyfi8" >> /.env
EOF
}

resource "aws_ec2_tag" "carsten_node_tag" {
  resource_id = aws_spot_instance_request.carsten_node.spot_instance_id
  key         = "Name"
  value       = "carsten_node"
}

output "db_endpoint" {
  value = aws_db_instance.carsten_database.endpoint
}

output "node_ip" {
  value = aws_spot_instance_request.carsten_node.public_ip
}