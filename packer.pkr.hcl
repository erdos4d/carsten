packer {
  required_plugins {
    amazon = {
      version = ">= 1.1.0"
      source  = "github.com/hashicorp/amazon"
    }
  }
}

source "amazon-ebs" "carsten_node" {
  profile  = "pmp"
  ami_name = "carsten_node"
  tags     = {
    Name    = "carsten_node"
    Release = "latest"
  }
  communicator            = "ssh"
  ssh_username            = "ubuntu"
  temporary_key_pair_type = "ed25519"
  force_deregister        = true
  force_delete_snapshot   = true
  instance_type           = "c6i.large"
  source_ami_filter {
    filters = {
      virtualization-type = "hvm"
      name                = "ubuntu/images/*ubuntu-jammy-22.04-amd64-server-*"
      root-device-type    = "ebs"
    }
    owners      = ["099720109477"]
    most_recent = true
  }
  launch_block_device_mappings {
    device_name           = "/dev/sda1"
    volume_size           = 20
    volume_type           = "gp2"
    delete_on_termination = true
  }
}

build {
  sources = [
    "source.amazon-ebs.carsten_node"
  ]

  provisioner "ansible" {
    playbook_file = "./playbook.yml"
    user          = "ubuntu"
    pause_before  = "10s"
    use_proxy     = false
  }
}
