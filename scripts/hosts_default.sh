#! /bin/bash
# reset the DNS nameserver's to the Default google one
# Usually ends up being set a local gateway, which stops other connections resolving properly
#
#clear it out
sudo  echo " " > /etc/resolv.conf
## back to google server
sudo echo "nameserver 8.8.8.8" >  /etc/resolv.conf
