#!/bin/bash

ip_master="192.168.1.128"
ping -c 2 $ip_master > /dev/null

if [ $? -ne 0 ]; then
echo "$(date) - master caigut: promocionant slave" >> /var/log/master_fail.log

sudo -u postgres pg_ctlcluster 18 main promote

echo "$(date) - slave promocionat a master" >> /var/log/master_fail.log
fi