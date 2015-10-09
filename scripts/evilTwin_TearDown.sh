#! /bin/bash
#

sudo service dnsmasq stop
sudo killall -9 airbase-ng
sudo killall -9 hostapd

ifconfig wlan1 down

sleep 1s
iw reg set UK
sleep 1s

ifconfig wlan1 up

## when interface is started it will be increased from 20 dBm to 30 dBm
sleep 2

airmon-ng stop mon0

sleep 3s
 
