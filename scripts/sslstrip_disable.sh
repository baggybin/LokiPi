#! /bin/bash

killall -9 sslstrip
iptables -t nat -D PREROUTING 1
