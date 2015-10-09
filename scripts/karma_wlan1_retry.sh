#! /bin/bash

### Script to try and correct when WLAN1 Ip doesnt get set

sudo ifconfig wlan1 10.0.0.1 netmask 255.255.255.0
ifconfig wlan1 up

service dnsmasq restart
sleep 6



iptables --flush
iptables --table nat --flush
iptables --delete-chain
iptables --table nat --delete-chain
iptables --table nat --append POSTROUTING --out-interface eth0 -j MASQUERADE
iptables --append FORWARD --in-interface wlan1 -j ACCEPT
echo 1 > /proc/sys/net/ipv4/ip_forward


