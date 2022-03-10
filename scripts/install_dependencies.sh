#!/bin/bash
yum -y update
yum install -y aws-cli
yum install -y amazon-linux-extras
amazon-linux-extras install python3.8
ln -sf $(which python3.8) /usr/bin/python3
cd /home/ec2-user || return
if [[ ! -f ./install ]]; then
  wget https://aws-codedeploy-us-east-2.s3.us-east-2.amazonaws.com/latest/install
  chmod +x ./install
fi
./install auto
service codedeploy-agent status
