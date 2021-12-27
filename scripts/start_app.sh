#!/bin/bash
cp /app/cocktails.service /etc/systemd/system/cocktails.service
systemctl daemon-reload
systemctl start cocktails
systemctl enable cocktails
systemctl status cocktails
