#! /bin/bash



route del default gw 192.168.1.1 eth0

#
echo "Stopping"
killall -9 hostapd

service dnsmasq stop
ifconfig wlan1 down
sleep 2s
ifconfig wlan1 up

iptables --flush
iptables --table nat --flush
iptables --delete-chain
iptables --table nat --delete-chain

ifconfig wlan1 down
sleep 3s
ifconfig wlan1 up
sleep 3s
ifconfig mon.wlan1 down


