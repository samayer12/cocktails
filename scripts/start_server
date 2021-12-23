#!/bin/bash
service httpd start
service httpd enable

# User perms 
usermod -a -G apache ec2-user
groups
chown -R ec2-user:apache /var/www
chmod 2775 /var/www
find /var/www -type d -exec chmod 2775 {} \;
find /var/www -type f -exec chmod 0664 {} \;
