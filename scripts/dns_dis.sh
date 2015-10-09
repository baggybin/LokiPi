#! /bin/bash

killall -9 dnsmasq


## temp Solution to add default gateway for ETH0 interface
## Will have to change this for auto DHCP assigned ETH address
## -- not my static address for testing and access

route add default gw 192.168.1.1 eth0

sudo ifconfig wlan1 10.0.0.1 netmask 255.255.255.0



echo "Starting"
#killall -9 dnsspoof
service dnsmasq start
sleep 6
#dnsmasq -p 0 -v &

#dnsspoof -i wlan1 -f /root/dnsspoof.hosts &

/rasberryPwnPi/hostapd-1.0-karma/hostapd/hostapd -dd /rasberryPwnPi/hostapd-1.0-karma/hostapd/hostapd-karma.conf & # -f /logs/hostapd_1.0_karma_wlan1_eth.log &


iptables --flush
iptables --table nat --flush
iptables --delete-chain
iptables --table nat --delete-chain
iptables --table nat --append POSTROUTING --out-interface eth0 -j MASQUERADE
iptables --append FORWARD --in-interface wlan1 -j ACCEPT
echo 1 > /proc/sys/net/ipv4/ip_forward


