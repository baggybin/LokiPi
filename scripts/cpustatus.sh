#!/bin/bash
# cpustatus
#
# Prints the current state of the CPU like temperature, voltage and speed.
# The temperature is reported in degrees Celsius (C) while
# the CPU speed is calculated in megahertz (MHz).
 
function convert_to_MHz {
let value=$1/1000
echo "$value"
}
 
function calculate_overvolts {
# We can safely ignore the integer
# part of the decimal argument
# since it's not realistic to run the Pi
# at voltages higher than 1.99 V
let overvolts=${1#*.}-20
echo "$overvolts"
}
 
temp=$(vcgencmd measure_temp)
temp=${temp:5:4}
 
volts=$(vcgencmd measure_volts)
volts=${volts:5:4}
 
if [ $volts != "1.20" ]; then
overvolts=$(calculate_overvolts $volts)
fi
 
minFreq=$(cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_min_freq)
minFreq=$(convert_to_MHz $minFreq)
 
maxFreq=$(cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq)
maxFreq=$(convert_to_MHz $maxFreq)
 
freq=$(cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq)
freq=$(convert_to_MHz $freq)
 
governor=$(cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor)
 
echo "Temperature: $temp C"
echo -n "Voltage: $volts V"
[ $overvolts ] && echo " (+0.$overvolts overvolt)" || echo -e "\r"
echo "Min speed: $minFreq MHz"
echo "Max speed: $maxFreq MHz"
echo "Current speed: $freq MHz"
echo "Governor: $governor"
 
exit 0
