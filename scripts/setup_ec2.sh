#!/bin/bash
mkdir -p /app || return
mkdir -p /app/out || return
mkdir -p /app/log || return
chown -R ec2-user:ec2-user /app
chmod +x /app/scripts/*