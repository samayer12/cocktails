#!/bin/bash
# Must run on EC2 instance before code deploy agent
# grabs new versions of code. This should be automated, 
# but isn't right now.

sudo yum -y update
sudo yum -y install ruby
sudo yum -y install wget

cd /home/ec2-user

wget https:/aws-codedeploy-us-east-2.s3.us-east-2.amazonaws.com/latest/install
chmod +x ./install
sudo ./install auto
sudo service codedeploy-agent status
