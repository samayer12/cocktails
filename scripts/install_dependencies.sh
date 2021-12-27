#!/bin/bash
yum -y update
yum install -y aws-cli
amazon-linux-extras install python3.8
cd /home/ec2-user || return
if [[ ! -f ./install ]]; then
  wget https://aws-codedeploy-us-east-2.s3.us-east-2.amazonaws.com/latest/install
  chmod +x ./install
fi
./install auto
service codedeploy-agent status